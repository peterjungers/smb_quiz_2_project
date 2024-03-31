import random
import string

from flask import Blueprint, render_template
from sqlalchemy import select

from smb_quiz_2 import db
from smb_quiz_2.models import Question


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/quiz")  # create one route for each level instead
def quiz():
    # Establish list of unique numeric values:
    values = []
    while len(values) < 10:
        v = random.randrange(1, 21)
        if v not in values:
            values.append(v)

    # Query database using those unique values as primary key value:
    questions = []
    for v in values:
        # Query returns object consisting of a
        # question, correct answer, two wrong answers:
        q = db.session.execute(
            select(Question)
            .filter(Question.id == v)
            )
        questions.append(q)

    # Separate elements of each Question object so answers can be shuffled:
    num = 1
    quiz = []
    correct_answers = []
    for q in questions:  # For each question object in list:
        for row in q:  # For each question:
            correct = row.Question.answer
            correct_answers.append(correct)
            answer_options = [
                row.Question.answer,
                row.Question.wrong_answer_1,
                row.Question.wrong_answer_2
            ]
            random.shuffle(answer_options)
            # Question number, question, question's three answer options:
            num_question_options = (num,
                                    row.Question.question,
                                    answer_options)
            quiz.append(num_question_options)
            num += 1

    # Silly little encryption so correct answers
    # aren't readily visible in dev tools :)
    def random_characters():
        # Help from https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
        random_string = "".join(random.choices(
            string.ascii_uppercase
            + string.ascii_lowercase
            + string.digits
            + string.punctuation,
            k=200)
        )
        return random_string

    coded_answers = []
    for answer in correct_answers:
        coded_answer = ""
        for letter in answer:
            letter = chr(ord(letter) + 5)
            coded_answer += letter
        key = str(len(coded_answer))
        # This is so I know all keys are two digits:
        if int(key) < 10:
            key = "0" + key
        coded_answer = coded_answer + key

        print(key)
        print(coded_answer)

        while len(coded_answer) < 200:
            x = "".join(random.choices(
                    string.ascii_uppercase
                    + string.ascii_lowercase
                    + string.digits
                    + string.punctuation,
                    k=1))
            coded_answer = x + coded_answer
        print(coded_answer)
        coded_answer = coded_answer + random_characters()
        # print(coded_answer)
        coded_answers.append(coded_answer)
        # print(len(coded_answer))

    return render_template("quiz.html",
                           quiz=quiz,
                           array=coded_answers)
