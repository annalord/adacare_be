from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import NoteSerializer, UserSerializer, DailyTaskSerializer, MedicationSerializer, EventSerializer
from .models import Note, DailyTask, Medication, Event
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib import auth
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

# USER HOUSEKEEPING

@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']

        if User.objects.filter(username=username).exists():
            return Response({ 'error': 'username taken' })
        else:
            user = User.objects.create_user(username=username, password=password)

            user = User.objects.get(id=user.id)

            return Response({ 'success': 'user created' })

@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return Response({ 'success': 'logged in' })
        else:
            return Response({ 'error': 'unable to log in' })

class LogoutView(APIView):
    def post(self, request, format=None):
        auth.logout(request)
        return Response({ 'success': 'logged out' })

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({ 'success': 'CSRF token created' })

# GET RID OF THIS BEFORE DEPLOYMENT - SHOWS ALL USER DATA 
class GetUsersView(APIView):
    permission_classes = (permissions.AllowAny, )  

    def get(self):
        users = User.objects.all()

        users = UserSerializer(users, many=True)
        return Response(users.data)


# MODEL VIEWS

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get_queryset(self): 
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set

class DailyTaskViewSet(viewsets.ModelViewSet):
    serializer_class = DailyTaskSerializer
    queryset = DailyTask.objects.all()

    def get_queryset(self): 
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set

class MedicationViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()

    def get_queryset(self): 
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set

class EventViewSet(viewsets.ModelViewSet):
    serializer_class =EventSerializer
    queryset = Event.objects.all()

    def get_queryset(self): 
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set
