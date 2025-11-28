from .database import db
from datetime import datetime


class User(db.Model):  # this is the user table
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    
    # Relationships
    reservations = db.relationship('Reservation', backref='user', cascade="all, delete", passive_deletes=True)


class ParkingLot(db.Model):  # this is where the lots are created and stored
    __tablename__ = 'parking_lots'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prime_location_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    max_spots = db.Column(db.Integer, nullable=False)
    
    # Relationships
    spots = db.relationship("ParkingSpot", backref="lot", cascade="all, delete", passive_deletes=True)
    reservations = db.relationship('Reservation', backref='lot', cascade="all, delete", passive_deletes=True)


class ParkingSpot(db.Model): # this is the parking spot specific info of lot
    __tablename__ = 'parking_spots'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id', ondelete="CASCADE"), nullable=False)
    spot_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')  # A = Available, O = Occupied
    
    # Relationships
    reservations = db.relationship("Reservation", backref="spot", cascade="all, delete", passive_deletes=True)
    
    # Composite unique constraint
    __table_args__ = (
        db.UniqueConstraint('lot_id', 'spot_number', name='unique_spot_per_lot'),
    )


class Reservation(db.Model):   # this is where the user reserves the spot 
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id', ondelete='CASCADE'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id', ondelete='CASCADE'), nullable=False)
    spot_number = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    total_cost = db.Column(db.Float, nullable=True)