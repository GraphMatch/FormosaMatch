# question.py


from app import db, bcrypt

class Question(db.Model):

    __tablename__ = "user_questions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(50), unique=True, nullable=False)
    selected_question_id = db.Column(db.Integer, db.ForeignKey('question_list.id'), nullable=True)
    selected_question = db.relationship("QuestionList")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="questions")

    def __init__(self, user_id, selected_id = None, text = None):
        self.user_id = user_id
        self.selected_id = selected_id
        self.text = text
