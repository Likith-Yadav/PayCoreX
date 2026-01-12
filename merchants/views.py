from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (
    MerchantRegisterSerializer,
    MerchantResponseSerializer,
    APIKeyResponseSerializer,
    MerchantPaymentConfigSerializer
)
from .services import MerchantService
from .models import MerchantPaymentConfig


@api_view(['POST'])
def register_merchant(request):
    serializer = MerchantRegisterSerializer(data=request.data)
    if serializer.is_valid():
        merchant, secret = MerchantService.register_merchant(
            serializer.validated_data['name'],
            serializer.validated_data['email']
        )
        response_data = MerchantResponseSerializer(merchant).data
        response_data['secret'] = secret
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def regenerate_api_key(request):
    merchant = request.merchant
    api_key, secret = MerchantService.regenerate_api_key(merchant)
    return Response({
        'api_key': api_key,
        'secret': secret,
        'message': 'API key regenerated successfully'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_profile(request):
    merchant = request.merchant
    profile = MerchantService.get_merchant_profile(merchant)
    return Response(profile, status=status.HTTP_200_OK)


# Payment Configuration Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def payment_configs(request):
    """List or create payment configurations"""
    merchant = request.user.merchant
    if not merchant:
        return Response({'error': 'No merchant account'}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        configs = MerchantPaymentConfig.objects.filter(merchant=merchant)
        serializer = MerchantPaymentConfigSerializer(configs, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MerchantPaymentConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(merchant=merchant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def payment_config_detail(request, config_id):
    """Get, update, or delete a payment configuration"""
    merchant = request.user.merchant
    if not merchant:
        return Response({'error': 'No merchant account'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        config = MerchantPaymentConfig.objects.get(id=config_id, merchant=merchant)
    except MerchantPaymentConfig.DoesNotExist:
        return Response({'error': 'Payment configuration not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MerchantPaymentConfigSerializer(config)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MerchantPaymentConfigSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        config.delete()
        return Response({'message': 'Payment configuration deleted'}, status=status.HTTP_200_OK)

