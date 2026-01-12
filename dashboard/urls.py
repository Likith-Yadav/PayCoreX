from django.urls import path
from . import views

urlpatterns = [
    path('stats', views.stats, name='dashboard_stats'),
    path('payments', views.payments, name='dashboard_payments'),
    path('ledgers', views.ledgers, name='dashboard_ledgers'),
    path('payment-configs', views.payment_configs, name='dashboard_payment_configs'),
    path('payment-configs/<uuid:config_id>', views.payment_config_detail, name='dashboard_payment_config_detail'),
    path('verifications', views.pending_verifications, name='dashboard_pending_verifications'),
    path('verifications/<uuid:payment_id>/verify', views.verify_payment, name='dashboard_verify_payment'),
]

