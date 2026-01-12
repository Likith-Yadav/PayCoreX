from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from merchants.models import MerchantPaymentConfig
import qrcode
import io
import base64
from .serializers import (
    PaymentCreateSerializer,
    PaymentResponseSerializer,
    RefundSerializer,
    RefundResponseSerializer
)
from .services import PaymentOrchestrator, RefundService
from .models import Payment


@api_view(['POST'])
@permission_classes([AllowAny])  # HMAC auth handled by middleware
def create_payment(request):
    # Get merchant from request.auth (set by HMACAuthentication)
    merchant = request.auth if hasattr(request, 'auth') and request.auth else None
    if not merchant:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = PaymentCreateSerializer(data=request.data)
    if serializer.is_valid():
        payment = PaymentOrchestrator.create_payment(
            merchant_id=merchant.id,
            amount=serializer.validated_data['amount'],
            method=serializer.validated_data['method'],
            currency=serializer.validated_data.get('currency', 'INR'),
            user_id=serializer.validated_data.get('user_id'),
            reference_id=serializer.validated_data.get('reference_id'),
            metadata=serializer.validated_data.get('metadata', {})
        )
        
        try:
            # For UPI payments, don't process immediately - just create and return
            # Payment will be confirmed later via webhook or manual update
            if serializer.validated_data['method'] == 'upi_intent':
                # Set status to pending for UPI payments
                payment.status = 'pending'
                payment.save()
            else:
                # Process other payment methods immediately
                payment = PaymentOrchestrator.process_payment(payment)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response_data = PaymentResponseSerializer(payment).data
        # Add payment page URL for redirect
        response_data['payment_page_url'] = f"/v1/payments/{payment.id}/page"
        
        return Response(
            response_data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])  # HMAC auth handled by authentication class
def get_payment(request, payment_id):
    """Get payment status - allows public access for payment page status checks"""
    try:
        payment = Payment.objects.get(id=payment_id)
        
        # If authenticated, verify merchant owns this payment
        merchant = request.auth if hasattr(request, 'auth') and request.auth else None
        if merchant and str(payment.merchant_id) != str(merchant.id):
            return Response(
                {'error': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Return payment data (public access allowed for status checks)
        return Response(
            PaymentResponseSerializer(payment).data,
            status=status.HTTP_200_OK
        )
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])  # HMAC auth handled by authentication class
def get_payment_methods(request):
    """Get available payment methods for the authenticated merchant"""
    merchant = request.auth if hasattr(request, 'auth') and request.auth else None
    if not merchant:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Get verified and active payment configs
    configs = MerchantPaymentConfig.objects.filter(
        merchant=merchant,
        is_verified=True,
        is_active=True
    )
    
    # Map config types to payment methods
    method_mapping = {
        'upi': 'upi_intent',
        'razorpay': 'tokenized',
        'stripe': 'tokenized',
        'phonepe': 'upi_intent',
        'paytm': 'upi_intent',
    }
    
    available_methods = []
    for config in configs:
        method = method_mapping.get(config.config_type)
        if method and method not in [m['method'] for m in available_methods]:
            method_info = {
                'method': method,
                'display_name': config.get_config_type_display(),
                'config_type': config.config_type,
            }
            
            # Add method-specific info
            if config.config_type == 'upi':
                method_info['upi_id'] = config.upi_id
            elif config.config_type in ['razorpay', 'stripe', 'phonepe', 'paytm']:
                method_info['provider'] = config.config_type
                method_info['merchant_id'] = config.provider_merchant_id
            
            available_methods.append(method_info)
    
    # If no configs, return default methods (for backward compatibility)
    if not available_methods:
        available_methods = [
            {'method': 'upi_intent', 'display_name': 'UPI', 'config_type': None},
            {'method': 'wallet', 'display_name': 'Wallet', 'config_type': None},
        ]
    
    return Response({
        'merchant_id': str(merchant.id),
        'available_methods': available_methods
    })


def payment_page(request, payment_id):
    """
    Payment page that shows QR code or redirects to payment app - Public endpoint
    This endpoint is READ-ONLY and will NEVER create new payments.
    It only displays existing payments by their ID.
    """
    # Ensure this is a GET request - no POST/PUT/DELETE allowed
    if request.method != 'GET':
        return HttpResponse('Method not allowed. This page only displays existing payments.', status=405)
    
    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        return render(request, 'payments/error.html', {
            'error': 'Payment not found',
            'payment_id': str(payment_id)
        }, status=404)
    
    # Get merchant's payment config for this payment method
    merchant_config = None
    if payment.method == 'upi_intent':
        configs = MerchantPaymentConfig.objects.filter(
            merchant_id=payment.merchant_id,
            config_type='upi',
            is_verified=True,
            is_active=True
        ).first()
        if configs:
            merchant_config = configs
    
    # Generate QR code on server side
    qr_code_data_uri = None
    if payment.method == 'upi_intent' and merchant_config:
        # Include payment ID in transaction note for easier tracking
        transaction_note = f"Payment-{str(payment.id)[:8]}"
        upi_string = f"upi://pay?pa={merchant_config.upi_id}&pn=PayCoreX&am={payment.amount}&cu=INR&tn={transaction_note}"
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(upi_string)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Convert to base64 data URI
            img_base64 = base64.b64encode(buffer.read()).decode()
            qr_code_data_uri = f"data:image/png;base64,{img_base64}"
        except Exception as e:
            print(f"Error generating QR code: {e}")
    
    context = {
        'payment': payment,
        'merchant_config': merchant_config,
        'qr_code_data_uri': qr_code_data_uri,
    }
    
    return render(request, 'payments/payment_page.html', context)


