from rest_framework import serializers
from .models import Note, DailyTask
from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
      model = User 
      fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Note
        fields = '__all__'

class DailyTaskSerializer(serializers.ModelSerializer):
    class Meta: 
        model = DailyTask
        fields = '__all__'