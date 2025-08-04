from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"^aichat/ws/$", consumers.AIConsumer.as_asgi()),
]