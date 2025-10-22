from flask_login import UserMixin
from core import db
import bcrypt


class User(UserMixin, db.Model):
    # opcional: __tablename__ = "user"  # para ficar explícito
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True, index=True)
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # precisa haver FK em Meal.user_id (abaixo) para isto funcionar
    meals = db.relationship(
        "Meal",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )