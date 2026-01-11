from rest_framework import serializers
from .models import WebhookEndpoint, WebhookDelivery


class WebhookEndpointSerializer(serializers.Serializer):
    url = serializers.URLField()
    events = serializers.ListField(child=serializers.CharField(), required=False)


class WebhookEndpointResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEndpoint
        fields = ['id', 'url', 'is_active', 'events', 'created_at']


class WebhookDeliveryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookDelivery
        fields = [
            'id', 'endpoint_id', 'event_type', 'status',
            'response_code', 'retry_count', 'created_at', 'delivered_at'
        ]

