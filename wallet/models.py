import uuid
from django.db import models
from django.utils import timezone
from decimal import Decimal


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    merchant_id = models.UUIDField(db_index=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0'))
    currency = models.CharField(max_length=3, default='INR')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wallets'
        unique_together = ['user_id', 'merchant_id']
        indexes = [
            models.Index(fields=['user_id', 'merchant_id']),
        ]

    def __str__(self):
        return f"Wallet {self.id} - {self.balance}"

