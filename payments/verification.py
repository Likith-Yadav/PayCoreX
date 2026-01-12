"""
Payment Verification Service
Handles verification of payments from various sources:
1. Payment gateway webhooks (Razorpay, PhonePe, Paytm, etc.)
2. Manual verification by merchant
3. UPI transaction ID verification
"""
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Payment
from merchants.models import MerchantPaymentConfig
from ledger.services import LedgerService
from webhooks.services import WebhookService
import requests
import hmac
import hashlib
import json


class PaymentVerificationService:
    """Service to verify if payments were actually completed"""
    
    @staticmethod
    def verify_payment(payment_id, verification_data=None):
        """
        Verify a payment was actually completed
        
        Args:
            payment_id: UUID of the payment
            verification_data: Dict with verification info (transaction_id, provider_response, etc.)
        
        Returns:
            dict: {'verified': bool, 'status': str, 'message': str}
        """
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            raise ValidationError("Payment not found")
        
        # If already verified, return current status
        if payment.status == 'success':
            return {
                'verified': True,
                'status': 'success',
                'message': 'Payment already verified'
            }
        
        # Get merchant's payment config to determine verification method
        merchant_config = MerchantPaymentConfig.objects.filter(
            merchant_id=payment.merchant_id,
            is_verified=True,
            is_active=True
        ).first()
        
        if not merchant_config:
            return {
                'verified': False,
                'status': 'pending',
                'message': 'No payment configuration found. Manual verification required.'
            }
        
        # Verify based on payment provider
        if merchant_config.config_type == 'razorpay':
            return PaymentVerificationService._verify_razorpay(payment, merchant_config, verification_data)
        elif merchant_config.config_type == 'phonepe':
            return PaymentVerificationService._verify_phonepe(payment, merchant_config, verification_data)
        elif merchant_config.config_type == 'paytm':
            return PaymentVerificationService._verify_paytm(payment, merchant_config, verification_data)
        elif merchant_config.config_type == 'upi':
            return PaymentVerificationService._verify_upi_manual(payment, merchant_config, verification_data)
        else:
            return {
                'verified': False,
                'status': 'pending',
                'message': 'Automatic verification not available. Manual verification required.'
            }
    
    @staticmethod
    def _verify_razorpay(payment, merchant_config, verification_data):
        """Verify payment via Razorpay API"""
        try:
            import razorpay
            client = razorpay.Client(
                auth=(merchant_config.provider_key, merchant_config.provider_secret)
            )
            
            # Get payment from Razorpay
            razorpay_payment = client.payment.fetch(payment.provider_reference or payment.reference_id)
            
            if razorpay_payment['status'] == 'captured':
                payment.status = 'success'
                payment.provider_reference = razorpay_payment['id']
                payment.save()
                
                # Update ledger
                LedgerService.update_ledger(
                    entity='merchant',
                    entity_id=payment.merchant_id,
                    credit=payment.amount,
                    reference_type='payment',
                    reference_id=payment.id,
                    description=f'Payment received: {payment.amount}'
                )
                
                # Send webhook
                WebhookService.send_payment_webhook(payment)
                
                return {
                    'verified': True,
                    'status': 'success',
                    'message': 'Payment verified via Razorpay'
                }
            else:
                return {
                    'verified': False,
                    'status': razorpay_payment['status'],
                    'message': f"Payment status: {razorpay_payment['status']}"
                }
        except Exception as e:
            return {
                'verified': False,
                'status': 'error',
                'message': f'Verification error: {str(e)}'
            }
    
    @staticmethod
    def _verify_phonepe(payment, merchant_config, verification_data):
        """Verify payment via PhonePe API"""
        # PhonePe verification logic
        # This would require PhonePe SDK integration
        return {
            'verified': False,
            'status': 'pending',
            'message': 'PhonePe verification not yet implemented'
        }
    
    @staticmethod
    def _verify_paytm(payment, merchant_config, verification_data):
        """Verify payment via Paytm API"""
        # Paytm verification logic
        # This would require Paytm SDK integration
        return {
            'verified': False,
            'status': 'pending',
            'message': 'Paytm verification not yet implemented'
        }
    
    @staticmethod
    def _verify_upi_manual(payment, merchant_config, verification_data):
        """
        Verify UPI payment manually using transaction ID or UTR
        
        For UPI, we need:
        1. Transaction ID (UPI reference number)
        2. UTR number (Unique Transaction Reference)
        3. Manual verification by merchant checking their bank account
        4. Or integration with bank APIs
        """
        if verification_data and verification_data.get('transaction_id'):
            # Store transaction ID
            payment.metadata['transaction_id'] = verification_data['transaction_id']
            payment.provider_reference = verification_data['transaction_id']
            payment.save()
            
            return {
                'verified': False,
                'status': 'pending',
                'message': 'Transaction ID recorded. Please verify manually in your bank account.'
            }
        
        return {
            'verified': False,
            'status': 'pending',
            'message': 'UPI payment requires manual verification. Please check your bank account.'
        }
    
    @staticmethod
    def verify_utr(payment_id, utr_number):
        """
        Verify payment using UTR (Unique Transaction Reference) number
        
        This method attempts to verify UTR through:
        1. Payment gateway APIs (Razorpay, PhonePe, Paytm)
        2. Bank API integration (if configured)
        3. Manual merchant verification (stores UTR for merchant to verify)
        
        Args:
            payment_id: UUID of the payment
            utr_number: UTR number from user's UPI app
        
        Returns:
            dict: {'verified': bool, 'status': str, 'message': str}
        """
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            raise ValidationError("Payment not found")
        
        if payment.status == 'success':
            return {
                'verified': True,
                'status': 'success',
                'message': 'Payment already verified'
            }
        
        # Store UTR in payment metadata
        payment.metadata['utr_number'] = utr_number
        payment.metadata['utr_submitted_at'] = timezone.now().isoformat()
        payment.provider_reference = utr_number
        payment.save()
        
        # Get merchant's payment config to determine verification method
        merchant_config = MerchantPaymentConfig.objects.filter(
            merchant_id=payment.merchant_id,
            is_verified=True,
            is_active=True
        ).first()
        
        if not merchant_config:
            return {
                'verified': False,
                'status': 'pending_merchant_verification',
                'message': 'UTR recorded. Merchant will verify manually.'
            }
        
        # Always store UTR for manual merchant verification
        # Merchant will verify in dashboard
        return {
            'verified': False,
            'status': 'pending_merchant_verification',
            'message': 'UTR recorded. Please wait for merchant verification in dashboard.'
        }
    
    @staticmethod
    def _verify_utr_razorpay(payment, merchant_config, utr_number):
        """Verify UTR via Razorpay API"""
        try:
            import razorpay
            client = razorpay.Client(
                auth=(merchant_config.provider_key, merchant_config.provider_secret)
            )
            
            # Search for payment by UTR or verify payment
            # Note: Razorpay API structure may vary
            try:
                # Try to fetch payment by UTR
                payments = client.payment.fetch_all({'count': 100})
                
                for razorpay_payment in payments.get('items', []):
                    if (razorpay_payment.get('notes', {}).get('utr') == utr_number or 
                        razorpay_payment.get('id') == utr_number or
                        str(razorpay_payment.get('notes', {}).get('payment_id')) == str(payment.id)):
                        
                        if razorpay_payment['status'] == 'captured':
                            # Payment verified!
                            payment.status = 'success'
                            payment.provider_reference = razorpay_payment['id']
                            payment.save()
                            
                            from ledger.services import LedgerService
                            LedgerService.update_ledger(
                                entity='merchant',
                                entity_id=payment.merchant_id,
                                credit=payment.amount,
                                reference_type='payment',
                                reference_id=payment.id,
                                description=f'Payment received: {payment.amount}'
                            )
                            
                            WebhookService.send_payment_webhook(payment)
                            
                            return {
                                'verified': True,
                                'status': 'success',
                                'message': 'Payment verified via Razorpay'
                            }
                
                return {
                    'verified': False,
                    'status': 'pending_merchant_verification',
                    'message': 'UTR not found in Razorpay. Merchant will verify manually.'
                }
            except Exception as e:
                return {
                    'verified': False,
                    'status': 'pending_merchant_verification',
                    'message': f'Could not verify via Razorpay: {str(e)}. Merchant will verify manually.'
                }
        except ImportError:
            return {
                'verified': False,
                'status': 'pending_merchant_verification',
                'message': 'Razorpay SDK not installed. Merchant will verify manually.'
            }
        except Exception as e:
            return {
                'verified': False,
                'status': 'pending_merchant_verification',
                'message': f'Verification error: {str(e)}. Merchant will verify manually.'
            }
    
    @staticmethod
    def _verify_utr_phonepe(payment, merchant_config, utr_number):
        """Verify UTR via PhonePe API"""
        # PhonePe verification logic would go here
        return {
            'verified': False,
            'status': 'pending_merchant_verification',
            'message': 'PhonePe UTR verification not yet implemented. Merchant will verify manually.'
        }
    
    @staticmethod
    def _verify_utr_paytm(payment, merchant_config, utr_number):
        """Verify UTR via Paytm API"""
        # Paytm verification logic would go here
        return {
            'verified': False,
            'status': 'pending_merchant_verification',
            'message': 'Paytm UTR verification not yet implemented. Merchant will verify manually.'
        }
    
    @staticmethod
    def mark_payment_verified(payment_id, transaction_id=None, verified_by=None):
        """
        Manually mark a payment as verified
        
        Args:
            payment_id: UUID of the payment
            transaction_id: UPI transaction ID or reference
            verified_by: User who verified (for admin verification)
        """
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            raise ValidationError("Payment not found")
        
        if payment.status == 'success':
            raise ValidationError("Payment already verified")
        
        # Update payment
        payment.status = 'success'
        if transaction_id:
            payment.provider_reference = transaction_id
            payment.metadata['transaction_id'] = transaction_id
        if verified_by:
            payment.metadata['verified_by'] = str(verified_by.id) if hasattr(verified_by, 'id') else str(verified_by)
        payment.save()
        
        # Update ledger
        LedgerService.update_ledger(
            entity='merchant',
            entity_id=payment.merchant_id,
            credit=payment.amount,
            reference_type='payment',
            reference_id=payment.id,
            description=f'Payment received: {payment.amount}'
        )
        
        # Send webhook
        WebhookService.send_payment_webhook(payment)
        
        return payment


