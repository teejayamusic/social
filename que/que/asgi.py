# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from app.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'que.settings')

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/chat/<int:chat_id>/", ChatConsumer.as_asgi()),
            ]
        )
    ),
    "http": get_asgi_application(),
})
