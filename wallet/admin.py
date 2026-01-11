from django.contrib import admin
from .models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'merchant_id', 'balance', 'currency', 'is_active', 'created_at']
    list_filter = ['is_active', 'currency', 'created_at']
    search_fields = ['user_id', 'merchant_id']
    readonly_fields = ['id', 'created_at', 'updated_at']

