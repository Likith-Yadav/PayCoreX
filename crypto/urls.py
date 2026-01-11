from django.urls import path
from . import views

urlpatterns = [
    path('address', views.register_address, name='register_address'),
    path('status/<str:tx>', views.get_transaction_status, name='get_transaction_status'),
]

