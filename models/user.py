from flask_login import UserMixin
from core import db
import bcrypt


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True, index=True)
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

  
    meals = db.relationship(
        "Meal",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )
