from flask import current_app as app, jsonify, request, send_from_directory
from .models import *
from flask_jwt_extended import create_access_token, current_user, jwt_required
from functools import wraps
from datetime import datetime
import pytz # python timezone converter
from celery.result import AsyncResult
from .task import monthly_report, daily_parking_reminder
from .cache_config import cache  # Import cache object only
import time  # For measuring response times

# =================================================================================

def to_ist(utc_dt):
    utc = pytz.utc
    ist = pytz.timezone('Asia/Kolkata')
    return utc.localize(utc_dt).astimezone(ist)


def role_required(required_role): # this is  for role based authententication
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify(message="unauthorised"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


#=================================================================================


@app.route('/')
def index():
    return jsonify(message="Parking Lot Management API"), 200   #this is sample route / index page 


@app.route('/register', methods=['POST'])   # Registering users 
def user_register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    address = request.json.get("address")
    pincode = request.json.get("pincode")
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(message='Username already taken. Please choose another.'), 400
    
    this_user = User.query.filter_by(email=email).first()
    if this_user:
        return jsonify(message='Email already registered. Please log in.'), 400
    
    new_user = User(username=username, email=email, password=password, address=address, pincode=pincode, role='user')
    db.session.add(new_user)
    db.session.commit()
    
    cache.delete('admin_users')  # clearing admin users cache since new user added
    
    return jsonify(message='Registration successful! You can now log in.'), 201


@app.route('/login', methods=['POST'])
def login():   # login of user and admin
    role = request.json.get("role")
    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")

    if role == "admin":
        admin = User.query.filter_by(role="admin").first()
        if admin.username==username and admin.email == email and admin.password == password:
            access_token = create_access_token(identity=admin)
            return jsonify(access_token=access_token, role="admin", user_id=admin.id, email=admin.email, username=admin.username, message="Admin login successful"), 200
        return jsonify(message="Invalid admin credentials"), 400

    elif role == "user":
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify(message='User not Registered Please Register'), 400
        
        if user.username==username and user.role == "user":
            if user.password == password:
                access_token = create_access_token(identity=user)
                return jsonify(access_token=access_token, role="user", email=user.email, user_id=user.id, username=user.username, message="Login successful"), 200
            else:
                return jsonify(message="Incorrect password"), 400
        else:
            return jsonify(message="Invalid email or password"), 400
    
    return jsonify(message="Invalid role"), 400


# @app.route('/logout')
# def logout():   # logging out user/admin
#     return jsonify(message="Logged out successfully"), 200


# ==========================================================================================


@app.route("/admin", methods=["GET"])
@role_required("admin")
@cache.cached(timeout=60, key_prefix='admin_dashboard')  # Cache for 1 minute
def admin():   # admin route to show the detials of the lots and admin related info
    start_time = time.time()  # Start measuring response time
    
    lots = ParkingLot.query.all()
    
    lots_data = []
    for lot in lots:
        occupied = len([s for s in lot.spots if s.status == 'O'])
        available = len([s for s in lot.spots if s.status == 'A'])
        
        lots_data.append({
            "id": lot.id,
            "name": lot.prime_location_name,
            "address": lot.address,
            "pincode": lot.pincode,
            "price": lot.price,
            "max_spots": lot.max_spots,
            "occupied": occupied,
            "available": available
        })
    
    response_time = (time.time() - start_time) * 1000  # Calculate response time in milliseconds
    print(f"Admin dashboard response time: {response_time:.2f}ms")
    
    return jsonify(lots=lots_data, response_time_ms=round(response_time, 2)), 200


@app.route("/admin/add_lot", methods=["POST"])
@role_required("admin")
def add_parking_lot():
    """Add new parking lot - clears cache after adding"""
    prime_location = request.json.get('name')
    address = request.json.get("address")
    pincode = request.json.get("pincode")
    price = float(request.json.get('price'))
    max_spots = int(request.json.get('max_spots'))

    new_lot = ParkingLot(   # creating new parking lot 
        prime_location_name=prime_location,
        address=address,
        pincode=pincode,
        price=price,
        max_spots=max_spots
    )
    db.session.add(new_lot)
    db.session.commit()

    for i in range(1, max_spots + 1):
        new_spot = ParkingSpot(
            lot_id=new_lot.id,
            spot_number=i,
            status='A'
        )
        db.session.add(new_spot)
    
    db.session.commit()
    
    cache.delete('admin_dashboard')  # Clear admin dashboard cache
    cache.delete('admin_summary')  # Clear admin summary cache
    print("Cache cleared after adding parking lot")
    
    return jsonify(message=f"Parking lot added successfully", lot_id=new_lot.id), 201


@app.route('/admin/edit_lot/<int:lot_id>', methods=['GET', 'POST'])
@role_required("admin")
def edit_parking_lot(lot_id):  # editing the lot adding new or removing spots 
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify(message="Lot not found"), 404
    
    occupied_count = len([s for s in lot.spots if s.status == 'O'])
    current_spot_count = len(lot.spots)

    if request.method == 'GET':
        return jsonify({
            "id": lot.id,
            "name": lot.prime_location_name,
            "address": lot.address,
            "pincode": lot.pincode,
            "price": lot.price,
            "max_spots": lot.max_spots,
            "occupied_count": occupied_count,
            "current_spot_count": current_spot_count
        }), 200

    if request.method == 'POST':
        lot.prime_location_name = request.json.get("name")
        lot.address = request.json.get("address")
        lot.pincode = request.json.get("pincode")
        lot.price = float(request.json.get("price"))
        new_max_spots = int(request.json.get("max_spots"))

        if new_max_spots < occupied_count:
            return jsonify(message="Cannot reduce max spots below current occupied spots"), 400   # logic to not remove the spots based if occupied 

        lot.max_spots = new_max_spots
        db.session.commit()

        if new_max_spots > current_spot_count:
            for i in range(current_spot_count + 1, new_max_spots + 1):
                new_spot = ParkingSpot(
                    lot_id=lot.id,
                    spot_number=i,
                    status='A'
                )
                db.session.add(new_spot)

        elif new_max_spots < current_spot_count:
            removable_spots = (
                ParkingSpot.query
                .filter_by(lot_id=lot.id, status='A')
                .order_by(ParkingSpot.spot_number.desc())
                .limit(current_spot_count - new_max_spots)
                .all()
            )
            for spot in removable_spots:
                db.session.delete(spot)

        db.session.commit()
        
        cache.delete('admin_dashboard')  # Clear admin dashboard cache
        cache.delete('admin_summary')  # Clear admin summary cache
        print("Cache cleared after editing parking lot")
        
        return jsonify(message="Parking lot updated successfully"), 200


@app.route('/admin/users')
@role_required("admin")
@cache.cached(timeout=300, key_prefix='admin_users')  # Cache for 5 minutes
def admin_view_users():   # veiwing  the users in the db
    start_time = time.time()
    
    users = User.query.filter_by(role='user').all()
    users_data = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "address": user.address,
            "pincode": user.pincode
        }
        for user in users
    ]
    
    response_time = (time.time() - start_time) * 1000
    print(f"Admin users response time: {response_time:.2f}ms")
    
    return jsonify(users=users_data, response_time_ms=round(response_time, 2)), 200


