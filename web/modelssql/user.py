# user.py


import datetime
from app import db, bcrypt
from datetime import date
from modelssql.question import Question
from modelssql.match import Match

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fullname = db.Column(db.String(255), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    birth_date = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    questions = db.relationship("Question", back_populates="user")
    #matches_a = db.relationship("Match", back_populates="user_b")
    #matches_b = db.relationship("Match", back_populates="user_a")

    def __init__(self, preference, gender, birth_date, country, city, email, username, password, admin=False):
        self.preference = preference
        self.gender = gender
        self.birth_date = birth_date
        self.country = country
        self.city = city
        self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)

    def calculate_age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
