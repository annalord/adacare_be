from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Note(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    date_time_created = models.DateTimeField(auto_now_add=True)

class DailyTask(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    task = models.TextField()
    time = models.TimeField(null=True) #10:30

