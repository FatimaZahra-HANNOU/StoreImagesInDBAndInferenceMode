from django.urls import path
from .consumers import ProgressConsumer


websocket_urlpatterns = [
    path('socket/', ProgressConsumer.as_asgi()),
]
