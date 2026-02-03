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

    # Relationship to scores
    scores = db.relationship(
        "Score", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"

    def get_id(self):
        """Required by Flask-Login"""
        return str(self.id)


class Score(db.Model):
    """Score model for storing game results"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, index=True
    )
    difficulty = db.Column(
        db.String(20), nullable=False
    )  # easy, medium, expert, master, extreme
    score = db.Column(db.Integer, nullable=False)
    time_seconds = db.Column(db.Integer, nullable=False)  # Total time in seconds
    mistakes = db.Column(db.Integer, nullable=False)  # Number of mistakes
    completed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<Score user={self.user_id} difficulty={self.difficulty} score={self.score}>"

    def to_dict(self):
        """Convert score to dictionary"""
        return {
            "id": self.id,
            "difficulty": self.difficulty,
            "score": self.score,
            "time_seconds": self.time_seconds,
            "mistakes": self.mistakes,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
        }
