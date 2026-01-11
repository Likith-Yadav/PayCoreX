from django.urls import path
from . import views

urlpatterns = [
    path('stats', views.get_stats, name='get_stats'),
    path('payments', views.get_payments, name='get_payments'),
    path('ledgers', views.get_ledgers, name='get_ledgers'),
]

