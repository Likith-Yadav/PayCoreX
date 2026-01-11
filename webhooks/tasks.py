from celery import shared_task
from django.utils import timezone
from django.db.models import F
from .models import WebhookDelivery
from .services import WebhookService


@shared_task
def retry_failed_webhooks():
    pending_retries = WebhookDelivery.objects.filter(
        status__in=['retrying', 'failed'],
        retry_count__lt=F('max_retries'),
        next_retry_at__lte=timezone.now()
    )

    for delivery in pending_retries:
        try:
            WebhookService.retry_webhook(delivery.id, delivery.merchant_id)
        except Exception as e:
            print(f"Error retrying webhook {delivery.id}: {e}")

