from rest_framework import routers 
from .views import UserViewSet, NoteViewSet

router = routers.DefaultRouter()
router.register(r'api/users', UserViewSet, 'users')
router.register(r'api/notes', NoteViewSet, 'notes')

urlpatterns = router.urls