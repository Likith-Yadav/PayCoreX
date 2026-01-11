from rest_framework import serializers
from .models import CryptoAddress, CryptoTransaction


class CryptoAddressSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    address = serializers.CharField()
    network = serializers.ChoiceField(choices=CryptoAddress.NETWORK_CHOICES, default='ethereum')


class CryptoAddressResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoAddress
        fields = ['id', 'user_id', 'address', 'network', 'created_at']


class CryptoTransactionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoTransaction
        fields = [
            'id', 'payment_id', 'tx_hash', 'from_address', 'to_address',
            'amount', 'network', 'status', 'block_number', 'confirmations',
            'created_at', 'updated_at'
        ]

