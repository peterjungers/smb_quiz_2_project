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


# If route is manually typed, sent back to index (make it go to level 1? but can't make work). Now it just goes to 404:
@main.route("/quiz")
def testing():
    return render_template("index.html")


@main.route("/quiz/<level_num>")
def quiz(level_num):
    """ To do:
    Read more about calling functions, variable placement above, etc.
    Shadowing variable names within functions as shown by intellisense.
    Functions within functions—seems hard to read.

    Make comments.
    """
    def get_questions(level_num):
        questions = db.session.execute(
                    select(Question)
                    .filter(Question.level == level_num)
                    ).all()
        random.shuffle(questions)
        questions = questions[0:5]

        return questions

    def get_elements(quiz_questions):
        correct_answers = []
        for q in quiz_questions:
            correct = q.Question.answer
            correct_answers.append(correct)

        quiz = []
        num = 1
        for q in quiz_questions:
            answer_options = [
                q.Question.answer,
                q.Question.wrong_answer_1,
                q.Question.wrong_answer_2
            ]
            random.shuffle(answer_options)

            num_question_options = (num,
                                    q.Question.question,
                                    answer_options)
            quiz.append(num_question_options)

            num += 1

        return correct_answers, quiz

    def encrypt_answers(correct_answers):
        """ """

        def get_key(coded_answer):
            key = str(len(coded_answer))
            # This is so I know all keys are two digits:
            if int(key) < 10:
                two_digit_key = "0" + key
            else:
                two_digit_key = key
            coded_answer = coded_answer + two_digit_key

            return coded_answer

        def get_random_characters(amount):
            # Help from https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
            random_string = "".join(random.choices(
                            string.ascii_uppercase
                            + string.ascii_lowercase
                            + string.digits
                            + string.punctuation,
                            k=amount)
                            )
            return random_string

        def create_coded_answers(correct_answers):
            coded_answers = []
            for answer in correct_answers:
                coded_answer = ""
                for letter in answer:
                    letter = chr(ord(letter) + 5)
                    coded_answer += letter

                get_key(coded_answer)

                # Make all coded answers have length of 200 characters:
                while len(coded_answer) < 200:
                    random_char = get_random_characters(1)
                    coded_answer = random_char + coded_answer

                # Append 200 more random characters at end of coded answer:
                coded_answer = coded_answer + get_random_characters(200)
                coded_answers.append(coded_answer)

            return coded_answers

        coded_answers = create_coded_answers(correct_answers)
        return coded_answers

    quiz_questions = get_questions(level_num)
    correct_answers, quiz = get_elements(quiz_questions)
    coded_answers = encrypt_answers(correct_answers)

    # score = 100

    return render_template("quiz.html",
                           quiz=quiz,
                           level_num=level_num,
                           array=coded_answers)
