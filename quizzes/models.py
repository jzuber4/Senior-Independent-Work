from django.db import models

# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=200)
    num_questions = models.IntegerField()
    status = models.CharField(max_length=200)
    score = models.FloatField(default=0.0)
    max_score = models.FloatField()

class Question(models.Model):
    # type of question
    q_type = models.CharField(max_length=200)
    # index in quiz
    idx = models.IntegerField()
    # quiz to which the question belongs
    quiz = models.ForeignKey(Quiz)

class QuestionInstance(models.Model):
    # text for prompt
    prompt = models.CharField(max_length=200)
    # json of structured data for question
    structure = models.TextField()
    # json of answer
    answer = models.TextField()
    # number of attempt
    idx = models.IntegerField()
    question = models.ForeignKey(Question)



