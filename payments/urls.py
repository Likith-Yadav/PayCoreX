from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_payment, name='create_payment'),
    path('methods', views.get_payment_methods, name='get_payment_methods'),
    path('<uuid:payment_id>', views.get_payment, name='get_payment'),
    path('<uuid:payment_id>/page', views.payment_page, name='payment_page'),
    path('<uuid:payment_id>/status', views.update_payment_status, name='update_payment_status'),
    path('<uuid:payment_id>/verify-utr', views.verify_utr, name='verify_utr'),
    path('<uuid:payment_id>/verify', views.verify_payment, name='verify_payment'),
    path('webhook', views.payment_webhook, name='payment_webhook'),
    path('refund', views.create_refund, name='create_refund'),
]