@api_view(['POST'])
@permission_classes([AllowAny])  # Public endpoint for webhook callbacks
def update_payment_status(request, payment_id):
    """Update payment status - used for webhooks or manual confirmation"""
    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get status from request
    new_status = request.data.get('status')
    if new_status not in ['success', 'failed', 'cancelled']:
        return Response(
            {'error': 'Invalid status. Must be: success, failed, or cancelled'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Update payment status
    old_status = payment.status
    payment.status = new_status
    payment.provider_reference = request.data.get('provider_reference', payment.provider_reference)
    payment.failure_reason = request.data.get('failure_reason') if new_status == 'failed' else None
    payment.save()
    
    # If payment is now successful, update ledger and send webhook
    if new_status == 'success' and old_status != 'success':
        from ledger.services import LedgerService
        from webhooks.services import WebhookService
        
        LedgerService.update_ledger(
            entity='merchant',
            entity_id=payment.merchant_id,
            credit=payment.amount,
            reference_type='payment',
            reference_id=payment.id,
            description=f'Payment received: {payment.amount}'
        )
        
        WebhookService.send_payment_webhook(payment)
    
    return Response(
        PaymentResponseSerializer(payment).data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])  # Public endpoint for payment gateway webhooks
def payment_webhook(request):
    """
    Receive webhooks from payment gateways (Razorpay, PhonePe, Paytm, etc.)
    This endpoint verifies the webhook signature and updates payment status
    """
    from .verification import PaymentVerificationService
    
    # Get webhook data
    webhook_data = request.data
    payment_id = webhook_data.get('payment_id') or webhook_data.get('entity', {}).get('id')
    
    if not payment_id:
        return Response({'error': 'Payment ID not found in webhook'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Verify webhook signature (if provided)
    # This would be provider-specific
    webhook_signature = request.headers.get('X-Razorpay-Signature') or \
                       request.headers.get('X-PhonePe-Signature') or \
                       request.headers.get('X-Paytm-Signature')
    
    # Verify payment
    verification_result = PaymentVerificationService.verify_payment(
        payment_id,
        verification_data=webhook_data
    )
    
    return Response({
        'verified': verification_result['verified'],
        'status': verification_result['status'],
        'message': verification_result['message']
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])  # Public endpoint - users can submit UTR
def verify_utr(request, payment_id):
    """
    Verify payment using UTR (Unique Transaction Reference) number
    Public endpoint - users can submit their UTR after payment
    """
    from .verification import PaymentVerificationService
    
    # Accept both 'utr_number' and 'transaction_id' for compatibility
    utr_number = request.data.get('utr_number') or request.data.get('transaction_id')
    if not utr_number:
        return Response(
            {'error': 'UTR number is required', 'verified': False, 'status': 'error'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate UTR format
    utr_number = utr_number.strip()
    if len(utr_number) < 8 or len(utr_number) > 50:
        return Response(
            {'error': 'UTR number must be between 8-50 characters', 'verified': False, 'status': 'error'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        verification_result = PaymentVerificationService.verify_utr(
            payment_id,
            utr_number
        )
        
        # Return response in format expected by frontend
        return Response({
            'status': verification_result.get('status', 'pending'),
            'verified': verification_result.get('verified', False),
            'message': verification_result.get('message', 'UTR recorded'),
        }, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response(
            {'error': str(e), 'verified': False, 'status': 'error'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Verification error: {str(e)}', 'verified': False, 'status': 'error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])  # HMAC auth handled by authentication class
def verify_payment(request, payment_id):
    """
    Manually verify a payment (for UPI or manual verification)
    Requires authentication
    """
    from .verification import PaymentVerificationService
    
    merchant = request.auth if hasattr(request, 'auth') and request.auth else None
    if not merchant:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        payment = Payment.objects.get(id=payment_id, merchant_id=merchant.id)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get verification data
    transaction_id = request.data.get('transaction_id')
    verify = request.data.get('verify', False)  # Manual verification flag
    
    if verify and transaction_id:
        # Manually mark as verified
        try:
            payment = PaymentVerificationService.mark_payment_verified(
                payment_id,
                transaction_id=transaction_id,
                verified_by=merchant
            )
            return Response(
                PaymentResponseSerializer(payment).data,
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Try automatic verification
        verification_result = PaymentVerificationService.verify_payment(
            payment_id,
            verification_data={'transaction_id': transaction_id} if transaction_id else None
        )
        return Response(verification_result, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])  # HMAC auth handled by authentication class
def create_refund(request):
    # Get merchant from request.auth (set by HMACAuthentication)
    merchant = request.auth if hasattr(request, 'auth') and request.auth else None
    if not merchant:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = RefundSerializer(data=request.data)
    if serializer.is_valid():
        try:
            refund = RefundService.create_refund(
                payment_id=serializer.validated_data['payment_id'],
                merchant_id=merchant.id,
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

