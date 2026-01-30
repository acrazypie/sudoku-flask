"""
Database models for Sudoku Flask app
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for storing user information"""

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(120), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    nickname = db.Column(db.String(120), nullable=True)
    picture = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<User {self.email}>"

    def get_id(self):
        """Required by Flask-Login"""
        return str(self.id)
