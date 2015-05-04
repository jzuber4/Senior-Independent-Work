""" Quiz service

This module contains a set of functions that allow a client
to call the SOAP service providing information on quizzes,
questions, and more. Contains Classes specifying types
of quizzes and questions, as well as functions that allow
the type of a Quiz or Question to be determined.

Attributes:
    service: Contains the (suds) SOAP service at the endpoint
        defined by QUIZ_SERVICE_URL in settings.
    DEBUG: If true, catch errors on SOAP service calls and
        return a value from a debugging function

"""
from functools import wraps
import json
import debug_data
import suds

service = None
DEBUG = False

class DebugWrapper(object):
    """ Decorator that calls a debug function if the decorated function fails

    Construct a decorator whose debug function is set to the first argument.
    source on decorators: http://stackoverflow.com/a/5929178

    Args:
        debug_function (Callable): Function to be called if the decorated function fails

    Returns:
        A function decorator
    """
    def __init__(self, debug_function):
        self.debug_function = debug_function
    def __call__(self, f):
        """ Apply the decorator to the function, calling a debug function on failure.

        Wrap the decorated function in try/except, if there is an error and DEBUG
        is set to True, this will print the error message and call the debug function.
        If DEBUG is false, this decorator does nothing and re-raises the error.

        Args:
            f (Callable): Function that is decorated

        Returns:
            The result of the function f, or, if there is an error
            and DEBUG is True, the result of the debug function

        Raises:
            If DEBUG is False, this will raise any error that f does.
        """
        decorator_self = self
        # preserve this.__name__ etc.
        @wraps(f)
        def wrappee(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if DEBUG:
                    print("Error occurred while executing {} in quiz service: {}".format(f.__name__, e))
                    return decorator_self.debug_function()
                else:
                    raise
        return wrappee

class NotFound(Exception):
    pass

class NoAttemptsLeft(Exception):
    pass

def custom_errors(f):
        @wraps(f)
        def wrappee(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except suds.WebFault as e:
                # errors are formatted like:
                # "'java.lang.RuntimeException: JSON_MESSAGE'"
                # have to drop first and last characters (they are single-quotes)
                try:
                    error = json.loads(str(e)[1:-1].split("java.lang.RuntimeException: ")[1])
                except:
                    raise e
                print(error)
                if "code" in error and error["code"] == "NOT_FOUND":
                    # if some resource isn't found, return this exception
                    raise NotFound("Not found")
                elif "code" in error and error["code"] == "NO_ATTEMPTS_LEFT":
                    # if a question is attempted too many times, return this
                    raise NoAttemptsLeft("No attempts left")
                raise e
        return wrappee

@DebugWrapper(debug_data.is_admin)
def is_admin(username):
    """ Return whether the user with name username is a admin/teacher.

    This is not the same as the admin of the Django server, it means
    the user is an admin as determined by the service connected to
    over SOAP. These admins are teachers that have access to enhanced
    functionality, such as the creation and management of quizzes.

    Args:
        username (string): username of user whose admin/teacher status is returned

    Returns:
        bool: whether or not the user is an admin/teacher
    """
    return service.isAdmin(username)

@custom_errors
def get_admin_quiz_info(quiz_id):
    return json.loads(service.getAdminQuizInfo(quiz_id))

def get_admin_courses(username):
    return json.loads(service.getAdminCourses(username))

def make_quiz(quiz, questions):
    service.makeQuiz(quiz, questions)

def edit_quiz(quiz, questions):
    service.editQuiz(quiz, questions)

def delete_quiz(quiz_id):
    service.deleteQuiz(quiz_id)

@DebugWrapper(debug_data.get_user_courses)
def get_user_courses(username):
    """ Get the courses for a user.

    Returns a python dictionary whose keys are
    ids and values are the titles of the classes correponding
    to the ids.

    Example:


    """
    return json.loads(service.getUserCourses(username))

@DebugWrapper(debug_data.get_course_quizzes)
@custom_errors
def get_course_quizzes(username, course_id):
    return json.loads(service.getCourseQuizzes(username, course_id))

@DebugWrapper(debug_data.select_quiz)
def select_quiz(username, quiz_id):
    service.selectQuiz(username, quiz_id)

@DebugWrapper(debug_data.get_quiz_info)
@custom_errors
def get_quiz_info(username, quiz_id):
    return json.loads(service.getQuizInfo(username, quiz_id))

def get_quiz_statistics(quiz_id):
    return json.loads(service.getQuizStatistics(quiz_id))

@DebugWrapper(debug_data.get_exercise)
@custom_errors
def get_exercise(username, quiz_id, question_idx):
    return json.loads(service.getExercise(username, quiz_id, question_idx))

@DebugWrapper(debug_data.get_result)
@custom_errors
def get_result(username, quiz_id, question_idx, user_answer):
    return json.loads(service.getResult(username, quiz_id, question_idx, user_answer))

@DebugWrapper(debug_data.get_attempt_info)
@custom_errors
def get_attempt_info(username, quiz_id, question_idx, attempt_idx):
    return json.loads(service.getAttemptInfo(username, quiz_id, question_idx, attempt_idx))

@DebugWrapper(debug_data.get_question_types)
def get_question_types():
    return json.loads(service.getQuestionTypes())

def get_grading_types():
    return json.loads(service.getGradingTypes())

class QuizStatus:
    BEFORE_START_DATE = "QUIZ_STATUS_BEFORE_START_DATE"
    STARTED           = "QUIZ_STATUS_STARTED"
    NOT_STARTED       = "QUIZ_STATUS_NOT_STARTED"
    EXPIRED           = "QUIZ_STATUS_EXPIRED"
    OVER              = "QUIZ_STATUS_OVER"
    AFTER_END_DATE    = "QUIZ_STATUS_AFTER_END_DATE"

def get_quiz_status(quiz):
    if   quiz["status"] == "BEFORE_START_DATE":
        return QuizStatus.BEFORE_START_DATE
    elif quiz["status"] == "STARTED":
        return QuizStatus.STARTED
    elif quiz["status"] == "NOT_STARTED":
        return QuizStatus.NOT_STARTED
    elif quiz["status"] == "EXPIRED":
        return QuizStatus.EXPIRED
    elif quiz["status"] == "OVER":
        return QuizStatus.OVER
    elif quiz["status"] == "AFTER_END_DATE":
        return QuizStatus.NOT_STARTED

class ResultStatus:
    FINISHED  = "RESULT_STATUS_FINISHED"
    TIMED_OUT = "RESULT_STATUS_TIMED_OUT"
    OTHER     = "RESULT_STATUS_OTHER"

def get_result_status(result):
    if   result["status"] == "FINISHED":
        return ResultStatus.FINISHED
    elif result["status"] == "TIMED_OUT":
        return ResultStatus.TIMED_OUT
    else:
        return ResultStatus.OTHER

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

