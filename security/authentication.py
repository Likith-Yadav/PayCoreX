import hmac
import hashlib
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from merchants.models import Merchant


class HMACAuthentication(BaseAuthentication):
    """
    REST Framework authentication class that performs HMAC authentication
    """
    
    def authenticate(self, request):
        # Skip authentication for payment pages (public pages)
        path = request.path if hasattr(request, 'path') else (request._request.path if hasattr(request, '_request') else '')
        if '/v1/payments/' in path and '/page' in path:
            return None
        
        # Get headers from the underlying Django request
        django_request = request._request if hasattr(request, '_request') else request
        
        # Get headers - Django converts X-Header-Name to HTTP_X_HEADER_NAME in META
        api_key = django_request.META.get('HTTP_X_API_KEY') or django_request.META.get('X-API-Key')
        signature = django_request.META.get('HTTP_X_SIGNATURE') or django_request.META.get('X-Signature')
        timestamp = django_request.META.get('HTTP_X_TIMESTAMP') or django_request.META.get('X-Timestamp')
        
        # If no headers, return None to allow other auth methods or AllowAny
        if not all([api_key, signature, timestamp]):
            return None
        
        # Get merchant
        try:
            merchant = Merchant.objects.get(api_key=api_key, is_active=True)
        except Merchant.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')
        
        # Get request body
        body = django_request.body.decode('utf-8') if django_request.body else ''
        payload = f"{timestamp}{body}"
        
        # Verify signature
        expected_signature = hmac.new(
            merchant.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            raise AuthenticationFailed('Invalid signature')
        
        # Return (user, auth) tuple - merchant goes in auth
        # Views can access via request.auth
        return (None, merchant)
    
    def authenticate_header(self, request):
        return 'HMAC'

