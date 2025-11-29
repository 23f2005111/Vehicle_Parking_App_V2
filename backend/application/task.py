from celery import shared_task
import csv
import os
from jinja2 import Template
from .mail import send_email
from .models import User, Reservation, ParkingLot, ParkingSpot
import datetime
import requests


# Task 1 - Export CSV report for user
# User triggered async job
@shared_task(ignore_results=False, name="export_user_parking_csv")
def export_user_parking_csv(user_id):
    """Export parking history for a specific user as CSV"""
    print(f" Generating CSV report for user_id: {user_id}")
    
    try:
        reservations = Reservation.query.filter_by(user_id=user_id).all()
        csv_file_name = f"parking_report_{user_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        
        os.makedirs('static', exist_ok=True)
        csv_path = os.path.join('static', csv_file_name)
        
        with open(csv_path, 'w', newline="") as csvfile:
            parking_csv = csv.writer(csvfile, delimiter=',')
            
            if not reservations:
                # Create CSV with "No reservations" message
                parking_csv.writerow(['Message'])
                parking_csv.writerow(['No reservations found for this user'])
                print(f"No reservations found for user {user_id}, created CSV with message")
            else:
                # Write headers and reservation data
                parking_csv.writerow(['Sr No.', 'Lot Name', 'Spot Number', 'Vehicle Number', 
                                     'Parking Time', 'Leaving Time', 'Total Cost', 'Status'])
                
                sr_no = 1
                for r in reservations:
                    lot = ParkingLot.query.get(r.lot_id)
                    lot_name = lot.prime_location_name if lot else "Unknown"
                    status = "Active" if r.leaving_timestamp is None else "Completed"
                    parking_time = r.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S') if r.parking_timestamp else "N/A"
                    leaving_time = r.leaving_timestamp.strftime('%Y-%m-%d %H:%M:%S') if r.leaving_timestamp else "N/A"
                    
                    this_row = [sr_no, lot_name, r.spot_number, r.vehicle_number, 
                               parking_time, leaving_time, r.total_cost or "N/A", status]
                    parking_csv.writerow(this_row)
                    sr_no += 1
                
                print(f"CSV generated: {csv_file_name} ({sr_no-1} records)")
        
        return csv_file_name
    
    except Exception as e:
        print(f" Error generating CSV: {str(e)}")
        raise e