@app.route('/admin/delete_lot/<int:lot_id>', methods=['POST'])
@role_required("admin")
def delete_parking_lot(lot_id):   # deleting the parking lot 
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify(message="Lot not found"), 404

    reservations = Reservation.query.filter_by(lot_id=lot.id).all()
    for r in reservations:
        db.session.delete(r)  # deleting from database the reservation

    spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
    for s in spots:
        db.session.delete(s)

    db.session.delete(lot)
    db.session.commit()
    
    cache.delete('admin_dashboard')  # Clear admin dashboard cache
    cache.delete('admin_summary')  # Clear admin summary cache
    print("Cache cleared after deleting parking lot")
    
    return jsonify(message="Parking lot deleted successfully"), 200


@app.route('/admin/spot_info/<int:lot_id>/<int:spot_number>')
@role_required("admin")
def view_spot_info(lot_id, spot_number):  # getting info of the spot based on the user allotement
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, spot_number=spot_number).first()
    if not spot:
        return jsonify(message="Spot not found"), 404
    
    reservation = Reservation.query.filter_by(spot_id=spot.id, leaving_timestamp=None).first()  # checking the reservatioon of the user 

    if not reservation:
        return jsonify(message="No active reservation found for this spot"), 200

    user = reservation.user
    return jsonify({
        "spot_number": spot.spot_number,
        "status": spot.status,
        "reservation": {
            "id": reservation.id,
            "vehicle_number": reservation.vehicle_number,
            "parking_timestamp": reservation.parking_timestamp.isoformat() if reservation.parking_timestamp else None,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
    }), 200


@app.route('/admin/summary')
@role_required("admin")
@cache.cached(timeout=120, key_prefix='admin_summary')  # Cache for 2 minutes
def admin_summary():   # finding the sumary stats of admin dashboard
    start_time = time.time()
    
    lots = ParkingLot.query.all()
    reservations = Reservation.query.all()
     
    total_lots = len(lots)
    total_spots = sum(lot.max_spots for lot in lots)
    total_occupied = sum(
        len([s for s in lot.spots if s.status == 'O']) for lot in lots
    )
    total_available = total_spots - total_occupied
    total_revenue = sum(r.total_cost or 0 for r in reservations if r.total_cost)

    revenue_by_lot = [
        {
            "lot": lot.prime_location_name,
            "revenue": sum(r.total_cost or 0 for r in lot.reservations)
        }
        for lot in lots
    ]

    occupancy_by_lot = [
        {
            "lot": lot.prime_location_name,
            "occupied": len([s for s in lot.spots if s.status == 'O']),
            "available": len([s for s in lot.spots if s.status == 'A']),
        }
        for lot in lots
    ]

    response_time = (time.time() - start_time) * 1000
    print(f"Admin summary response time: {response_time:.2f}ms")

    return jsonify({
        "total_lots": total_lots,
        "total_spots": total_spots,
        "total_occupied": total_occupied,
        "total_available": total_available,
        "total_revenue": total_revenue,
        "revenue_by_lot": revenue_by_lot,
        "occupancy_by_lot": occupancy_by_lot,
        "response_time_ms": round(response_time, 2)
    }), 200


# ==========================================================================================


@app.route('/user/<int:user_id>')
@role_required("user")
def user_dashboard(user_id):    # user dashboard and info of parking lot 
    start_time = time.time()
    
    if current_user.id != user_id and current_user.role != 'admin':
        return jsonify(message="Unauthorized access"), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 404

    recent_reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.parking_timestamp.desc()).all()
    
    reservations_data = [    # info of reservation data 
        {
            "id": r.id,
            "lot_id": r.lot_id,
            "lot_name": r.lot.prime_location_name,
            "spot_number": r.spot_number,
            "vehicle_number": r.vehicle_number,
            "parking_timestamp": r.parking_timestamp.isoformat() if r.parking_timestamp else None,
            "leaving_timestamp": r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
            "total_cost": r.total_cost,
            "status": "active" if r.leaving_timestamp is None else "completed"
        }
        for r in recent_reservations
    ]

    parking_lots = ParkingLot.query.all()  # parking info 
    lots_with_availability = []
    for lot in parking_lots:
        available_spots = sum(1 for spot in lot.spots if spot.status == 'A')
        lots_with_availability.append({
            'id': lot.id,
            'name': lot.prime_location_name,
            'address': lot.address,
            'pincode': lot.pincode,
            'price': lot.price,
            'available': available_spots
        })

    response_time = (time.time() - start_time) * 1000
    print(f"User dashboard response time: {response_time:.2f}ms")

    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "address": user.address,
            "pincode": user.pincode
        },
        "reservations": reservations_data,
        "lots": lots_with_availability,
        "response_time_ms": round(response_time, 2)
    }), 200


