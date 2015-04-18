from django.db import models

# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=200)
    num_answered = models.IntegerField(default=0.0)
    num_questions = models.IntegerField()
    status = models.CharField(max_length=200)
    score = models.FloatField(default=0.0)
    max_score = models.FloatField()

class Question(models.Model):
    # type of question
    q_type = models.CharField(max_length=200)
    # index in quiz
    idx = models.IntegerField()
    # current score of question
    score = models.FloatField(default=0.0)
    # maximum score for that question
    max_score = models.FloatField(default=10.0)
    # attempts used
    attempts = models.IntegerField(default=0)
    # answered
    answered = models.BooleanField(default=False)
    # number of possible attempts
    max_attempts = models.IntegerField(default=4)
    # is there an instance currently in progress (may have timed out)
    in_progress = models.BooleanField(default=False)
    # quiz to which the question belongs
    quiz = models.ForeignKey(Quiz)

class QuestionInstance(models.Model):
    # text for prompt
    prompt = models.CharField(max_length=200)
    # json of structured data for question
    structure = models.TextField()
    # json of answer
    answer = models.TextField()
    # json of user_answer
    user_answer = models.TextField(default="")
    # whether the user got it right
    correct = models.NullBooleanField()
    # number of attempt
    idx = models.IntegerField()
    # current score of question
    score = models.FloatField(default=0.0)
    # starting time of question
    start_time = models.DateTimeField(auto_now_add=True)
    # time by which the question must be answered
    end_time = models.DateTimeField()
    # whether the question has been answered yet
    complete = models.BooleanField(default=False)
    # question to which the instance belongs
    question = models.ForeignKey(Question)



