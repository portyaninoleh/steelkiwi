from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    subject = models.CharField(max_length=100)
    body = models.CharField(max_length=2000)
    user = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.now())


class Response(models.Model):
    question = models.ForeignKey(Question)
    message = models.CharField(max_length=2000)
    user = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.now())