@app.route('/user/book/<int:lot_id>/<int:user_id>', methods=['GET'])
@role_required("user")
def book_parking_spot(lot_id, user_id):      #  Get booking information for a specific lot
    if current_user.id != user_id:
        return jsonify(message="Unauthorized access"), 403
    
    lot = ParkingLot.query.get(lot_id)
    user = User.query.get(user_id)
    
    if not lot or not user:
        return jsonify(message="Lot or User not found"), 404

    available_spot = ParkingSpot.query.filter_by(
        lot_id=lot_id, status='A'
    ).order_by(ParkingSpot.spot_number).first()

    if not available_spot:
        return jsonify(message='No available spots in this lot!'), 400
    
    return jsonify({
        "lot": {
            "id": lot.id,
            "name": lot.prime_location_name,
            "address": lot.address,
            "price": lot.price
        },
        "spot": {
            "id": available_spot.id,
            "spot_number": available_spot.spot_number
        },
        "user": {
            "id": user.id,
            "username": user.username
        }
    }), 200


@app.route('/user/reserve', methods=['POST'])
@role_required("user")
def reserve_spot():  # Reserve a parking spot for the user 
    lot_id = request.json.get('lot_id')
    spot_number = request.json.get('spot_number')
    user_id = request.json.get('user_id')
    vehicle_number = request.json.get('vehicle_number')
    
    if current_user.id != int(user_id):
        return jsonify(message="Unauthorized access"), 403

    spot = ParkingSpot.query.filter_by(lot_id=lot_id, spot_number=spot_number).first()

    if not spot:
        return jsonify(message='Invalid spot!'), 400

    if spot.status == 'O':
        return jsonify(message='Spot already occupied!'), 400

    spot.status = 'O'

    new_reservation = Reservation(    # creates new reservation
        lot_id=lot_id,                     
        spot_id=spot.id,
        spot_number=spot.spot_number,       
        user_id=user_id,
        vehicle_number=vehicle_number,     
        parking_timestamp=to_ist(datetime.utcnow()).replace(tzinfo=None),
        leaving_timestamp=None,
        total_cost=None
    )

    db.session.add(new_reservation)
    db.session.commit()

    cache.delete('admin_dashboard')  # Clear admin dashboard (spot counts changed)
    cache.delete('admin_summary')  # Clear admin summary (stats changed)
    print("Cache cleared after reservation")

    return jsonify(message="Spot reserved successfully", reservation_id=new_reservation.id), 201


