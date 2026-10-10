from datetime import datetime, timezone
from .extensions import db
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# test class 
class Item(db.Model):
    """Placeholder model. Rename or replace to suit your domain."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Item {self.id} {self.name!r}>"

# class User 
class User(UserMixin, db.Model): 
    __tablename__ = 'users'

    # columns 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # hash passwords safely
    def set_password(self, password): 
        self.password_hash = generate_password_hash(password)

    # verify password on login 
    def check_password(self, password): 
        return check_password_hash(self.password_hash, password)

    def to_dict(self): 
        return {
            "id": self.id, 
            "username": self.username, 
            "created_at": self.created_at.isoformat()
        }
    
    # visual represenataion -> object for debugging 
    def __repr__(self): 
        return f'<User {self.username}'