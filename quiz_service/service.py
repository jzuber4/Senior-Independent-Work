from functools import wraps
import json
import debug_data

class Client:
    s = None
    debug = False

# source: http://stackoverflow.com/a/5929178
# decorator which specifies an alternate function to call on error
# used for testing when service is not available
class DebugWrapper(object):
    def __init__(self, debug_function):
        self.debug_function = debug_function
    def __call__(self, f):
        decorator_self = self
        @wraps(f)
        def wrappee(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if Client.debug:
                    print("Error occurred while executing {} in quiz service: {}".format(f.__name__, e))
                    return decorator_self.debug_function()
                else:
                    raise
        return wrappee

@DebugWrapper(debug_data.is_admin)
def is_admin(username):
    return Client.s.isAdmin(username)

@DebugWrapper(debug_data.get_user_courses)
def get_user_courses(username):
    return json.loads(Client.s.getUserCourses(username))

@DebugWrapper(debug_data.get_course_quizzes)
def get_course_quizzes(username, course_id):
    return json.loads(Client.s.getCourseQuizzes(username, course_id))

@DebugWrapper(debug_data.select_quiz)
def select_quiz(username, quiz_id):
    Client.s.selectQuiz(username, quiz_id)

@DebugWrapper(debug_data.get_quiz_info)
def get_quiz_info(username, quiz_id):
    return json.loads(Client.s.getQuizInfo(username, quiz_id))

def get_quiz_statistics(quiz_id):
    return json.loads(Client.s.getQuizStatistics(quiz_id))

@DebugWrapper(debug_data.get_exercise)
def get_exercise(username, quiz_id, question_idx):
    return json.loads(Client.s.getExercise(username, quiz_id, question_idx))

@DebugWrapper(debug_data.get_result)
def get_result(username, quiz_id, question_idx, user_answer):
    return json.loads(Client.s.getResult(username, quiz_id, question_idx, user_answer))

@DebugWrapper(debug_data.get_attempt_info)
def get_attempt_info(username, quiz_id, question_idx, attempt_idx):
    return json.loads(Client.s.getAttemptInfo(username, quiz_id, question_idx, attempt_idx))

def get_question_types():
    return [
        ["BLAType", "BLATitle"],
        ["FOOType", "FOOTitle"],
        ["BAZType", "BAZTitle"],
        ["BARType", "BARTitle"],
    ]

def get_grading_types():
    return ["best", "average"]

class QuizStatus:
    STARTED     = "QUIZ_STATUS_STARTED"
    NOT_STARTED = "QUIZ_STATUS_NOT_STARTED"
    OTHER       = "QUIZ_STATUS_OTHER"

def get_quiz_status(quiz):
    if   quiz["status"] == "STARTED":
        return QuizStatus.STARTED
    elif quiz["status"] == "NOT_STARTED":
        return QuizStatus.NOT_STARTED
    else:
        return QuizStatus.OTHER

class QuestionType:
    BST_INSERT   = "QUESTION_TYPE_BST_INSERT"
    BST_SEARCH   = "QUESTION_TYPE_BST_SEARCH"
    CHECKBOX     = "QUESTION_TYPE_CHECKBOX"
    MATCHING     = "QUESTION_TYPE_MATCHING"
    NUMERIC      = "QUESTION_TYPE_NUMERIC"
    RADIO        = "QUESTION_TYPE_RADIO"
    SHORT_ANSWER = "QUESTION_TYPE_SHORT_ANSWER"
    OTHER        = "QUESTION_TYPE_OTHER"

def get_question_type(question):
    if question["type"] == "SHORTANSWER":
        # certain questions have special handling / pretty display
        if question["referenceNum"] == 1:
            return QuestionType.BST_INSERT
        elif question["referenceNum"] == 2:
            return QuestionType.BST_SEARCH
        else:
            return QuestionType.SHORT_ANSWER
    elif question["type"] == "CHECKBOX":
        return QuestionType.CHECKBOX
    elif question["type"] == "MATCHING":
        return QuestionType.MATCHING
    elif question["type"] == "NUMERIC":
        return QuestionType.NUMERIC
    elif question["type"] == "RADIO":
        return QuestionType.RADIO
    elif question["type"] == "REGEXP":
        # handle regexp questions the same as short answer
        return QuestionType.SHORT_ANSWER
    elif question["type"] == "VECTOR":
        # handle vector questions the same as short answer
        return QuestionType.SHORT_ANSWER
    else:
        return QuestionType.OTHER

