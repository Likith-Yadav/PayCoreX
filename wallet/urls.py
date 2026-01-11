from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_wallet, name='create_wallet'),
    path('topup', views.topup_wallet, name='topup_wallet'),
    path('pay', views.pay_from_wallet, name='pay_from_wallet'),
    path('balance', views.get_balance, name='get_balance'),
]

