from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Note(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    author = models.CharField(max_length=20)
    message = models.TextField()
    date_time_created = models.DateTimeField(auto_now_add=True)


class DailyTask(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    task = models.CharField(max_length=50)
    time = models.TimeField(null=True) #10:30


class Medication(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    med_name = models.CharField(max_length=25)
    dosage = models.CharField(max_length=50)
    time = models.TimeField(null=True)
    notes = models.CharField(max_length=200)
    refill_date = models.DateField(null=True) #YYYY-MM-DD
    is_prescription = models.BooleanField()


class Event(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    details = models.TextField()
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    all_day = models.BooleanField(default=False) 
