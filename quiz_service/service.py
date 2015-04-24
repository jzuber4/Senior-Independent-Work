import json

class Client:
    s = None
    debug = False

def get_quizzes():
    try:
        result = Client.s.getQuizzes()
        return json.loads(result)
    except Exception as e:
        if Client.debug:
            print("ERROR OCCURED IN QUIZ_SERVICE: {}".format(e))
            return [
                {"quizId": 1, "quizTitle": "Fake Quiz 1", "numQuestions":5, "startDate":"2015-08-07 13:13:13", "endDate":"2015-08-07 13:50:00"},
                {"quizId": 2, "quizTitle": "Fake Quiz 2", "numQuestions":5, "startDate":"2015-08-07 13:13:13", "endDate":"2015-08-07 13:50:00"},
                {"quizId": 3, "quizTitle": "Fake Quiz 3", "numQuestions":5, "startDate":"2015-08-07 13:13:13", "endDate":"2015-08-07 13:50:00"},
                {"quizId": 4, "quizTitle": "Fake Quiz 4", "numQuestions":5, "startDate":"2015-08-07 13:13:13", "endDate":"2015-08-07 13:50:00"},
                {"quizId": 5, "quizTitle": "Fake Quiz 5", "numQuestions":5, "startDate":"2015-08-07 13:13:13", "endDate":"2015-08-07 13:50:00"},
            ]
        else:
            raise

def get_quiz_info(user_id, quiz_id):
    result = Client.s.getQuizInfo(user_id, quiz_id)
    return json.loads(result)

def select_quiz(user_id, quiz_id):
    result = Client.s.selectQuiz(user_id, quiz_id)
    return json.loads(result)

def get_exercise(user_id, quiz_id, question_idx):
    try:
        result = Client.s.getExercise(user_id, quiz_id, question_idx)
        return json.loads(result)
    except Exception as e:
        if Client.debug:
            print("ERROR OCCURED IN QUIZ_SERVICE: {}".format(e))
            return {u'prompt': u'Given a BST whose level-order traversal is:\n\n    18 15 76 32 98 61 84 42 54 43 \n\nSuppose that you search for the key 97. What is the sequence of keys\nin the BST that are compared with 97 during the search miss?', u'title': u'FAKE QUESTION: Binary Search Tree Search', u'promptPrettyStructure': u'{"name":"18","children":[{"name":"15","children":[{"name":"","children":[]},{"name":"","children":[]}]},{"name":"76","children":[{"name":"32","children":[{"name":"","children":[]},{"name":"61","children":[{"name":"42","children":[{"name":"","children":[]},{"name":"54","children":[{"name":"43","children":[{"name":"","children":[]},{"name":"","children":[]}]},{"name":"","children":[]}]}]},{"name":"","children":[]}]}]},{"name":"98","children":[{"name":"84","children":[{"name":"","children":[]},{"name":"","children":[]}]},{"name":"","children":[]}]}]}]}', u'promptPretty': u'Given a BST whose level-order traversal is:\n\n    18 15 76 32 98 61 84 42 54 43 \n\nSuppose that you search for the key 97. What is the sequence of keys\nin the BST that are compared with 97 during the search miss?', u'seed': 200181, u'referenceNum': 2, u'type': u'SHORTANSWER'}
        else:
            raise

def get_result(user_id, quiz_id, question_idx, user_answer):
    try:
        result = Client.s.getResult(user_id, quiz_id, question_idx, user_answer)
        return json.loads(result)
    except Exception as e:
        if Client.debug:
            print("ERROR OCCURED IN QUIZ_SERVICE: {}".format(e))
            return {u'promptPretty': u'Given a BST whose level-order traversal is:\n\n    96 79 30 91 12 61 22 36 62 16 \n\nSuppose that you search for the key 33. What is the sequence of keys\nin the BST that are compared with 33 during the search miss?', u'title': u'FAKE ANSWER: Binary Search Tree Search', u'maxScore': u'5.0', u'explanation': u'', u'score': u'0.0', u'referenceNum': 2, u'promptPrettyStructure': u'{"name":"96","children":[{"name":"79","children":[{"name":"30","children":[{"name":"12","children":[{"name":"","children":[]},{"name":"22","children":[{"name":"16","children":[{"name":"","children":[]},{"name":"","children":[]}]},{"name":"","children":[]}]}]},{"name":"61","children":[{"name":"36","children":[{"name":"","children":[]},{"name":"","children":[]}]},{"name":"62","children":[{"name":"","children":[]},{"name":"","children":[]}]}]}]},{"name":"91","children":[{"name":"","children":[]},{"name":"","children":[]}]}]},{"name":"","children":[]}]}', u'type': u'SHORTANSWER', u'answer': u'96 79 30 61 36', u'prompt': u'Given a BST whose level-order traversal is:\n\n    96 79 30 91 12 61 22 36 62 16 \n\nSuppose that you search for the key 33. What is the sequence of keys\nin the BST that are compared with 33 during the search miss?', u'seed': 19986, u'userAnswer': u'96 79 61'}
        else:
            raise

class QType:
    BST_INSERT   = "Q_TYPE_BST_INSERT"
    BST_SEARCH   = "Q_TYPE_BST_SEARCH"
    CHECKBOX     = "Q_TYPE_CHECKBOX"
    MATCHING     = "Q_TYPE_MATCHING"
    RADIO        = "Q_TYPE_RADIO"
    SHORT_ANSWER = "Q_TYPE_SHORT_ANSWER"
    OTHER        = "Q_TYPE_OTHER"

def get_question_type(question):
    if question["type"] == "SHORTANSWER":
        if question["referenceNum"] == 1:
            return QType.BST_INSERT
        elif question["referenceNum"] == 2:
            return QType.BST_SEARCH
        else:
            return QType.SHORT_ANSWER
    elif question["type"] == "RADIO":
        return QType.RADIO
    elif question["type"] == "CHECKBOX":
        return QType.CHECKBOX
    elif question["type"] == "MATCHING":
        return QType.MATCHING
    else:
        return QType.OTHER

