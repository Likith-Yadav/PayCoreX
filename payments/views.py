from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .serializers import (
    PaymentCreateSerializer,
    PaymentResponseSerializer,
    RefundSerializer,
    RefundResponseSerializer
)
from .services import PaymentOrchestrator, RefundService


@api_view(['POST'])
def create_payment(request):
    serializer = PaymentCreateSerializer(data=request.data)
    if serializer.is_valid():
        payment = PaymentOrchestrator.create_payment(
            merchant_id=request.merchant.id,
            amount=serializer.validated_data['amount'],
            method=serializer.validated_data['method'],
            currency=serializer.validated_data.get('currency', 'INR'),
            user_id=serializer.validated_data.get('user_id'),
            reference_id=serializer.validated_data.get('reference_id'),
            metadata=serializer.validated_data.get('metadata', {})
        )
        
        try:
            payment = PaymentOrchestrator.process_payment(payment)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            PaymentResponseSerializer(payment).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_payment(request, payment_id):
    try:
        from .models import Payment
        payment = Payment.objects.get(id=payment_id, merchant_id=request.merchant.id)
        return Response(
            PaymentResponseSerializer(payment).data,
            status=status.HTTP_200_OK
        )
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def create_refund(request):
    serializer = RefundSerializer(data=request.data)
    if serializer.is_valid():
        try:
            refund = RefundService.create_refund(
                payment_id=serializer.validated_data['payment_id'],
                merchant_id=request.merchant.id,
                amount=serializer.validated_data.get('amount'),
                reason=serializer.validated_data.get('reason')
            )
            return Response(
                RefundResponseSerializer(refund).data,
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

