import json

class Client:
    s = None

def get_quizzes():
    result = Client.s.getQuizzes()
    return json.loads(result)

def get_quiz_info(user_id, quiz_id):
    result = Client.s.getQuizInfo(user_id, quiz_id)
    return json.loads(result)

def select_quiz(user_id, quiz_id):
    result = Client.s.selectQuiz(user_id, quiz_id)
    return json.loads(result)

def get_exercise(user_id, quiz_id, question_idx, is_text):
    result = Client.s.getExercise(user_id, quiz_id, question_idx, is_text)
    return json.loads(result)

def get_result(user_id, quiz_id, question_idx, user_answer):
    result = Client.s.getResult(user_id, quiz_id, question_idx, user_answer)
    return json.loads(result)

class QType:
    BST_INSERT   = "Q_TYPE_BST_INSERT"
    BST_SEARCH   = "Q_TYPE_BST_SEARCH"
    SHORT_ANSWER = "Q_TYPE_SHORT_ANSWER"
    RADIO        = "Q_TYPE_RADIO"
    CHECKBOX     = "Q_TYPE_CHECKBOX"
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
    else:
        return QType.OTHER

