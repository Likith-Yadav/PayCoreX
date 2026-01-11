from decimal import Decimal
from .models import Ledger


class LedgerService:
    @staticmethod
    def update_ledger(entity, entity_id, credit=Decimal('0'), debit=Decimal('0'), 
                     reference_type=None, reference_id=None, description=None):
        last_entry = Ledger.objects.filter(
            entity=entity,
            entity_id=entity_id
        ).order_by('-created_at').first()
        
        previous_balance = last_entry.balance if last_entry else Decimal('0')
        new_balance = previous_balance + credit - debit
        
        ledger_entry = Ledger.objects.create(
            entity=entity,
            entity_id=entity_id,
            credit=credit,
            debit=debit,
            balance=new_balance,
            reference_type=reference_type,
            reference_id=reference_id,
            description=description
        )
        return ledger_entry

    @staticmethod
    def get_balance(entity, entity_id):
        last_entry = Ledger.objects.filter(
            entity=entity,
            entity_id=entity_id
        ).order_by('-created_at').first()
        return last_entry.balance if last_entry else Decimal('0')

    @staticmethod
    def get_ledger_history(entity, entity_id, limit=100):
        return Ledger.objects.filter(
            entity=entity,
            entity_id=entity_id
        ).order_by('-created_at')[:limit]

