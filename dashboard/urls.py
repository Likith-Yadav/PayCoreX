from django.urls import path
from . import views

urlpatterns = [
    path('stats', views.stats, name='stats'),
    path('payments', views.payments, name='payments'),
    path('ledgers', views.ledgers, name='ledgers'),
]

