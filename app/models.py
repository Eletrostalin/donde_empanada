# models.py

from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    second_name = db.Column(db.String(150), nullable=False)
    phone_hash = db.Column(db.String(256), unique=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_phone(self, phone):
        self.phone_hash = generate_password_hash(phone)

    def check_phone(self, phone):
        return check_password_hash(self.phone_hash, phone)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    average_rating = db.Column(db.Float, default=0, nullable=False)
    rating_count = db.Column(db.Integer, default=0)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    address = db.Column(db.String(255), nullable=True)
    working_hours = db.Column(db.String(255), nullable=True)
    average_check = db.Column(db.Integer, nullable=True)

    reviews = db.relationship('Review', backref='location', lazy=True)
    owner_info = db.relationship('OwnerInfo', backref='location', uselist=False)  # Связь с OwnerInfo

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='reviews', lazy=True)

    def __repr__(self):
        return f'<Review {self.rating}>'

class OwnerInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    website = db.Column(db.String(200), nullable=True)
    owner_info = db.Column(db.Text, nullable=False)

    user = db.relationship('User', backref='owner_info', lazy=True)

class Migration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    migration_name = db.Column(db.String(255), nullable=False, unique=True)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Migration {self.migration_name} applied at {self.applied_at}>'

    def __repr__(self):
        return f'<OwnerInfo {self.id}>'
