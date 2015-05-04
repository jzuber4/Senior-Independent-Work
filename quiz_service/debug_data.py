import json
import os
import random

# This file provides debugging functions to be called when functions
# in service.py fail and QUIZ_SERVICE_DEBUG = True
# They can be used to test / develop the site in the absence of
# a SOAP connection or when the SOAP service is unavailable or broken

# path of directory containing this file
location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
# function to read json from file with name filename
def read_json_from_file(filename):
    return json.loads("".join([line.strip() for line in open(os.path.join(location, filename))]))

# Always returns True so that admin functionality can be tested
def is_admin():
    return True

# No need to select quiz
def select_quiz():
    return

# Return the attempt stored in debug_data_attempt_info.txt
def get_attempt_info():
    return read_json_from_file('debug_data_attempt_info.txt')

# Return the data stored in debug_data_user_courses.txt
def get_user_courses():
    return read_json_from_file('debug_data_user_courses.txt')

# Return the data stored in debug_data_course_quizzes.txt
def get_course_quizzes():
    return read_json_from_file('debug_data_course_quizzes.txt')

# Return the data stored in debug_data_quiz_info.txt
def get_quiz_info():
    return read_json_from_file('debug_data_quiz_info.txt')

# Return the data stored in debug_data_question_types.txt
def get_question_types():
    return read_json_from_file('debug_data_question_types.txt')

# Return the data stored in debug_data_grading_types.txt
def get_grading_types():
    return read_json_from_file('debug_data_grading_types.txt')

# return a random type of exercise
def get_exercise():
    # exercises contains, in order:
    # BST_INSERT exercise
    # BST_SEARCH exercise
    # CHECKBOX exercise
    # MATCHING exercise
    # RADIO exercise
    # SHORT_ANSWER exercise
    exercises = read_json_from_file('debug_data_exercises.txt')
    return random.choice(exercises)

# return a random result
def get_result():
    # results contains, in order:
    # BST_INSERT result
    # BST_SEARCH result
    # CHECKBOX result
    # MATCHING result
    # RADIO result
    # SHORT_ANSWER result
    results = read_json_from_file('debug_data_results.txt')
    return random.choice(results)
