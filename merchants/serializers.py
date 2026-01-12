from rest_framework import serializers
from .models import Merchant, MerchantPaymentConfig


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


class MerchantPaymentConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantPaymentConfig
        fields = [
            'id', 'config_type', 'is_primary', 'is_active',
            'account_holder_name', 'account_number', 'ifsc_code', 
            'bank_name', 'branch_name', 'upi_id',
            'provider_key', 'provider_secret', 'provider_merchant_id',
            'provider_webhook_secret', 'metadata', 'is_verified',
            'verified_at', 'verified_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_verified', 'verified_at', 'verified_by']
    
    def to_representation(self, instance):
        """Add verified_by username to response"""
        data = super().to_representation(instance)
        if instance.verified_by:
            data['verified_by_username'] = instance.verified_by.username
            data['verified_by_email'] = instance.verified_by.email
        return data
    
    def validate(self, attrs):
        config_type = attrs.get('config_type')
        
        # Validate bank account fields
        if config_type == 'bank_account':
            required_fields = ['account_holder_name', 'account_number', 'ifsc_code', 'bank_name']
            for field in required_fields:
                if not attrs.get(field):
                    raise serializers.ValidationError(f"{field} is required for bank account")
        
        # Validate UPI fields
        elif config_type == 'upi':
            if not attrs.get('upi_id'):
                raise serializers.ValidationError("upi_id is required for UPI")
        
        # Validate payment provider fields
        elif config_type in ['razorpay', 'stripe', 'phonepe', 'paytm', 'other']:
            if not attrs.get('provider_key') or not attrs.get('provider_secret'):
                raise serializers.ValidationError("provider_key and provider_secret are required for payment providers")
        
        return attrs

