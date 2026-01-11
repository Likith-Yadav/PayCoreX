from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_payment, name='create_payment'),
    path('<uuid:payment_id>', views.get_payment, name='get_payment'),
    path('refund', views.create_refund, name='create_refund'),
]

