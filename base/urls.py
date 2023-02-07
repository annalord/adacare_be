from rest_framework import routers
from .views import LoginView, NoteViewSet, SignupView,LogoutView, DailyTaskViewSet, MedicationViewSet, EventViewSet, CheckAuthenticatedView, GetCSRFToken
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register('notes', NoteViewSet, 'notes')
router.register('dailytasks', DailyTaskViewSet, 'daily tasks')
router.register('medications', MedicationViewSet, 'medications')
router.register('events', EventViewSet, 'events')

urlpatterns = [
    path('', include(router.urls)),
    path('signup', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    # path('csrf/', GetCSRFToken.as_view()),
    # path('users', GetUsersView.as_view()),
    path('checkauth', CheckAuthenticatedView.as_view()),
    path('csrf/', views.csrf),
    path('ping/', views.ping),


]