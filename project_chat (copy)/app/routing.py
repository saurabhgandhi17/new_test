from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # path('ws/wsc/<str:groupname>/',consumers.CustomWebsocketConsumer.as_asgi()),
    path('ws/wsc/<str:groupname>/', consumers.CustomWebsocketConsumer.as_asgi()),
]
