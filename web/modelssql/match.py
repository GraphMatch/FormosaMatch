# match.py

import datetime
from app import db, bcrypt
from modelssql.user import User

class Match(db.Model):

    __tablename__ = "match"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_a_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_b_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    user_b = db.relationship("User", back_populates="matches_a")
    user_a = db.relationship("User", back_populates="matches_b")
    messages = db.relationship("Message", back_populates="match")

    __table_args__ = (db.UniqueConstraint('user_a_id', 'user_b_id', name='_users_match'),)

    def __init__(self, status):
        self.status = status
        self.timestamp = datetime.datetime.now()
