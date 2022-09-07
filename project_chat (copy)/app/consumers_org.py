import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Group,Chat

class CustomWebsocketConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['groupname']
    
        # Check if group is exists or not
        group = Group.objects.filter(name=self.group_name).first()
        if group:
            pass
        else:
            # Create new group if not exists
            group = Group(name=self.group_name)
            group.save()

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['msg']
        group = Group.objects.get(name=self.group_name)
        chat = Chat(
            content=data["msg"],
            group = group
        )        
        chat.save()
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat.message',  # event handler
                'message': message,
            },
        )

    # Event handler
    def chat_message(self, event):
        print("eventevent", event)
        self.send(text_data=json.dumps({
            "msg": event['message']
        }))

    def disconnect(self, code):
        print('Disconnected')
