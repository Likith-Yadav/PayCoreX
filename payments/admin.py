from django.contrib import admin
from .models import Payment, Refund


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'merchant_id', 'amount', 'status', 'method', 'created_at']
    list_filter = ['status', 'method', 'created_at']
    search_fields = ['id', 'merchant_id', 'reference_id']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment_id', 'merchant_id', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'payment_id', 'reference_id']
    readonly_fields = ['id', 'created_at', 'updated_at']

