from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User
from merchants.models import Merchant
from merchants.services import MerchantService


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    company_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'first_name', 'last_name', 
                 'company_name', 'phone', 'username')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        company_name = validated_data.pop('company_name')
        password = validated_data.pop('password')
        username = validated_data.pop('username', validated_data.get('email'))  # Remove username from validated_data
        
        # Create user
        user = User.objects.create_user(
            password=password,
            username=username or validated_data.get('email'),  # Use email as username if not provided
            **validated_data
        )
        
        # Create merchant account
        merchant, secret = MerchantService.register_merchant(
            name=company_name,
            email=user.email
        )
        
        user.merchant = merchant
        user.company_name = company_name
        user.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include "email" and "password".')
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    merchant_id = serializers.UUIDField(source='merchant.id', read_only=True)
    api_key = serializers.CharField(source='merchant.api_key', read_only=True)
    merchant_name = serializers.CharField(source='merchant.name', read_only=True)
    merchant_created_at = serializers.DateTimeField(source='merchant.created_at', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'company_name', 'phone',
                 'merchant_id', 'api_key', 'merchant_name', 'merchant_created_at',
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'email', 'created_at', 'updated_at', 'merchant_id', 
                          'api_key', 'merchant_name', 'merchant_created_at')

