from django.db import models
from django.contrib.auth.models import User

# UserInfo saves teacher status for users
class UserInfo(models.Model):
    user = models.OneToOneField(User)
    is_teacher = models.BooleanField(default=False)

# Course saves titles for course ids
class Course(models.Model):
    service_id = models.IntegerField()
    title = models.TextField()

# Quiz saves titles for quiz ids
class Quiz(models.Model):
    service_id = models.IntegerField()
    title = models.TextField()
