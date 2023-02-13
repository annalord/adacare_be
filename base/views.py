from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .serializers import NoteSerializer, DailyTaskSerializer, MedicationSerializer, EventSerializer
from .models import Note, DailyTask, Medication, Event

# USER MANAGEMENT VIEWS

@method_decorator(csrf_exempt, name='dispatch') 
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']
        pw_repeat = data['pw_repeat']
        first_name = data['first_name']

        if User.objects.filter(username=username).exists():
            return Response({'username_error': 'Sorry, that username is taken'})
        elif password != pw_repeat:
            return Response({'password_error': 'Passwords do not match'})
        else:
            user = User.objects.create_user(username=username, password=password, first_name=first_name)

            user = User.objects.get(id=user.id)

            return Response({ 'success': 'user created' })

@method_decorator(ensure_csrf_cookie, name='dispatch') 
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']

        try:
          user = auth.authenticate(username=username, password=password)
        except:
          return Response({'error': 'unable to authenticate user'})

        # print(auth.authenticate(username=username, password=password))

        if user is not None:
          token, _ = Token.objects.get_or_create(user=user)
          auth.login(request, user)
          return Response({'success': 'logged in', 'key': token.key, 'user_id': user.id, 'user_name': user.first_name })
        else:
            return Response({ 'error': 'unable to log in after authenticating' })

class LogoutView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        auth.logout(request)
        response = Response({ 'success': 'user logged out' })
        return response

@method_decorator(ensure_csrf_cookie, name='dispatch') #for use in development only
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({ 'success': 'CSRF token created' })



# MODEL VIEWS

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get_queryset(self): 
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        print(f'note self.request.user {self.request.user}')

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
        is_prescription = self.request.query_params.get('is_prescription', None)
        if is_prescription:
            queryset = queryset.filter(is_prescription=is_prescription)
        query_set = queryset.filter(user=self.request.user)
        return query_set


class EventViewSet(viewsets.ModelViewSet):
    serializer_class =EventSerializer
    queryset = Event.objects.all()

    def get_queryset(self): 
        queryset = self.queryset
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            queryset = queryset.filter(start__date=start_date)
        query_set = queryset.filter(user=self.request.user)
        return query_set
