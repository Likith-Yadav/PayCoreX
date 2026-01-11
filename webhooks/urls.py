from django.urls import path
from . import views

urlpatterns = [
    path('provider', views.create_endpoint, name='create_endpoint'),
    path('retry', views.retry_webhook, name='retry_webhook'),
]

