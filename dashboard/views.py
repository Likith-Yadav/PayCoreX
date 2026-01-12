from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from payments.models import Payment, Refund
from payments.serializers import PaymentResponseSerializer
from payments.verification import PaymentVerificationService
from ledger.models import Ledger
from merchants.models import MerchantPaymentConfig
from merchants.serializers import MerchantPaymentConfigSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stats(request):
    """Get dashboard statistics"""
    merchant = request.user.merchant
    if not merchant:
        return Response({'error': 'No merchant account'}, status=400)
    
    # Date ranges
    today = timezone.now().date()
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)
    
    # Payment stats
    all_payments = Payment.objects.filter(merchant_id=merchant.id)
    successful_payments = all_payments.filter(status='success')
    
    total_volume = successful_payments.aggregate(Sum('amount'))['amount__sum'] or 0
    total_transactions = all_payments.count()
    successful_transactions = successful_payments.count()
    success_rate = (successful_transactions / total_transactions * 100) if total_transactions > 0 else 0
    
    # This month
    this_month_payments = successful_payments.filter(created_at__gte=this_month_start)
    this_month_volume = this_month_payments.aggregate(Sum('amount'))['amount__sum'] or 0
    this_month_count = this_month_payments.count()
    
    # Last month
    last_month_payments = successful_payments.filter(
        created_at__gte=last_month_start,
        created_at__lte=last_month_end
    )
    last_month_volume = last_month_payments.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Refunds
    refunds = Refund.objects.filter(merchant_id=merchant.id, status='success')
    total_refunds = refunds.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Recent activity
    recent_payments = all_payments.order_by('-created_at')[:10]
    
    return Response({
        'overview': {
            'total_volume': float(total_volume),
            'total_transactions': total_transactions,
            'successful_transactions': successful_transactions,
        'success_rate': round(success_rate, 2),
            'total_refunds': float(total_refunds),
            'net_volume': float(total_volume - total_refunds),
        },
        'this_month': {
            'volume': float(this_month_volume),
            'transactions': this_month_count,
        },
        'last_month': {
            'volume': float(last_month_volume),
        },
        'recent_payments': [
            {
                'id': str(p.id),
                'amount': float(p.amount),
                'status': p.status,
                'method': p.method,
                'created_at': p.created_at.isoformat(),
            }
            for p in recent_payments
        ]
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payments(request):
    """Get payments list with filters"""
    merchant = request.user.merchant
    if not merchant:
        return Response({'error': 'No merchant account'}, status=400)
    
    payments = Payment.objects.filter(merchant_id=merchant.id)
    
    # Filters
    status_filter = request.query_params.get('status')
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    method_filter = request.query_params.get('method')
    if method_filter:
        payments = payments.filter(method=method_filter)
    
    # Date range
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    if start_date:
        payments = payments.filter(created_at__gte=start_date)
    if end_date:
        payments = payments.filter(created_at__lte=end_date)
    
    # Pagination
    page = int(request.query_params.get('page', 1))
    limit = int(request.query_params.get('limit', 20))
    offset = (page - 1) * limit
    
    total = payments.count()
    payments = payments.order_by('-created_at')[offset:offset + limit]
    
    return Response({
        'total': total,
        'page': page,
        'limit': limit,
        'results': [
            {
                'id': str(p.id),
                'amount': float(p.amount),
                'currency': p.currency,
                'status': p.status,
                'method': p.method,
                'user_id': str(p.user_id) if p.user_id else None,
                'reference_id': p.reference_id,
                'provider_reference': p.provider_reference,
                'failure_reason': p.failure_reason,
                'metadata': p.metadata,
                'created_at': p.created_at.isoformat(),
                'updated_at': p.updated_at.isoformat(),
            }
            for p in payments
        ]
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ledgers(request):
    """Get ledger entries"""
    merchant = request.user.merchant
    if not merchant:
        return Response({'error': 'No merchant account'}, status=400)
    
    ledgers = Ledger.objects.filter(
        entity='merchant',
        entity_id=merchant.id
    ).order_by('-created_at')
    
    # Pagination
    page = int(request.query_params.get('page', 1))
    limit = int(request.query_params.get('limit', 20))
    offset = (page - 1) * limit
    
    total = ledgers.count()
    ledgers = ledgers[offset:offset + limit]
    
    return Response({
        'total': total,
        'page': page,
        'limit': limit,
        'results': [
            {
        'id': str(l.id),
                'debit': float(l.debit) if l.debit else None,
                'credit': float(l.credit) if l.credit else None,
                'balance': float(l.balance),
        'reference_type': l.reference_type,
        'reference_id': str(l.reference_id) if l.reference_id else None,
        'description': l.description,
                'created_at': l.created_at.isoformat(),
            }
            for l in ledgers
        ]
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def payment_configs(request):
    """Get or create payment configurations"""
    merchant = request.user.merchant
    if not merchant:
        return Response({'error': 'No merchant account'}, status=400)
    
    if request.method == 'GET':
        configs = MerchantPaymentConfig.objects.filter(merchant=merchant)
        serializer = MerchantPaymentConfigSerializer(configs, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MerchantPaymentConfigSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(merchant=merchant)
                return Response(serializer.data, status=201)
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        return Response(serializer.errors, status=400)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def payment_config_detail(request, config_id):
    """Update or delete payment configuration"""
    merchant = request.user.merchant
    if not merchant:
        return Response({'error': 'No merchant account'}, status=400)
    
    try:
        config = MerchantPaymentConfig.objects.get(id=config_id, merchant=merchant)
    except MerchantPaymentConfig.DoesNotExist:
        return Response({'error': 'Payment configuration not found'}, status=404)
    
    if request.method == 'PUT':
        serializer = MerchantPaymentConfigSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        config.delete()
        return Response({'message': 'Payment configuration deleted'}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_verifications(request):
    """Get pending payments that need verification (with UTR numbers)"""
    merchant = request.user.merchant
    if not merchant:
        return Response({'error': 'No merchant account'}, status=400)
    
    # Get pending payments with UTR numbers
    pending_payments = Payment.objects.filter(
        merchant_id=merchant.id,
        status='pending'
    ).order_by('-created_at')
    
    # Filter only payments with UTR numbers
    payments_with_utr = []
    for payment in pending_payments:
        utr_number = payment.metadata.get('utr_number')
        if utr_number:
            payments_with_utr.append({
                'id': str(payment.id),
                'amount': float(payment.amount),
                'currency': payment.currency,
                'method': payment.method,
                'user_id': str(payment.user_id) if payment.user_id else None,
                'reference_id': payment.reference_id,
                'utr_number': utr_number,
                'utr_submitted_at': payment.metadata.get('utr_submitted_at'),
                'created_at': payment.created_at.isoformat(),
                'updated_at': payment.updated_at.isoformat(),
            })
    
    return Response({
        'total': len(payments_with_utr),
        'results': payments_with_utr
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request, payment_id):
    """Verify a payment manually (merchant verifies UTR matches bank account)"""
    merchant = request.user.merchant
    if not merchant:
        return Response({'error': 'No merchant account'}, status=400)
    
    try:
        payment = Payment.objects.get(id=payment_id, merchant_id=merchant.id)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=404)
    
    if payment.status != 'pending':
        return Response(
            {'error': f'Payment is already {payment.status}. Cannot verify.'},
            status=400
        )
    
    # Get UTR from request or payment metadata
    utr_number = request.data.get('utr_number') or payment.metadata.get('utr_number')
    if not utr_number:
        return Response({'error': 'UTR number is required'}, status=400)
    
    # Verify payment using UTR
    try:
        verified_payment = PaymentVerificationService.mark_payment_verified(
            payment_id,
            transaction_id=utr_number,
            verified_by=request.user
        )
        
        return Response(
            PaymentResponseSerializer(verified_payment).data,
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({'error': str(e)}, status=400)
