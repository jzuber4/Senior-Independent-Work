import json
import os
import random

def is_admin():
    return True

def select_quiz():
    return

def get_attempt_info():
    filename = 'debug_data_attempt_info.txt'
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return json.loads("".join([line.strip() for line in open(os.path.join(location, filename))]))

def get_user_courses():
    filename = 'debug_data_user_courses.txt'
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return json.loads("".join([line.strip() for line in open(os.path.join(location, filename))]))

def get_course_quizzes():
    filename = 'debug_data_course_quizzes.txt'
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return json.loads("".join([line.strip() for line in open(os.path.join(location, filename))]))

def get_quiz_info():
    filename = 'debug_data_quiz_info.txt'
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return json.loads("".join([line.strip() for line in open(os.path.join(location, filename))]))

def get_exercise():
    # exercises contains, in order:
    # BST_INSERT exercise
    # BST_SEARCH exercise
    # CHECKBOX exercise
    # MATCHING exercise
    # RADIO exercise
    # SHORT_ANSWER exercise
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    filename = 'debug_data_exercises.txt'
    exercises = [json.loads(line.strip()) for line in open(os.path.join(location, filename))]
    return random.choice(exercises)

def get_result():
    # results contains, in order:
    # BST_INSERT result
    # BST_SEARCH result
    # CHECKBOX result
    # MATCHING result
    # RADIO result
    # SHORT_ANSWER result
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    filename = 'debug_data_results.txt'
    results = [json.loads(line.strip()) for line in open(os.path.join(location, filename))]
    return random.choice(results)