@app.route('/user/release/<int:res_id>', methods=['GET', 'POST'])
@role_required("user")
def release_spot(res_id):
    reservation = Reservation.query.get(res_id)  #    Release a parking spot - clears cache after release
    if not reservation:
        return jsonify(message="Reservation not found"), 404
    
    if current_user.id != reservation.user_id:
        return jsonify(message="Unauthorized access"), 403
    
    spot = reservation.spot
    lot = ParkingLot.query.get(reservation.lot_id)

    now = to_ist(datetime.utcnow()).replace(tzinfo=None)
    hours = max(1, int((now - reservation.parking_timestamp).total_seconds() // 3600))
    cost = lot.price * hours

    if request.method == 'GET':
        return jsonify({
            "lot_id": lot.id,
            "reservation_id": reservation.id,
            "lot_name": lot.prime_location_name,
            "spot_number": spot.spot_number,
            "vehicle_number": reservation.vehicle_number,
            "parking_timestamp": reservation.parking_timestamp.isoformat(),
            "current_time": now.isoformat(),
            "hours_parked": hours,
            "total_cost": cost
        }), 200

    if request.method == 'POST':
        reservation.leaving_timestamp = now
        reservation.total_cost = cost
        spot.status = 'A'

        db.session.commit()
        
        cache.delete('admin_dashboard')  # Clear admin dashboard (spot counts changed)
        cache.delete('admin_summary')  # Clear admin summary (revenue changed)
        print("Cache cleared after spot release")
        
        return jsonify(message="Spot released successfully", total_cost=cost), 200


@app.route('/user/remove/<int:res_id>', methods=['POST'])
@role_required("user")
def remove_reservation(res_id):  #  remove a completed reservation from histpry of user dash
    reservation = Reservation.query.get(res_id)
    if not reservation:
        return jsonify(message="Reservation not found"), 404
    
    if current_user.id != reservation.user_id:
        return jsonify(message="Unauthorized access"), 403

    if reservation.leaving_timestamp is None:
        return jsonify(message='You can only remove after parked out'), 400

    user_id = reservation.user_id
    
    db.session.delete(reservation)
    db.session.commit()
    
    print("Cache cleared after removing reservation")

    return jsonify(message="Reservation removed successfully"), 200


@app.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@role_required("user")
def edit_profile(user_id):  # Edit user profile with no change in email as it is primary key 
    if current_user.id != user_id:
        return jsonify(message="Unauthorized access"), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 404

    if request.method == 'GET':
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "address": user.address,
            "pincode": user.pincode
        }), 200

    if request.method == 'POST':
        new_username = request.json.get('username')
        
        if new_username and new_username != user.username:  
            existing = User.query.filter_by(username=new_username).first()
            if existing:
                return jsonify(message="Username already taken"), 400
            user.username = new_username
        
        user.address = request.json.get('address')
        user.pincode = request.json.get('pincode')

        db.session.commit()
        
        cache.delete('admin_users')  # Clear admin users cache
        print("Cache cleared after profile update")
        
        return jsonify(message="Profile updated successfully"), 200


