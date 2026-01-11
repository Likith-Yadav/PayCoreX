from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    MerchantRegisterSerializer,
    MerchantResponseSerializer,
    APIKeyResponseSerializer
)
from .services import MerchantService


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

