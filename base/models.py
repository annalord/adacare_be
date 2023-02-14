from django.db import models
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
    completed = models.BooleanField(default=False)

class Medication(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    med_name = models.CharField(max_length=25)
    dosage = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    notes = models.CharField(max_length=200, null=True, blank=True)
    refill_date = models.CharField(max_length=25, null=True, blank=True) 
    is_prescription = models.BooleanField()

class Event(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    details = models.TextField(null=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    all_day = models.BooleanField(default=False) 
    completed = models.BooleanField(default=False)

