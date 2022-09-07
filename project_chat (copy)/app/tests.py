import pytest
import json
import asyncio
from django.test import TestCase
from django.urls import path
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator

from .consumers import CustomWebsocketConsumer
from .models import User


@pytest.mark.django_db
@pytest.mark.asyncio
class TestWebSockets(TestCase):
    databases = '__all__'

    def setUp(self):
        print('Setup the test database')
        self.user = User(username="saurabh")
        self.user.set_password('password@123')
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()

        self.user = User(username="tejash")
        self.user.set_password('password@123')
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()

        self.user = User(username="amit")
        self.user.set_password('password@123')
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()

    async def test_connect(self):
        print('2. Webscokect connection testing...')
        application = URLRouter(
            [path('ws/wsc/<str:groupname>/', CustomWebsocketConsumer.as_asgi()), ])
        communicator = WebsocketCommunicator(application, "/ws/wsc/tejash/")
        connected = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_private_chat(self):
        print('3. Private chat testing')
        application = URLRouter(
            [path('ws/wsc/<str:groupname>/', CustomWebsocketConsumer.as_asgi()), ])
        communicator = WebsocketCommunicator(application, "/ws/wsc/tejash/")
        connected = await communicator.connect()
        self.assertTrue(connected)
        # Send data to server for testing
        await communicator.send_to(text_data=json.dumps({"msg": "hello", "message_type": "private"}))
        # check if it raise the TimeoutError or not
        if pytest.raises(asyncio.TimeoutError):
            await communicator.receive_from()
        else:
            await communicator.receive_from()
        await communicator.disconnect()

    async def test_group_chat(self):
        print('3. Group chat testing')
        application = URLRouter(
            [path('ws/wsc/<str:groupname>/', CustomWebsocketConsumer.as_asgi()), ])
        communicator = WebsocketCommunicator(application, "/ws/wsc/indian/")
        connected = await communicator.connect()
        self.assertTrue(connected)
        # Send data to server for testing
        await communicator.send_to(text_data=json.dumps({"msg": "hello", "participants": [1, 2, 3], "message_type": "group"}))
        # check if it raise the TimeoutError or not
        if pytest.raises(asyncio.TimeoutError):
            await communicator.receive_from()
        else:
            await communicator.receive_from()
        await communicator.disconnect()
