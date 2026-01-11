from django.urls import path
from . import views

urlpatterns = [
    path('store', views.store_token, name='store_token'),
    path('list', views.list_tokens, name='list_tokens'),
    path('<uuid:id>', views.delete_token, name='delete_token'),
]

