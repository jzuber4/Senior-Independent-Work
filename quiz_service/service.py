import json
import debug_data

class Client:
    s = None
    debug = False

def is_admin(username):
    # for now, everyone is a star
    return True

def get_question_types():
    return [
        ["BLAType", "BLATitle"],
        ["FOOType", "FOOTitle"],
        ["BAZType", "BAZTitle"],
        ["BARType", "BARTitle"],
    ]

def get_grading_types():
    return ["best", "average"]

def get_quizzes():
    try:
        result = Client.s.getQuizzes()
    except Exception as e:
        if Client.debug:
            print("ERROR OCCURED IN QUIZ_SERVICE: {}".format(e))
            return debug_data.get_quizzes()
        else:
            raise
    return json.loads(result)

def get_quiz_info(user_id, quiz_id):
    result = Client.s.getQuizInfo(user_id, quiz_id)
    return json.loads(result)

def select_quiz(user_id, quiz_id):
    Client.s.selectQuiz(user_id, quiz_id)

def get_exercise(user_id, quiz_id, question_idx):
    try:
        result = Client.s.getExercise(user_id, quiz_id, question_idx)
    except Exception as e:
        if Client.debug:
            print("ERROR OCCURED IN QUIZ_SERVICE: {}".format(e))
            return debug_data.get_exercise()
        else:
            raise
    return json.loads(result)

def get_result(user_id, quiz_id, question_idx, user_answer):
    try:
        result = Client.s.getResult(user_id, quiz_id, question_idx, user_answer)
    except Exception as e:
        if Client.debug:
            print("ERROR OCCURED IN QUIZ_SERVICE: {}".format(e))
            return debug_data.get_result()
        else:
            raise
    return json.loads(result)

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

