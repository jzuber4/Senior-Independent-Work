from django.db import models

# Create your models here.

class Question(models.Model):
    BSTINSERT = 'BI'
    BSTSEARCH = 'BS'
    Q_TYPE_CHOICES = (
        (BSTINSERT, 'BST Insert'),
        (BSTSEARCH, 'BST Search'),
    )

    # type of question displayed
    q_type = models.CharField(max_length=2,
                              choices = Q_TYPE_CHOICES,
                              default = BSTSEARCH,)

    # text for prompt
    prompt = models.CharField(max_length=200)
    # json of structured data for question
    structure = models.TextField()
    # json of answer
    answer = models.TextField()

