from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from ..models import GroupInfoModel, User
from .serializers import GroupSerializer, MessagesSerializer,PrivateMessagesModel,UsersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = GroupInfoModel.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('name',)
    

class MessagesViewSet(viewsets.ModelViewSet):
    queryset = PrivateMessagesModel.objects.all()
    serializer_class = MessagesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('sender','receiver')
