import random
from flask import Blueprint, render_template
from sqlalchemy import select

from smb_quiz_2 import db
from smb_quiz_2.models import Question


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/quiz")
def quiz():
    # Establish list of unique numeric values:
    values = []
    while len(values) < 10:
        v = random.randrange(1, 21)
        if v not in values:
            values.append(v)

    print(values)

    # Query database using those unique values as primary key value:
    # question_objects = []
    question_objects = db.session.execute(
                select(Question)
                .filter(Question.id.in_(values)))
    # question_objects.append(question)

    # Query database using those unique values as primary key value:
    question_objects = []
    for v in values:
        question = db.session.execute(
                select(Question)
                .filter(Question.id == v))
        # print(question)
        question_objects.append(question)
    # print(question_objects)
    # for q_o in question_objects:
    #     for row in q_o:
    #         print(row.Question.id)

    # for q_o in question_objects:
    #     print(q_o.Question)
        # for row in q_o:
        #     print(row.Question.id)

    # Separate each Question object so answers can be shuffled:
    num = 1
    quiz_questions = []
    correct_answers = []
    for q_o in question_objects:
        for row in q_o:
            correct = row.Question.answer
            correct_answers.append(correct)
            answer_options = [
                row.Question.answer, row.Question.wrong_answer_1, row.Question.wrong_answer_2
            ]
            random.shuffle(answer_options)
            # Question number, question, question's three answer options:
            num_question_options = num, row.Question.question, answer_options
            quiz_questions.append(num_question_options)
            num +=1

    for q in quiz_questions:
        print(q[0])
    # print(correct_answers)

    # Silly little encryption so correct answers
    # aren't readily visible in dev tools :)
    coded_answers = []
    for answer in correct_answers:
        coded_answer = ""
        for letter in answer:
            letter = chr(ord(letter) + 5)
            coded_answer += letter
        coded_answers.append(coded_answer)

    return render_template("quiz.html",
                           quiz_questions=quiz_questions,
                           array=coded_answers)
