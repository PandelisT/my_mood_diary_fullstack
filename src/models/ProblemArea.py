from main import db
from datetime import datetime 
from sqlalchemy import text
from flask_login import UserMixin

class ProblemArea(UserMixin, db.Model):
    __tablename__ = "problem_area"

    id = db.Column(db.Integer, primary_key=True)
    problem_area_entry = db.Column(db.String())
    problem_area_date = db.Column(db.DateTime, default=datetime.now)
    user_id_fk = db.Column(db.Integer())

