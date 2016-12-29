# message.py

import datetime
from app import db, bcrypt

class Message(db.Model):

    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    match = db.relationship("Match", back_populates="messages")

    def __init__(self, text):
        self.text = text
        self.timestamp = datetime.datetime.now()
