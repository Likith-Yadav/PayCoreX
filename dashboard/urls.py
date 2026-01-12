from django.urls import path
from . import views

urlpatterns = [
    path('stats', views.stats, name='stats'),
    path('payments', views.payments, name='payments'),
    path('ledgers', views.ledgers, name='ledgers'),
    path('payment-configs', views.payment_configs, name='payment_configs'),
    path('payment-configs/<uuid:config_id>', views.payment_config_detail, name='payment_config_detail'),
]

