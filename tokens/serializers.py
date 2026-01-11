from rest_framework import serializers
from .models import Token


class TokenStoreSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    token = serializers.CharField()
    token_type = serializers.ChoiceField(choices=Token.TYPE_CHOICES)
    last_four = serializers.CharField(max_length=4, required=False)
    expiry_month = serializers.IntegerField(required=False, min_value=1, max_value=12)
    expiry_year = serializers.IntegerField(required=False)
    metadata = serializers.JSONField(required=False, default=dict)


class TokenResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = [
            'id', 'user_id', 'token_type', 'last_four',
            'expiry_month', 'expiry_year', 'is_active',
            'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class TokenListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = [
            'id', 'user_id', 'token_type', 'last_four',
            'expiry_month', 'expiry_year', 'is_active',
            'created_at'
        ]

