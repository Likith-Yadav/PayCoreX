from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .serializers import (
    WalletCreateSerializer,
    WalletTopupSerializer,
    WalletPaySerializer,
    WalletResponseSerializer
)
from .services import WalletService


@api_view(['POST'])
def create_wallet(request):
    serializer = WalletCreateSerializer(data=request.data)
    if serializer.is_valid():
        wallet = WalletService.create_wallet(
            serializer.validated_data['user_id'],
            request.merchant.id
        )
        return Response(
            WalletResponseSerializer(wallet).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def topup_wallet(request):
    serializer = WalletTopupSerializer(data=request.data)
    if serializer.is_valid():
        try:
            wallet = WalletService.topup_wallet(
                serializer.validated_data['wallet_id'],
                serializer.validated_data['amount'],
                request.merchant.id
            )
            return Response(
                WalletResponseSerializer(wallet).data,
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def pay_from_wallet(request):
    serializer = WalletPaySerializer(data=request.data)
    if serializer.is_valid():
        try:
            wallet = WalletService.pay_from_wallet(
                serializer.validated_data['wallet_id'],
                serializer.validated_data['amount'],
                request.merchant.id,
                serializer.validated_data.get('reference_id')
            )
            return Response(
                WalletResponseSerializer(wallet).data,
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_balance(request):
    wallet_id = request.query_params.get('wallet_id')
    if not wallet_id:
        return Response({'error': 'wallet_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        balance = WalletService.get_balance(wallet_id, request.merchant.id)
        return Response({'wallet_id': wallet_id, 'balance': str(balance)}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

