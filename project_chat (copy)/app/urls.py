from django.urls import include, path
from rest_framework import routers
from app.api import views

router = routers.DefaultRouter()
router.register(r'users', views.UsersViewSet, basename="users")
router.register(r'groups', views.GroupViewSet, basename="groups")
router.register(r'messages', views.MessagesViewSet, basename="messages")

urlpatterns = [
    path('', include(router.urls)),
]
