import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import GroupInfoModel, PrivateGroupMessagesModel, PrivateMessagesModel, User, GroupMessagesModel
from .api.serializers import PrivateGroupMessagesSerializer, GroupSerializer, GroupMessagesSerializer , MessagesSerializer


class CustomWebsocketConsumer(WebsocketConsumer):
    def one_to_one_chat(self, data):
        '''
            function used to store one to one chat records
        '''
        receiver = User.objects.get(username=self.group_name)
        sender = User.objects.get(id=1)  # --> need to change
        queryset = PrivateGroupMessagesModel.objects.filter(name=sender.username + "_"+receiver.username)
        if not queryset.exists():
            serializer = PrivateGroupMessagesSerializer(data={
                "name": sender.username + "_"+receiver.username,
                "receiver": receiver.id,
                "sender": sender.id
            })
            if serializer.is_valid():
                group = serializer.save()
        else:
            group = PrivateGroupMessagesModel.objects.filter(name=sender.username + "_"+receiver.username)
        
        chat = MessagesSerializer(data = {
                "content" : data["msg"], 
                "sender":sender.id, 
                "receiver" : receiver.id, 
                "group" : group[0].id
            })
        if chat.is_valid():
            chat.save()


    def group_chat(self, data):
        '''
            function used to store group chat records
        '''
        group = GroupInfoModel.objects.filter(name=self.group_name).first()
        if not group:
            user = User.objects.get(id=1)
            group_serializer = GroupSerializer(data={
                "name": self.group_name,
                "created_by": user.id
            })
            if group_serializer.is_valid():
                group = group_serializer.save()

        sender = User.objects.get(id=1)
        participants = data['participants']
        for participant in participants:
            receiver = User.objects.get(pk=participant)
            message_serializer = GroupMessagesSerializer(data={
                "content": data["msg"],
                "sender": sender.id,
                "participants": receiver.pk,
                "group": group.id
            })
            if message_serializer.is_valid():
                message_serializer.save()

    def connect(self):
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        data = json.loads(text_data)
        message = data['msg']
        message_type = data['message_type']

        '''
            Check type of messages - it's one-to-one or group
        '''
        if message_type == "one_to_one":
            self.one_to_one_chat(data)
        else:
            self.group_chat(data)

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat.message',  # event handler
                'message': message,
            },
        )

     # Event handler
    def chat_message(self, event):
        self.send(text_data=json.dumps({
            "msg": event['message']
        }))


    def disconnect(self, code):
        pass