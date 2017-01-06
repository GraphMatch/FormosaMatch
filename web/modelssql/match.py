# match.py

import datetime
from app import db, bcrypt
from modelssql.message import Message

class Match(db.Model):

    __tablename__ = "match"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_a_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_b_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, nullable=False)
    ## True is enabled, False is disabled
    status = db.Column(db.Boolean, nullable=False)
    user_a = db.relationship("User", foreign_keys=[user_a_id])
    user_b = db.relationship("User", foreign_keys=[user_b_id])
    messages = db.relationship("Message", back_populates="match")

    def __init__(self, status, user_a_id, user_b_id):
        self.status = status
        self.timestamp = datetime.datetime.now()
        self.user_a_id = user_a_id
        self.user_b_id = user_b_id
