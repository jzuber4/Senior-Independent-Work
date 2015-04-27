from django.db import models

# Course saves titles for course ids
class Course(models.Model):
    service_id = models.IntegerField()
    title = models.TextField()

# Quiz saves titles for quiz ids
class Quiz(models.Model):
    service_id = models.IntegerField()
    title = models.TextField()
