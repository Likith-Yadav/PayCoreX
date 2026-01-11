from decimal import Decimal
from django.core.exceptions import ValidationError
from .models import Wallet
from ledger.services import LedgerService


class WalletService:
    @staticmethod
    def create_wallet(user_id, merchant_id):
        wallet, created = Wallet.objects.get_or_create(
            user_id=user_id,
            merchant_id=merchant_id,
            defaults={'balance': Decimal('0')}
        )
        return wallet

    @staticmethod
    def topup_wallet(wallet_id, amount, merchant_id):
        try:
            wallet = Wallet.objects.get(id=wallet_id, merchant_id=merchant_id)
        except Wallet.DoesNotExist:
            raise ValidationError("Wallet not found")

        wallet.balance += Decimal(str(amount))
        wallet.save()

        LedgerService.update_ledger(
            entity='wallet',
            entity_id=wallet.id,
            credit=Decimal(str(amount)),
            reference_type='topup',
            description=f'Wallet topup: {amount}'
        )
        return wallet

    @staticmethod
    def pay_from_wallet(wallet_id, amount, merchant_id, reference_id=None):
        try:
            wallet = Wallet.objects.get(id=wallet_id, merchant_id=merchant_id)
        except Wallet.DoesNotExist:
            raise ValidationError("Wallet not found")

        amount_decimal = Decimal(str(amount))
        if wallet.balance < amount_decimal:
            raise ValidationError("Insufficient funds")

        wallet.balance -= amount_decimal
        wallet.save()

        LedgerService.update_ledger(
            entity='wallet',
            entity_id=wallet.id,
            debit=amount_decimal,
            reference_type='payment',
            reference_id=reference_id,
            description=f'Wallet payment: {amount}'
        )
        return wallet

    @staticmethod
    def get_balance(wallet_id, merchant_id):
        try:
            wallet = Wallet.objects.get(id=wallet_id, merchant_id=merchant_id)
            return wallet.balance
        except Wallet.DoesNotExist:
            raise ValidationError("Wallet not found")

    @staticmethod
    def refund_to_wallet(wallet_id, amount, merchant_id, reference_id=None):
        try:
            wallet = Wallet.objects.get(id=wallet_id, merchant_id=merchant_id)
        except Wallet.DoesNotExist:
            raise ValidationError("Wallet not found")

        amount_decimal = Decimal(str(amount))
        wallet.balance += amount_decimal
        wallet.save()

        LedgerService.update_ledger(
            entity='wallet',
            entity_id=wallet.id,
            credit=amount_decimal,
            reference_type='refund',
            reference_id=reference_id,
            description=f'Wallet refund: {amount}'
        )
        return wallet

