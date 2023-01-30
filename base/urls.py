from rest_framework import routers
from .views import GetUsersView, LoginView, NoteViewSet, SignupView, GetCSRFToken,LogoutView, DailyTaskViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('notes', NoteViewSet, 'notes')
router.register('dailytasks', DailyTaskViewSet, 'daily tasks' )

urlpatterns = [
    path('', include(router.urls)),
    path('signup', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('csrf', GetCSRFToken.as_view()),
    path('users', GetUsersView.as_view())
]