import uuid
from django.db import models
from django.utils import timezone
from decimal import Decimal


class CryptoAddress(models.Model):
    NETWORK_CHOICES = [
        ('ethereum', 'Ethereum'),
        ('polygon', 'Polygon'),
        ('bsc', 'Binance Smart Chain'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    merchant_id = models.UUIDField(db_index=True)
    address = models.CharField(max_length=255, db_index=True)
    network = models.CharField(max_length=20, choices=NETWORK_CHOICES, default='ethereum')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'crypto_addresses'
        unique_together = ['user_id', 'merchant_id', 'network']

    def __str__(self):
        return f"{self.network}:{self.address}"


class CryptoTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_id = models.UUIDField(db_index=True, null=True, blank=True)
    merchant_id = models.UUIDField(db_index=True)
    tx_hash = models.CharField(max_length=255, unique=True, db_index=True)
    from_address = models.CharField(max_length=255)
    to_address = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=30, decimal_places=18)
    network = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    block_number = models.BigIntegerField(null=True, blank=True)
    confirmations = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crypto_transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tx_hash']),
            models.Index(fields=['payment_id', 'status']),
        ]

    def __str__(self):
        return f"{self.tx_hash} - {self.status}"

