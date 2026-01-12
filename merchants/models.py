import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings


class Merchant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    api_key = models.CharField(max_length=255, unique=True, db_index=True)
    secret = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'merchants'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class MerchantPaymentConfig(models.Model):
    """Merchant payment receiving configurations"""
    
    TYPE_CHOICES = [
        ('bank_account', 'Bank Account'),
        ('upi', 'UPI'),
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
        ('phonepe', 'PhonePe'),
        ('paytm', 'Paytm'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        related_name='payment_configs'
    )
    config_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Bank Account Fields
    account_holder_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    ifsc_code = models.CharField(max_length=11, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    branch_name = models.CharField(max_length=255, null=True, blank=True)
    
    # UPI Fields
    upi_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Payment Provider Fields
    provider_key = models.CharField(max_length=255, null=True, blank=True)  # API Key
    provider_secret = models.CharField(max_length=255, null=True, blank=True)  # Secret Key
    provider_merchant_id = models.CharField(max_length=255, null=True, blank=True)
    provider_webhook_secret = models.CharField(max_length=255, null=True, blank=True)
    
    # Additional metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_payment_configs',
        help_text='Admin user who verified this payment configuration'
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'merchant_payment_configs'
        ordering = ['-is_primary', '-created_at']
        indexes = [
            models.Index(fields=['merchant', 'config_type']),
            models.Index(fields=['merchant', 'is_primary']),
        ]
    
    def __str__(self):
        if self.config_type == 'bank_account':
            return f"Bank Account - {self.bank_name} ({self.account_number[-4:] if self.account_number else 'N/A'})"
        elif self.config_type == 'upi':
            return f"UPI - {self.upi_id}"
        else:
            return f"{self.get_config_type_display()} - {self.provider_merchant_id or 'N/A'}"
    
    def save(self, *args, **kwargs):
        # Ensure only one primary config per type per merchant
        if self.is_primary:
            MerchantPaymentConfig.objects.filter(
                merchant=self.merchant,
                config_type=self.config_type,
                is_primary=True
            ).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)

