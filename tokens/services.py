from django.core.exceptions import ValidationError
from .models import Token


class TokenService:
    @staticmethod
    def store_token(user_id, merchant_id, token_value, token_type, last_four=None,
                   expiry_month=None, expiry_year=None, metadata=None):
        token_hash = Token.hash_token(token_value)
        
        existing = Token.objects.filter(
            user_id=user_id,
            merchant_id=merchant_id,
            token_hash=token_hash,
            is_active=True
        ).first()

        if existing:
            return existing

        token_obj = Token(
            user_id=user_id,
            merchant_id=merchant_id,
            token_hash=token_hash,
            token_type=token_type,
            last_four=last_four,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            metadata=metadata or {}
        )
        token_obj.encrypted_token = token_obj.encrypt_token(token_value)
        token_obj.save()
        return token_obj

    @staticmethod
    def get_token(token_id, user_id):
        try:
            token = Token.objects.get(id=token_id, user_id=user_id, is_active=True)
            return token
        except Token.DoesNotExist:
            raise ValidationError("Token not found")

    @staticmethod
    def list_tokens(user_id, merchant_id):
        return Token.objects.filter(
            user_id=user_id,
            merchant_id=merchant_id,
            is_active=True
        ).order_by('-created_at')

    @staticmethod
    def delete_token(token_id, user_id):
        try:
            token = Token.objects.get(id=token_id, user_id=user_id)
            token.is_active = False
            token.save()
            return True
        except Token.DoesNotExist:
            raise ValidationError("Token not found")

    @staticmethod
    def process_payment(token, amount, metadata):
        decrypted_token = token.decrypt_token()
        return {
            'success': True,
            'reference': f'TOKEN_{token.id}',
            'message': 'Payment processed using tokenized method'
        }

