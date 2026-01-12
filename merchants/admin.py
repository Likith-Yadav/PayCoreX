from django.contrib import admin
from django.utils import timezone
from .models import Merchant, MerchantPaymentConfig


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'api_key', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'email', 'api_key']
    readonly_fields = ['id', 'api_key', 'secret', 'created_at', 'updated_at']


@admin.register(MerchantPaymentConfig)
class MerchantPaymentConfigAdmin(admin.ModelAdmin):
    list_display = ['merchant', 'config_type', 'is_primary', 'is_verified', 'verified_by', 'verified_at', 'created_at']
    list_filter = ['config_type', 'is_verified', 'is_primary', 'is_active', 'created_at']
    search_fields = ['merchant__name', 'merchant__email', 'upi_id', 'account_number', 'bank_name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'verified_at', 'verified_by']
    fieldsets = (
        ('Basic Information', {
            'fields': ('merchant', 'config_type', 'is_primary', 'is_active')
        }),
        ('Bank Account', {
            'fields': ('account_holder_name', 'account_number', 'ifsc_code', 'bank_name', 'branch_name'),
            'classes': ('collapse',)
        }),
        ('UPI', {
            'fields': ('upi_id',),
            'classes': ('collapse',)
        }),
        ('Payment Provider', {
            'fields': ('provider_key', 'provider_secret', 'provider_merchant_id', 'provider_webhook_secret'),
            'classes': ('collapse',)
        }),
        ('Verification', {
            'fields': ('is_verified', 'verified_by', 'verified_at')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['verify_selected', 'unverify_selected']
    
    def verify_selected(self, request, queryset):
        """Admin action to verify selected payment configurations"""
        updated = queryset.update(
            is_verified=True,
            verified_at=timezone.now(),
            verified_by=request.user
        )
        self.message_user(request, f'{updated} payment configuration(s) verified.')
    verify_selected.short_description = 'Verify selected payment configurations'
    
    def unverify_selected(self, request, queryset):
        """Admin action to unverify selected payment configurations"""
        updated = queryset.update(
            is_verified=False,
            verified_at=None,
            verified_by=None
        )
        self.message_user(request, f'{updated} payment configuration(s) unverified.')
    unverify_selected.short_description = 'Unverify selected payment configurations'

