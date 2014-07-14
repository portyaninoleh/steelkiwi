from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from signals import notify_author


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


post_save.connect(notify_author, sender=Response)