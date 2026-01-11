from django.contrib import admin
from .models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'merchant_id', 'token_type', 'last_four', 'is_active', 'created_at']
    list_filter = ['token_type', 'is_active', 'created_at']
    search_fields = ['user_id', 'merchant_id']
    readonly_fields = ['id', 'token_hash', 'encrypted_token', 'created_at', 'updated_at']

