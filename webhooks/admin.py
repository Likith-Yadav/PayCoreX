from django.contrib import admin
from .models import WebhookEndpoint, WebhookDelivery


@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    list_display = ['id', 'merchant_id', 'url', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['url', 'merchant_id']
    readonly_fields = ['id', 'secret', 'created_at', 'updated_at']


@admin.register(WebhookDelivery)
class WebhookDeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'endpoint_id', 'event_type', 'status', 'retry_count', 'created_at']
    list_filter = ['status', 'event_type', 'created_at']
    search_fields = ['id', 'endpoint_id']
    readonly_fields = ['id', 'created_at', 'delivered_at']

