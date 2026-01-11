from django.contrib import admin
from .models import Ledger


@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ['entity', 'entity_id', 'credit', 'debit', 'balance', 'created_at']
    list_filter = ['entity', 'created_at']
    search_fields = ['entity_id', 'reference_id']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']

