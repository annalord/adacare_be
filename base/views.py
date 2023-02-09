from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import NoteSerializer, UserSerializer, DailyTaskSerializer, MedicationSerializer, EventSerializer
from .models import Note, DailyTask, Medication, Event
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib import auth
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.views.decorators.csrf import requires_csrf_token

# USER HOUSEKEEPING

from django.http import JsonResponse
from django.middleware.csrf import get_token

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

def ping(request):
    return JsonResponse({'result': 'OK'})


@method_decorator(csrf_exempt, name='dispatch') #exempt not protect 
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']
        pw_repeat = data['pw_repeat']
        first_name = data['first_name']

        if User.objects.filter(username=username).exists():
            print('UN TAKEN')
            return Response({'error': 'Sorry, that username is taken'})
        elif password != pw_repeat:
            print('PW DONTMATCH')
            return Response({'error': 'passwords do not match'})
        else:
            user = User.objects.create_user(username=username, password=password, first_name=first_name)

            user = User.objects.get(id=user.id)

            return Response({ 'success': 'user created' })

@method_decorator(ensure_csrf_cookie, name='dispatch') #exempt or protect?? 
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return Response({ 'success': 'logged in', 'user_id': user.id, 'user_name': user.first_name })
        else:
            return Response({ 'error': 'unable to log in' })

# @method_decorator(csrf_protect, name='dispatch') #exempt or protect 

class LogoutView(APIView):
    # @csrf_exempt
    permission_classes = (permissions.AllowAny, )
    # @requires_csrf_token
    def post(self, request, format=None):
        print('inside logout post')
        print(request)
        auth.logout(request)
        return Response({ 'success': 'logged out' })

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({ 'success': 'CSRF token created' })

# # GET RID OF THIS BEFORE DEPLOYMENT - SHOWS ALL USER DATA 
# class GetUsersView(APIView):
#     permission_classes = (permissions.AllowAny, )  

#     def get(self):
#         users = User.objects.all()

#         users = UserSerializer(users, many=True)
#         return Response(users.data)


class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated

            if isAuthenticated:
                return Response({ 'isAuthenticated': 'success' })
            else:
                return Response({ 'isAuthenticated': 'error' })
        except:
            return Response({ 'error': 'Something went wrong when checking authentication status' })


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
