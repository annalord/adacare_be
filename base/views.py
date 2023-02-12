from rest_framework import viewsets, permissions
from .serializers import NoteSerializer, DailyTaskSerializer, MedicationSerializer, EventSerializer
from .models import Note, DailyTask, Medication, Event
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib import auth
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt, csrf_protect
from rest_framework.authtoken.models import Token

# USER HOUSEKEEPING

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
            print('UN TAKEN')
            return Response({'error': 'Sorry, that username is taken'})
        elif password != pw_repeat:
            print('PW DONTMATCH')
            return Response({'error': 'Passwords do not match'})
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

        user = auth.authenticate(username=username, password=password)

        # print(auth.authenticate(username=username, password=password))

        if user is not None:
          token, _ = Token.objects.get_or_create(user=user)
          try:
            print(f'login user {user}')
            auth.login(request, user)
            print(f'self.request.user after login {self.request.user}')
          except:
            print('user not actually logged in!')
          return Response({'success': 'logged in', 'key': token.key, 'user_id': user.id, 'user_name': user.first_name })
        else:
            return Response({ 'error': 'unable to log in' })


class LogoutView(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, format=None):

        # request.user.auth_token.delete()
        print(f'inside logout post--{request.user.is_authenticated}')
        print(f'logout self.request.user {self.request.user}')

        auth.logout(request)
        response = Response({ 'success': 'logged out' })
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
