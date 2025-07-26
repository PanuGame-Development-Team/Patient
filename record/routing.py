from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"^record/ws/$", consumers.RecordConsumer.as_asgi()),
]