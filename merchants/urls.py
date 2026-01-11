from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_merchant, name='register_merchant'),
    path('apikey', views.regenerate_api_key, name='regenerate_api_key'),
    path('profile', views.get_profile, name='get_profile'),
]

