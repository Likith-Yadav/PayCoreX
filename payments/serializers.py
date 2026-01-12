from rest_framework import serializers
from .models import Payment, Refund


class PaymentCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    currency = serializers.CharField(max_length=3, default='INR', required=False)
    method = serializers.ChoiceField(choices=Payment.METHOD_CHOICES)
    user_id = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    reference_id = serializers.CharField(max_length=255, required=False)
    metadata = serializers.JSONField(required=False, default=dict)


class PaymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'merchant_id', 'amount', 'currency', 'status',
            'method', 'user_id', 'reference_id', 'provider_reference',
            'metadata', 'failure_reason', 'created_at', 'updated_at'
        ]


class RefundSerializer(serializers.Serializer):
    payment_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    reason = serializers.CharField(required=False)


class RefundResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = [
            'id', 'payment_id', 'merchant_id', 'amount', 'status',
            'reason', 'reference_id', 'provider_reference',
            'created_at', 'updated_at'
        ]

