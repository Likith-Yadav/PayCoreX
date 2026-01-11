from .models import Merchant
from utils.crypto_utils import generate_api_key, generate_secret


class MerchantService:
    @staticmethod
    def register_merchant(name, email):
        api_key = generate_api_key()
        secret = generate_secret()
        
        merchant = Merchant.objects.create(
            name=name,
            email=email,
            api_key=api_key,
            secret=secret
        )
        return merchant, secret

    @staticmethod
    def regenerate_api_key(merchant):
        api_key = generate_api_key()
        secret = generate_secret()
        
        merchant.api_key = api_key
        merchant.secret = secret
        merchant.save()
        return api_key, secret

    @staticmethod
    def get_merchant_profile(merchant):
        return {
            'id': str(merchant.id),
            'name': merchant.name,
            'email': merchant.email,
            'api_key': merchant.api_key,
            'is_active': merchant.is_active,
            'created_at': merchant.created_at.isoformat(),
        }

