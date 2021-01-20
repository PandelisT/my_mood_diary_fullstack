from main import db
from datetime import datetime 
from sqlalchemy import text
from flask_login import UserMixin

class Journal(UserMixin, db.Model):
    __tablename__ = "journal"

    id = db.Column(db.Integer, primary_key=True)
    journal_entry = db.Column(db.String())
    journal_date = db.Column(db.DateTime, default=datetime.now)
    user_id_fk = db.Column(db.Integer())

    @classmethod
    def date_filter(cls, year, month, day, user_id):
        sql_query = text("SELECT * FROM  journal WHERE DATE(journal_date) = ':year-:month-:day' and client_id_fk=':user_id';")
        return  db.engine.execute(sql_query, {"year":year, "month": month, "day": day, "user_id": user_id})