# question.py


from app import db, bcrypt

class Question(db.Model):

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(200), nullable=False)

    def __init__(self, text):
        self.text = text
