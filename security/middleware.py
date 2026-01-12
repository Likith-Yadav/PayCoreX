import hmac
import hashlib
import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from merchants.models import Merchant


class HMACAuthMiddleware(MiddlewareMixin):
    EXEMPT_PATHS = [
        '/v1/merchants/register',
        '/api/auth/',
        '/api/dashboard/',
        '/admin/',
        '/',
        '/favicon.ico',
        '/static/',
        '/media/',
    ]

    def process_request(self, request):
        if any(request.path.startswith(path) for path in self.EXEMPT_PATHS):
            return None

        api_key = request.headers.get('X-API-Key')
        signature = request.headers.get('X-Signature')
        timestamp = request.headers.get('X-Timestamp')

        if not all([api_key, signature, timestamp]):
            return JsonResponse({'error': 'Missing authentication headers'}, status=401)

        try:
            merchant = Merchant.objects.get(api_key=api_key, is_active=True)
        except Merchant.DoesNotExist:
            return JsonResponse({'error': 'Invalid API key'}, status=401)

        body = request.body.decode('utf-8') if request.body else ''
        payload = f"{timestamp}{body}"

        expected_signature = hmac.new(
            merchant.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            return JsonResponse({'error': 'Invalid signature'}, status=401)

        request.merchant = merchant
        return None

