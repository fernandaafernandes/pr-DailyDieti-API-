from datetime import datetime
from core import db

class Meal(db.Model):
    # opcional: __tablename__ = "meal"
    id = db.Column(db.Integer, primary_key=True)

    # ➜ AQUI está a Foreign Key que faltava
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    # se você definir __tablename__ = "users" no User, mude para "users.id"
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), default="")
    calories = db.Column(db.Integer, nullable=False)
    when_at = db.Column(db.DateTime, nullable=False, index=True)
    in_diet = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)