import requests
import json
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import WebhookEndpoint, WebhookDelivery
from utils.webhook_utils import generate_webhook_signature
from utils.crypto_utils import generate_secret
from payments.models import Payment
from payments.models import Refund


class WebhookService:
    @staticmethod
    def create_endpoint(merchant_id, url, events=None):
        secret = generate_secret()
        endpoint = WebhookEndpoint.objects.create(
            merchant_id=merchant_id,
            url=url,
            secret=secret,
            events=events or []
        )
        return endpoint, secret

    @staticmethod
    def send_payment_webhook(payment):
        endpoints = WebhookEndpoint.objects.filter(
            merchant_id=payment.merchant_id,
            is_active=True
        )
        
        if 'payment' in [e for endpoint in endpoints for e in endpoint.events] or not any(endpoint.events for endpoint in endpoints):
            for endpoint in endpoints:
                payload = {
                    'event': 'payment.success',
                    'data': {
                        'payment_id': str(payment.id),
                        'amount': str(payment.amount),
                        'status': payment.status,
                        'method': payment.method,
                        'reference_id': payment.reference_id,
                        'created_at': payment.created_at.isoformat()
                    }
                }
                WebhookService._send_webhook(endpoint, payload)

    @staticmethod
    def send_refund_webhook(refund):
        endpoints = WebhookEndpoint.objects.filter(
            merchant_id=refund.merchant_id,
            is_active=True
        )
        
        if 'refund' in [e for endpoint in endpoints for e in endpoint.events] or not any(endpoint.events for endpoint in endpoints):
            for endpoint in endpoints:
                payload = {
                    'event': 'refund.success',
                    'data': {
                        'refund_id': str(refund.id),
                        'payment_id': str(refund.payment_id),
                        'amount': str(refund.amount),
                        'status': refund.status,
                        'reference_id': refund.reference_id,
                        'created_at': refund.created_at.isoformat()
                    }
                }
                WebhookService._send_webhook(endpoint, payload)

    @staticmethod
    def _send_webhook(endpoint, payload):
        signature = generate_webhook_signature(payload, endpoint.secret)
        
        delivery = WebhookDelivery.objects.create(
            endpoint_id=endpoint.id,
            merchant_id=endpoint.merchant_id,
            event_type=payload['event'],
            payload=payload,
            signature=signature,
            status='pending'
        )

        try:
            headers = {
                'Content-Type': 'application/json',
                'X-Webhook-Signature': signature,
                'X-Webhook-Event': payload['event']
            }
            
            response = requests.post(
                endpoint.url,
                json=payload,
                headers=headers,
                timeout=10
            )

            delivery.response_code = response.status_code
            delivery.response_body = response.text[:1000]

            if response.status_code in [200, 201, 202]:
                delivery.status = 'sent'
                delivery.delivered_at = timezone.now()
            else:
                delivery.status = 'failed'
                if delivery.retry_count < delivery.max_retries:
                    delivery.status = 'retrying'
                    delivery.next_retry_at = timezone.now() + timedelta(minutes=2 ** delivery.retry_count)
                delivery.retry_count += 1

            delivery.save()
        except Exception as e:
            delivery.status = 'failed'
            delivery.response_body = str(e)[:1000]
            if delivery.retry_count < delivery.max_retries:
                delivery.status = 'retrying'
                delivery.next_retry_at = timezone.now() + timedelta(minutes=2 ** delivery.retry_count)
            delivery.retry_count += 1
            delivery.save()

    @staticmethod
    def retry_webhook(delivery_id, merchant_id):
        try:
            delivery = WebhookDelivery.objects.get(id=delivery_id, merchant_id=merchant_id)
        except WebhookDelivery.DoesNotExist:
            raise ValidationError("Webhook delivery not found")

        if delivery.status == 'sent':
            raise ValidationError("Webhook already delivered")

        try:
            endpoint = WebhookEndpoint.objects.get(id=delivery.endpoint_id)
        except WebhookEndpoint.DoesNotExist:
            raise ValidationError("Webhook endpoint not found")

        WebhookService._send_webhook(endpoint, delivery.payload)
        delivery.refresh_from_db()
        return delivery

