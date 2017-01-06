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
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", foreign_keys=[sender_id])

    def __init__(self, text, match_id, sender_id):
        self.text = text
        self.timestamp = datetime.datetime.now()
        self.match_id = match_id
        self.sender_id = sender_id
