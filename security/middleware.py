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
        '/v1/payments/',  # Payment pages are public
    ]

    def process_request(self, request):
        if any(request.path.startswith(path) for path in self.EXEMPT_PATHS):
            return None

        # Django uses META for headers, with HTTP_ prefix and underscores converted to hyphens
        api_key = request.META.get('HTTP_X_API_KEY') or request.META.get('X-API-Key')
        signature = request.META.get('HTTP_X_SIGNATURE') or request.META.get('X-Signature')
        timestamp = request.META.get('HTTP_X_TIMESTAMP') or request.META.get('X-Timestamp')

        # Debug: log available META keys
        import logging
        logger = logging.getLogger(__name__)
        relevant_keys = [k for k in request.META.keys() if 'API' in k.upper() or 'SIGNATURE' in k.upper() or 'TIMESTAMP' in k.upper()]
        logger.debug(f"HMAC Middleware - Path: {request.path}, Relevant META keys: {relevant_keys}")
        logger.debug(f"HMAC Middleware - api_key: {bool(api_key)}, signature: {bool(signature)}, timestamp: {bool(timestamp)}")

        if not all([api_key, signature, timestamp]):
            logger.warning(f"HMAC Middleware - Missing headers for {request.path}")
            return JsonResponse({'error': 'Missing authentication headers'}, status=401)

        try:
            merchant = Merchant.objects.get(api_key=api_key, is_active=True)
        except Merchant.DoesNotExist:
            return JsonResponse({'error': 'Invalid API key', 'debug': f'API key: {api_key[:10]}...'}, status=401)

        body = request.body.decode('utf-8') if request.body else ''
        payload = f"{timestamp}{body}"

        expected_signature = hmac.new(
            merchant.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"HMAC Middleware - Signature mismatch. Received: {signature[:20]}..., Expected: {expected_signature[:20]}..., Payload: {payload[:50]}")
            return JsonResponse({
                'error': 'Invalid signature',
                'debug': {
                    'received': signature[:20],
                    'expected': expected_signature[:20],
                    'payload': payload[:50]
                }
            }, status=401)

        # Signature verified - set merchant on request object
        # This is the Django WSGIRequest - REST Framework will wrap it but _request points here
        request.merchant = merchant
        
        # Verify it was set
        import logging
        logger = logging.getLogger(__name__)
        if hasattr(request, 'merchant'):
            logger.info(f"HMAC Middleware - SUCCESS: Merchant {merchant.id} set for {request.path}")
        else:
            logger.error(f"HMAC Middleware - ERROR: Failed to set merchant attribute on request!")
            # Try alternative method
            setattr(request, 'merchant', merchant)
            logger.info(f"HMAC Middleware - Used setattr, now has merchant: {hasattr(request, 'merchant')}")
        
        return None

