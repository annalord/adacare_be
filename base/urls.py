from rest_framework import routers
from django.urls import path, include
from .views import LoginView, NoteViewSet, SignupView,LogoutView, DailyTaskViewSet, MedicationViewSet, EventViewSet, GetCSRFToken

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
    path('csrf', GetCSRFToken.as_view()), #for use in development only
]