@app.route("/user/summary/<int:user_id>")
@role_required("user")
def user_summary(user_id):    # summary statsfor specific user
    if current_user.id != user_id:
        return jsonify(message="Unauthorized access"), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 404
    
    reservations = Reservation.query.filter_by(user_id=user_id).all()

    total_reservations = len(reservations)
    total_spent = sum(r.total_cost or 0 for r in reservations)

    usage_by_lot = {}
    for r in reservations:
        lot = ParkingLot.query.get(r.lot_id)  
        lot_name = lot.prime_location_name if lot else "Unknown Lot"
        usage_by_lot[lot_name] = usage_by_lot.get(lot_name, 0) + 1

    usage_data = [{"lot": lot, "count": count} for lot, count in usage_by_lot.items()]

    return jsonify({
        "username": user.username,
        "userid": user.id,
        "total_reservations": total_reservations,
        "total_spent": total_spent,
        "usage_data": usage_data
    }), 200


# ==========================================================================================

# these are all for task to work backend jobs 
@app.route('/user/export_csv/<int:user_id>', methods=['POST'])
@role_required("user")
def trigger_csv_export(user_id): # Trigger async CSV export task
    from .task import export_user_parking_csv
    
    if current_user.id != user_id:
        return jsonify(message="Unauthorized access"), 403
    
    task = export_user_parking_csv.delay(user_id)
    print(task)
    return jsonify(message="CSV export started", task_id=task.id), 202


@app.route('/user/csv_status/<task_id>')
@role_required("user")
def check_csv_status(task_id): # Check status of CSV export task
    task_result = AsyncResult(task_id)
    print(f"Task Result: {task_result}")
    if task_result.ready():
        if task_result.successful():
            return jsonify(status="completed", filename=task_result.result), 200
        else:
            return jsonify(status="failed", error=str(task_result.result)), 500
    else:
        return jsonify(status="processing"), 202


@app.route('/user/download_csv/<filename>')
def download_csv(filename):   # Download the generated CSV file
    return send_from_directory('static', filename, as_attachment=True)


@app.route('/api/send_mail')
def send_mail():   # Manual trigger for monthly report"""
    res = monthly_report.delay()
    return jsonify(message="Monthly report task triggered", task_id=res.id)


# =========================================================================================