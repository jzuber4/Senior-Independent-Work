from django.db import models

# Create your models here.

class Question(models.Model):
    # text for prompt
    prompt = models.CharField(max_length=200)
    # json of structured data for question
    structure = models.TextField()
    # json of answer
    answer = models.TextField()

    @classmethod
    def create(cls, prompt, structure, answer):
        book = cls(prompt=prompt, structure=structure, answer=answer)
        return book
