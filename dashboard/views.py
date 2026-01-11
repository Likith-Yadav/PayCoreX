from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from payments.models import Payment, Refund
from ledger.models import Ledger
from wallet.models import Wallet


@api_view(['GET'])
def get_stats(request):
    merchant_id = request.merchant.id
    
    total_payments = Payment.objects.filter(merchant_id=merchant_id).count()
    successful_payments = Payment.objects.filter(
        merchant_id=merchant_id,
        status='success'
    ).count()
    
    total_volume = Payment.objects.filter(
        merchant_id=merchant_id,
        status='success'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    success_rate = (successful_payments / total_payments * 100) if total_payments > 0 else 0
    
    total_refunds = Refund.objects.filter(
        merchant_id=merchant_id,
        status='success'
    ).count()
    
    refund_amount = Refund.objects.filter(
        merchant_id=merchant_id,
        status='success'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    today = timezone.now().date()
    today_payments = Payment.objects.filter(
        merchant_id=merchant_id,
        created_at__date=today
    ).count()
    
    today_volume = Payment.objects.filter(
        merchant_id=merchant_id,
        status='success',
        created_at__date=today
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    return Response({
        'total_payments': total_payments,
        'successful_payments': successful_payments,
        'total_volume': str(total_volume),
        'success_rate': round(success_rate, 2),
        'total_refunds': total_refunds,
        'refund_amount': str(refund_amount),
        'today_payments': today_payments,
        'today_volume': str(today_volume)
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_payments(request):
    merchant_id = request.merchant.id
    
    status_filter = request.query_params.get('status')
    method_filter = request.query_params.get('method')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    queryset = Payment.objects.filter(merchant_id=merchant_id)
    
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if method_filter:
        queryset = queryset.filter(method=method_filter)
    if start_date:
        queryset = queryset.filter(created_at__gte=start_date)
    if end_date:
        queryset = queryset.filter(created_at__lte=end_date)
    
    payments = queryset.order_by('-created_at')[:100]
    
    from payments.serializers import PaymentResponseSerializer
    return Response(
        PaymentResponseSerializer(payments, many=True).data,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_ledgers(request):
    merchant_id = request.merchant.id
    
    entity_type = request.query_params.get('entity', 'merchant')
    entity_id = request.query_params.get('entity_id', str(merchant_id))
    
    queryset = Ledger.objects.filter(
        entity=entity_type,
        entity_id=entity_id
    )
    
    ledgers = queryset.order_by('-created_at')[:100]
    
    return Response([{
        'id': str(l.id),
        'entity': l.entity,
        'entity_id': str(l.entity_id),
        'credit': str(l.credit),
        'debit': str(l.debit),
        'balance': str(l.balance),
        'reference_type': l.reference_type,
        'reference_id': str(l.reference_id) if l.reference_id else None,
        'description': l.description,
        'created_at': l.created_at.isoformat()
    } for l in ledgers], status=status.HTTP_200_OK)

