import uuid
from decimal import Decimal
from django.core.exceptions import ValidationError
from .models import Payment, Refund
from ledger.services import LedgerService
from wallet.services import WalletService
from tokens.services import TokenService
from crypto.services import CryptoService
from webhooks.services import WebhookService


class PaymentOrchestrator:
    @staticmethod
    def create_payment(merchant_id, amount, method, currency='INR', user_id=None, 
                      reference_id=None, metadata=None):
        payment = Payment.objects.create(
            merchant_id=merchant_id,
            amount=Decimal(str(amount)),
            currency=currency,
            method=method,
            user_id=user_id,
            reference_id=reference_id or str(uuid.uuid4()),
            metadata=metadata or {}
        )
        return payment

    @staticmethod
    def process_payment(payment):
        payment.status = 'processing'
        payment.save()

        try:
            if payment.method == 'wallet':
                result = PaymentOrchestrator._process_wallet_payment(payment)
            elif payment.method == 'tokenized':
                result = PaymentOrchestrator._process_tokenized_payment(payment)
            elif payment.method == 'upi_intent':
                result = PaymentOrchestrator._process_upi_payment(payment)
            elif payment.method == 'crypto':
                result = PaymentOrchestrator._process_crypto_payment(payment)
            else:
                raise ValidationError(f"Unsupported payment method: {payment.method}")

            if result['success']:
                payment.status = 'success'
                payment.provider_reference = result.get('reference')
                payment.save()

                LedgerService.update_ledger(
                    entity='merchant',
                    entity_id=payment.merchant_id,
                    credit=payment.amount,
                    reference_type='payment',
                    reference_id=payment.id,
                    description=f'Payment received: {payment.amount}'
                )

                WebhookService.send_payment_webhook(payment)
            else:
                payment.status = 'failed'
                payment.failure_reason = result.get('error', 'Payment processing failed')
                payment.save()

        except Exception as e:
            payment.status = 'failed'
            payment.failure_reason = str(e)
            payment.save()
            raise

        return payment

    @staticmethod
    def _process_wallet_payment(payment):
        if not payment.user_id:
            return {'success': False, 'error': 'user_id required for wallet payment'}
        
        try:
            wallet = WalletService.create_wallet(payment.user_id, payment.merchant_id)
            WalletService.pay_from_wallet(
                wallet.id,
                payment.amount,
                payment.merchant_id,
                payment.id
            )
            return {'success': True, 'reference': str(wallet.id)}
        except ValidationError as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def _process_tokenized_payment(payment):
        if not payment.user_id:
            return {'success': False, 'error': 'user_id required for tokenized payment'}
        
        token_id = payment.metadata.get('token_id')
        if not token_id:
            return {'success': False, 'error': 'token_id required in metadata'}

        try:
            token = TokenService.get_token(token_id, payment.user_id)
            result = TokenService.process_payment(token, payment.amount, payment.metadata)
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def _process_upi_payment(payment):
        upi_id = payment.metadata.get('upi_id')
        if not upi_id:
            return {'success': False, 'error': 'upi_id required in metadata'}
        
        return {'success': True, 'reference': f'UPI_{payment.id}'}

    @staticmethod
    def _process_crypto_payment(payment):
        address = payment.metadata.get('crypto_address')
        if not address:
            return {'success': False, 'error': 'crypto_address required in metadata'}
        
        try:
            result = CryptoService.create_payment_address(payment.id, address, payment.amount)
            return {'success': True, 'reference': result.get('address')}
        except Exception as e:
            return {'success': False, 'error': str(e)}


class RefundService:
    @staticmethod
    def create_refund(payment_id, merchant_id, amount=None, reason=None):
        try:
            payment = Payment.objects.get(id=payment_id, merchant_id=merchant_id)
        except Payment.DoesNotExist:
            raise ValidationError("Payment not found")

        if payment.status != 'success':
            raise ValidationError("Can only refund successful payments")

        refund_amount = Decimal(str(amount)) if amount else payment.amount
        if refund_amount > payment.amount:
            raise ValidationError("Refund amount cannot exceed payment amount")

        existing_refunds = Refund.objects.filter(
            payment_id=payment_id,
            status__in=['pending', 'processing', 'success']
        )
        total_refunded = sum(r.amount for r in existing_refunds)
        
        if total_refunded + refund_amount > payment.amount:
            raise ValidationError("Total refund amount cannot exceed payment amount")

        refund = Refund.objects.create(
            payment_id=payment_id,
            merchant_id=merchant_id,
            amount=refund_amount,
            reason=reason,
            reference_id=str(uuid.uuid4())
        )

        refund.status = 'processing'
        refund.save()

        try:
            if payment.method == 'wallet':
                wallet = WalletService.create_wallet(payment.user_id, merchant_id)
                WalletService.refund_to_wallet(wallet.id, refund_amount, merchant_id, refund.id)
            
            refund.status = 'success'
            refund.save()

            LedgerService.update_ledger(
                entity='merchant',
                entity_id=merchant_id,
                debit=refund_amount,
                reference_type='refund',
                reference_id=refund.id,
                description=f'Refund processed: {refund_amount}'
            )

            WebhookService.send_refund_webhook(refund)
        except Exception as e:
            refund.status = 'failed'
            refund.save()
            raise

        return refund

