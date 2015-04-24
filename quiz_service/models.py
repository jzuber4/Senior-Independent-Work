from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User)
    is_teacher = models.BooleanField(default=False)
