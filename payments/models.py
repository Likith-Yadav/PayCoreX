import uuid
from django.db import models
from django.utils import timezone
from decimal import Decimal


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    METHOD_CHOICES = [
        ('upi_intent', 'UPI Intent'),
        ('wallet', 'Wallet'),
        ('tokenized', 'Tokenized'),
        ('crypto', 'Crypto'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant_id = models.UUIDField(db_index=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    user_id = models.UUIDField(null=True, blank=True)
    reference_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    provider_reference = models.CharField(max_length=255, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    failure_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['merchant_id', 'status']),
            models.Index(fields=['reference_id']),
        ]

    def __str__(self):
        return f"Payment {self.id} - {self.amount} {self.status}"


class Refund(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_id = models.UUIDField(db_index=True)
    merchant_id = models.UUIDField(db_index=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(null=True, blank=True)
    reference_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    provider_reference = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'refunds'
        ordering = ['-created_at']

    def __str__(self):
        return f"Refund {self.id} - {self.amount} {self.status}"

