from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_merchant, name='register_merchant'),
    path('apikey', views.regenerate_api_key, name='regenerate_api_key'),
    path('profile', views.get_profile, name='get_profile'),
    path('payment-configs', views.payment_configs, name='payment_configs'),
    path('payment-configs/<uuid:config_id>', views.payment_config_detail, name='payment_config_detail'),
]

