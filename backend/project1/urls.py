from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('api/', include('api.urls')),
]