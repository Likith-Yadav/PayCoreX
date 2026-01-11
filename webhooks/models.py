import uuid
from django.db import models
from django.utils import timezone


class WebhookEndpoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant_id = models.UUIDField(db_index=True)
    url = models.URLField()
    secret = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    events = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'webhook_endpoints'

    def __str__(self):
        return f"Webhook {self.url}"


class WebhookDelivery(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('retrying', 'Retrying'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    endpoint_id = models.UUIDField(db_index=True)
    merchant_id = models.UUIDField(db_index=True)
    event_type = models.CharField(max_length=50)
    payload = models.JSONField()
    signature = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response_code = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(null=True, blank=True)
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    next_retry_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'webhook_deliveries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['endpoint_id', 'status']),
            models.Index(fields=['merchant_id', 'status']),
        ]

    def __str__(self):
        return f"Webhook {self.id} - {self.event_type} - {self.status}"

