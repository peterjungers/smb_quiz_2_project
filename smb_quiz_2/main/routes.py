import random
from flask import Blueprint, render_template
# from smb_quiz_2.models import Question


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/quiz")
def quiz():
    # Establish list of unique numeric values:
    # values = []
    # while len(values) < 10:
    #     v = random.randrange(1, 51)
    #     if v not in values:
    #         values.append(v)
    #
    # # Query database using those unique values as primary key value:
    # question_objects = []
    # for v in values:
    #     question = Question.objects.get(pk=v)
    #     question_objects.append(question)
    #
    # # Separate each Question object so answers can be shuffled:
    # num = 1
    # quiz_questions = []
    # correct_answers = []
    # for q in question_objects:
    #     correct = q.answer
    #     correct_answers.append(correct)
    #     answer_options = [
    #         q.answer, q.wrong_answer_1, q.wrong_answer_2
    #     ]
    #     random.shuffle(answer_options)
    #     # Question number, question, question's three answer options:
    #     num_question_options = num, q.question, answer_options
    #     quiz_questions.append(num_question_options)
    #     num +=1
    #
    # # Silly little encryption so correct answers
    # # aren't readily visible in dev tools :)
    # coded_answers = []
    # for answer in correct_answers:
    #     coded_answer = ""
    #     for letter in answer:
    #         letter = chr(ord(letter) + 5)
    #         coded_answer += letter
    #     coded_answers.append(coded_answer)

    return render_template("quiz.html", array=["aaaaa","bbbbb","ccccc","ddddd","eeeee","fffff","ggggg","hhhhh","iiiii","jjjjj"])
