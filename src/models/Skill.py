from main import db
from datetime import datetime
from flask_login import UserMixin


class Skill(UserMixin, db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    skill_entry = db.Column(db.String())
    skill_date = db.Column(db.DateTime, default=datetime.now)
    user_id_fk = db.Column(db.Integer())
