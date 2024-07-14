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


@main.route("/quiz")
def quiz():
    """ To do:
    Read more about calling functions, variable placement above, etc.
    Shadowing variable names within functions as shown by intellisense.
    Functions within functions—seems hard to read.

    Make comments.
    """

    def get_questions():
        levels = [1, 2, 3]
        quiz_questions = []

        for level in levels:
            questions = db.session.execute(
                        select(Question)
                        .filter(Question.level == level)
                        ).all()
            random.shuffle(questions)
            questions = questions[0:4]
            quiz_questions.append(questions)

        return quiz_questions

    def get_elements(quiz_questions):
        correct_answers = []
        for question_levels in quiz_questions:
            for q in question_levels:
                correct = q.Question.answer
                correct_answers.append(correct)

        quiz = []
        num = 1
        for question_levels in quiz_questions:
            for q in question_levels:
                answer_options = [
                    q.Question.answer,
                    q.Question.wrong_answer_1,
                    q.Question.wrong_answer_2
                ]
                random.shuffle(answer_options)

                num_ques_opt_lev = (num,
                                    q.Question.question,
                                    answer_options,
                                    q.Question.level)
                quiz.append(num_ques_opt_lev)

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

                coded_answer = get_key(coded_answer)

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

    quiz_questions = get_questions()
    correct_answers, quiz = get_elements(quiz_questions)
    coded_answers = encrypt_answers(correct_answers)

    # score = 100

    return render_template("quiz.html",
                           quiz=quiz,
                           array=coded_answers)


@main.route("/high_scores")
def high_scores():
    return render_template("high_scores.html")
