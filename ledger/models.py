import uuid
from django.db import models
from django.utils import timezone


class Ledger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity = models.CharField(max_length=50, db_index=True)
    entity_id = models.UUIDField(db_index=True)
    credit = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    debit = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    reference_type = models.CharField(max_length=50, null=True, blank=True)
    reference_id = models.UUIDField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'ledgers'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['entity', 'entity_id']),
        ]

    def __str__(self):
        return f"{self.entity}:{self.entity_id} - {self.balance}"

