from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    CryptoAddressSerializer,
    CryptoAddressResponseSerializer,
    CryptoTransactionResponseSerializer
)
from .services import CryptoService


@api_view(['POST'])
def register_address(request):
    serializer = CryptoAddressSerializer(data=request.data)
    if serializer.is_valid():
        address = CryptoService.register_address(
            user_id=serializer.validated_data['user_id'],
            merchant_id=request.merchant.id,
            address=serializer.validated_data['address'],
            network=serializer.validated_data.get('network', 'ethereum')
        )
        return Response(
            CryptoAddressResponseSerializer(address).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_transaction_status(request, tx):
    network = request.query_params.get('network', 'ethereum')
    status_data = CryptoService.get_transaction_status(tx, network)
    return Response(status_data, status=status.HTTP_200_OK)

