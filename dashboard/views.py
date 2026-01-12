from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from payments.models import Payment, Refund
from ledger.models import Ledger


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
