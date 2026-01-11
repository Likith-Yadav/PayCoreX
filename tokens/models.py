import uuid
from django.db import models
from django.utils import timezone
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import hashlib


class Token(models.Model):
    TYPE_CHOICES = [
        ('card', 'Card'),
        ('bank_account', 'Bank Account'),
        ('upi', 'UPI'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    merchant_id = models.UUIDField(db_index=True)
    token_hash = models.CharField(max_length=255, db_index=True)
    encrypted_token = models.TextField()
    token_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    last_four = models.CharField(max_length=4, null=True, blank=True)
    expiry_month = models.IntegerField(null=True, blank=True)
    expiry_year = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tokens'
        indexes = [
            models.Index(fields=['user_id', 'merchant_id']),
        ]

    def __str__(self):
        return f"Token {self.id} - {self.token_type}"

    @staticmethod
    def _get_encryption_key():
        key = getattr(settings, 'TOKEN_ENCRYPTION_KEY', None)
        if not key:
            key = Fernet.generate_key().decode()
        return key.encode() if isinstance(key, str) else key

    def encrypt_token(self, token_value):
        key = self._get_encryption_key()
        f = Fernet(key)
        return f.encrypt(token_value.encode()).decode()

    def decrypt_token(self):
        key = self._get_encryption_key()
        f = Fernet(key)
        return f.decrypt(self.encrypted_token.encode()).decode()

    @staticmethod
    def hash_token(token_value):
        return hashlib.sha256(token_value.encode()).hexdigest()

