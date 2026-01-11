from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .serializers import (
    TokenStoreSerializer,
    TokenResponseSerializer,
    TokenListSerializer
)
from .services import TokenService


@api_view(['POST'])
def store_token(request):
    serializer = TokenStoreSerializer(data=request.data)
    if serializer.is_valid():
        token = TokenService.store_token(
            user_id=serializer.validated_data['user_id'],
            merchant_id=request.merchant.id,
            token_value=serializer.validated_data['token'],
            token_type=serializer.validated_data['token_type'],
            last_four=serializer.validated_data.get('last_four'),
            expiry_month=serializer.validated_data.get('expiry_month'),
            expiry_year=serializer.validated_data.get('expiry_year'),
            metadata=serializer.validated_data.get('metadata', {})
        )
        return Response(
            TokenResponseSerializer(token).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_tokens(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    tokens = TokenService.list_tokens(user_id, request.merchant.id)
    return Response(
        TokenListSerializer(tokens, many=True).data,
        status=status.HTTP_200_OK
    )


@api_view(['DELETE'])
def delete_token(request, id):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        TokenService.delete_token(id, user_id)
        return Response({'message': 'Token deleted successfully'}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

