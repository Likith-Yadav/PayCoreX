from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('profile', views.profile, name='profile'),
    path('regenerate-key', views.regenerate_api_key, name='regenerate_key'),
]

