import json
import os
import random

def get_quizzes():
    return [
            {"quizId": 1, "quizTitle": "Fake Quiz 1", "numQuestions":5, "startDate":"2015-08-07 13:13:13", "endDate":"2015-08-07 13:50:00"},
            {"quizId": 2, "quizTitle": "Fake Quiz 2", "numQuestions":5, "startDate":"2015-08-07 13:13:13", "endDate":"2015-08-07 13:50:00"},
            {"quizId": 3, "quizTitle": "Fake Quiz 3", "numQuestions":5, "startDate":"2015-08-07 13:13:13", "endDate":"2015-08-07 13:50:00"},
            {"quizId": 4, "quizTitle": "Fake Quiz 4", "numQuestions":5, "startDate":"2015-08-07 13:13:13", "endDate":"2015-08-07 13:50:00"},
            {"quizId": 5, "quizTitle": "Fake Quiz 5", "numQuestions":5, "startDate":"2015-08-07 13:13:13", "endDate":"2015-08-07 13:50:00"},
            ]

def get_exercise():
    # exercises contains, in order:
    # BST_INSERT exercise
    # BST_SEARCH exercise
    # CHECKBOX exercise
    # MATCHING exercise
    # RADIO exercise
    # SHORT_ANSWER exercise
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    exercises = [json.loads(line.strip()) for line in open(os.path.join(location, 'debug_data_exercises.txt'))]
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
    results = [json.loads(line.strip()) for line in open(os.path.join(location, 'debug_data_results.txt'))]
    return random.choice(results)




