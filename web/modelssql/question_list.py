# question_list.py


from app import db, bcrypt

class QuestionList(db.Model):

    __tablename__ = "question_list"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, text):
        self.text = text
