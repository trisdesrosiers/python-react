from django.urls import path
from api.consumers import DatabaseChangesConsumer

websocket_urlpatterns = [
    path('ws/changes/', DatabaseChangesConsumer.as_asgi()),
]

