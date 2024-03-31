from flask import current_app
from smb_quiz_2 import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(), nullable=False)
    answer = db.Column(db.String(), nullable=False)
    wrong_answer_1 = db.Column(db.String(), nullable=False)
    wrong_answer_2 = db.Column(db.String(), nullable=False)
    level = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return (f"""
                Row:
                id = {self.id}
                question = {self.question}
                answer = {self.answer}
                wrong_answer_1 = {self.wrong_answer_1}
                wrong_answer_2 = {self.wrong_answer_2}
                level = {self.level}
                """)
