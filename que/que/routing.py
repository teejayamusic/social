# your_project/routing.py

from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from app.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/friendship/(?P<from_user_id>\d+)/(?P<to_user_id>\d+)/$', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