# Task 2 - Monthly activity report sent via mail
# Scheduled job via crontab (runs on 1st of every month or every 2 minutes for testing)
@shared_task(ignore_results=False, name="monthly_report")
def monthly_report():
    """Send monthly parking activity report to all users"""
    users = User.query.filter_by(role='user').all()
    
    print(f" Found {len(users)} users with role='user'")
    
    email_count = 0
    
    for user in users:
        # Get user's reservations from the current month
        today = datetime.datetime.now()
        first_day_current_month = datetime.datetime(today.year, today.month, 1)
        
        # Get reservations from current month
        reservations = Reservation.query.filter(
            Reservation.user_id == user.id,
            Reservation.parking_timestamp >= first_day_current_month
        ).all()
        
        if not reservations:
            print(f"Skipping {user.username} ({user.email}) - no reservations this month")
            continue
        
        print(f" {user.username} has {len(reservations)} reservations this month")
        
        # Calculate statistics
        total_bookings = len(reservations)
        total_spent = sum(r.total_cost or 0 for r in reservations)
        
        # Most used parking lot
        lot_usage = {}
        for r in reservations:
            lot = ParkingLot.query.get(r.lot_id)
            if lot:
                lot_name = lot.prime_location_name
                lot_usage[lot_name] = lot_usage.get(lot_name, 0) + 1
        
        most_used_lot = max(lot_usage, key=lot_usage.get) if lot_usage else "N/A"
        
        # Prepare data for template
        user_data = {
            'username': user.username,
            'email': user.email,
            'month': today.strftime('%B %Y'),  # current month
            'total_bookings': total_bookings,
            'total_spent': total_spent,
            'most_used_lot': most_used_lot,
            'reservations': []
        }
        
        for r in reservations:
            lot = ParkingLot.query.get(r.lot_id)
            user_data['reservations'].append({
                'lot_name': lot.prime_location_name if lot else "Unknown",
                'vehicle_number': r.vehicle_number,
                'parking_time': r.parking_timestamp.strftime('%d-%m-%Y %H:%M') if r.parking_timestamp else "N/A",
                'cost': r.total_cost or 0
            })
        
        # Email template
        mail_template = """
        <h2>Monthly Parking Activity Report</h2>
        <h3>Dear {{user_data.username}},</h3>
        <p>Here's your parking activity summary for <strong>{{user_data.month}}</strong>:</p>
        
        <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h4>Summary:</h4>
            <ul>
                <li><strong>Total Bookings:</strong> {{user_data.total_bookings}}</li>
                <li><strong>Total Amount Spent:</strong> ₹{{user_data.total_spent}}</li>
                <li><strong>Most Used Parking Lot:</strong> {{user_data.most_used_lot}}</li>
            </ul>
        </div>
        
        <h4>Booking Details:</h4>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #e0e0e0;">
                <th>Parking Lot</th>
                <th>Vehicle Number</th>
                <th>Parking Time</th>
                <th>Cost (₹)</th>
            </tr>
            {% for reservation in user_data.reservations %}
            <tr>
                <td>{{reservation.lot_name}}</td>
                <td>{{reservation.vehicle_number}}</td>
                <td>{{reservation.parking_time}}</td>
                <td>{{reservation.cost}}</td>
            </tr>
            {% endfor %}
        </table>
        
        <p style="margin-top: 20px;">Visit our app at <a href="http://127.0.0.1:5173">http://127.0.0.1:5173</a> for more details.</p>
        
        <h5>Regards,<br>
        Parking Lot Management Team</h5>
        """
        
        message = Template(mail_template).render(user_data=user_data)

        # Send email
        print(f" Sending email to {user.email}...")
        try:
            result = send_email(user.email, subject=f"Monthly Parking Report - {user_data['month']}", message=message)
            if result:
                email_count += 1
                print(f" Email sent successfully to {user.email}")
            else:
                print(f"Email failed for {user.email}")
        except Exception as e:
            print(f"Exception sending email to {user.email}: {str(e)}")
    
    result_msg = f"Monthly reports sent to {email_count} user(s)"
    print(f" {result_msg}")
    return result_msg


# Task 3 - Daily reminder via Google Chat webhook
# Scheduled job (runs daily in the evening or every 2 minutes for testing)
@shared_task(ignore_results=False, name="daily_parking_reminder")
def daily_parking_reminder():
    """Send daily reminders to users who haven't booked parking"""
    users = User.query.filter_by(role='user').all()
    
    print(f" Checking {len(users)} users for daily reminders")
    
    reminder_count = 0
    
    for user in users:
        # Check if user has any active reservation today
        active_reservation = Reservation.query.filter(
            Reservation.user_id == user.id,
            Reservation.leaving_timestamp == None
        ).first()
        
        if not active_reservation:
            text = f"Hi {user.username}, you haven't booked a parking spot today. Visit our app to reserve your spot now: http://127.0.0.1:5173"
            
            # Your Google Chat webhook URL
            webhook_url = "https://chat.googleapis.com/v1/spaces/AAQACx2a9KM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=NalLhNhIphRIGkp1gjv5X7SRdtVNfwyA-18wxMTEpTA"
            
            print(f"Reminder for {user.username}: {text}")
            reminder_count += 1
            
            try:
                response = requests.post(webhook_url, json={"text": text})
                print(f"Reminder sent to {user.username}: {response.status_code}")
            except Exception as e:
                print(f" Error sending reminder to {user.username}: {str(e)}")
        else:
            print(f" {user.username} already has active reservation")
    
    result_msg = f"Daily reminders sent to {reminder_count} user(s)"
    print(f" {result_msg}")
    return result_msg