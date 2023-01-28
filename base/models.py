from django.db import models

class User(models.Model):
  username = models.CharField
  password = models.CharField
  first_name = models.CharField

class Note(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  message = models.CharField
  date_time_created = models.DateTimeField(auto_now_add=True)



