import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Extended User model for dashboard authentication"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.OneToOneField(
        'merchants.Merchant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='user_account'
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return self.email
