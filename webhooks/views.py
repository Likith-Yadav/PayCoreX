from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .serializers import (
    WebhookEndpointSerializer,
    WebhookEndpointResponseSerializer,
    WebhookDeliveryResponseSerializer
)
from .services import WebhookService


@api_view(['POST'])
def create_endpoint(request):
    serializer = WebhookEndpointSerializer(data=request.data)
    if serializer.is_valid():
        endpoint, secret = WebhookService.create_endpoint(
            merchant_id=request.merchant.id,
            url=serializer.validated_data['url'],
            events=serializer.validated_data.get('events')
        )
        response_data = WebhookEndpointResponseSerializer(endpoint).data
        response_data['secret'] = secret
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def retry_webhook(request):
    delivery_id = request.data.get('delivery_id')
    if not delivery_id:
        return Response({'error': 'delivery_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        delivery = WebhookService.retry_webhook(delivery_id, request.merchant.id)
        return Response(
            WebhookDeliveryResponseSerializer(delivery).data,
            status=status.HTTP_200_OK
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

