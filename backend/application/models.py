from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .database import db 

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     username = db.Column(db.Text, unique = True, nullable = False)
#     email = db.Column(db.Text, unique = True, nullable = False)
#     password = db.Column(db.Text, nullable = False)
#     role = db.Column(db.Text, nullable = False, default = "user")


class UserCardDetail(db.Model):
    id = db.Column(db.Integer, primary_key = True)


# db = SQLAlchemy()

# -------------------------
# User Model (for normal users)
# -------------------------
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Text, nullable = False, default = "user")
    
    reservations = db.relationship('Reservation', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


# -------------------------
# Parking Lot Model
# -------------------------
class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'

    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)

    spots = db.relationship('ParkingSpot', backref='lot', lazy=True)

    def __repr__(self):
        return f'<ParkingLot {self.prime_location_name}>'


# -------------------------
# Parking Spot Model
# -------------------------
class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'

    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')  # A = Available, O = Occupied

    reservations = db.relationship('Reservation', backref='spot', lazy=True)

    def __repr__(self):
        return f'<ParkingSpot {self.id} in Lot {self.lot_id} - Status: {self.status}>'


# -------------------------
# Reservation Model
# -------------------------
class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    
    # vehicle_no = db.Column(db.String(20), nullable=False)
    parking_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f'<Reservation User {self.user_id} -> Spot {self.spot_id}>'
