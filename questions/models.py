from django.db import models

# Create your models here.

class Question(models.Model):
    # type of question displayed
    q_type = models.CharField(max_length=200)

    # text for prompt
    prompt = models.CharField(max_length=200)
    # json of structured data for question
    structure = models.TextField()
    # json of answer
    answer = models.TextField()

