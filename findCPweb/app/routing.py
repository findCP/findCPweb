from django.urls import re_path
from django.conf.urls import url
from django.urls import path

from . import consumers

websocket_urlpatterns = [
	path('ws/conn', consumers.ChatConsumer),
]
