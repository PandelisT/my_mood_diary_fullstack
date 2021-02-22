from flask_login import UserMixin
from main import db


class Psychologist(UserMixin, db.Model):
    __tablename__ = "psychologists"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer)
