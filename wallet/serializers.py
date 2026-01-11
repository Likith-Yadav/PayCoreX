from rest_framework import serializers
from .models import Wallet


class WalletCreateSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()


class WalletTopupSerializer(serializers.Serializer):
    wallet_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)


class WalletPaySerializer(serializers.Serializer):
    wallet_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    reference_id = serializers.UUIDField(required=False)


class WalletResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'user_id', 'balance', 'currency', 'is_active', 'created_at']

