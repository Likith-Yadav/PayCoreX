from django.contrib import admin
from .models import CryptoAddress, CryptoTransaction


@admin.register(CryptoAddress)
class CryptoAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'merchant_id', 'address', 'network', 'created_at']
    list_filter = ['network', 'created_at']
    search_fields = ['address', 'user_id']


@admin.register(CryptoTransaction)
class CryptoTransactionAdmin(admin.ModelAdmin):
    list_display = ['tx_hash', 'payment_id', 'status', 'amount', 'network', 'created_at']
    list_filter = ['status', 'network', 'created_at']
    search_fields = ['tx_hash', 'payment_id']
    readonly_fields = ['id', 'created_at', 'updated_at']

