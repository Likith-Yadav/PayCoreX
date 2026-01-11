from rest_framework import serializers
from .models import Merchant


class MerchantRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['name', 'email']
        read_only_fields = ['id', 'api_key', 'secret', 'created_at']


class MerchantResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['id', 'name', 'email', 'api_key', 'is_active', 'created_at']


class APIKeyResponseSerializer(serializers.Serializer):
    api_key = serializers.CharField()
    secret = serializers.CharField()
    message = serializers.CharField()

