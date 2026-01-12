from django.contrib import admin
from django.urls import path, include
from core.views import health_check
import core.admin  # Import to apply admin customization

urlpatterns = [
    path('', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('v1/merchants/', include('merchants.urls')),
    path('v1/payments/', include('payments.urls')),
    path('v1/wallet/', include('wallet.urls')),
    path('v1/tokens/', include('tokens.urls')),
    path('v1/webhooks/', include('webhooks.urls')),
    path('v1/crypto/', include('crypto.urls')),
    path('v1/dashboard/', include('dashboard.urls')),
]

