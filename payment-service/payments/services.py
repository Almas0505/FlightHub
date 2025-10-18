"""
Payment service - Business logic
"""
from .models import Payment, PaymentStatus, PaymentMethod
from .providers import MockPaymentProvider, StripeProvider, KaspiProvider
import uuid
import logging

logger = logging.getLogger(__name__)


class PaymentService:
    """Main payment service"""
    
    def __init__(self):
        """Initialize payment providers"""
        self.providers = {
            'mock': MockPaymentProvider(),
            'stripe': StripeProvider(),
            'kaspi': KaspiProvider(),
        }
    
    def create_payment(self, data):
        """
        Create and process payment
        
        Args:
            data: Payment data from serializer
            
        Returns:
            Payment instance
        """
        # Generate idempotency key
        idempotency_key = str(uuid.uuid4())
        
        # Check for duplicate payment
        existing = Payment.objects.filter(
            booking_id=data['booking_id'],
            status__in=[PaymentStatus.COMPLETED, PaymentStatus.PROCESSING]
        ).first()
        
        if existing:
            logger.warning(f"Duplicate payment attempt for booking {data['booking_id']}")
            return existing
        
        # Create payment record
        payment = Payment.objects.create(
            booking_id=data['booking_id'],
            user_id=data['user_id'],
            amount=data['amount'],
            currency=data.get('currency', 'KZT'),
            payment_method=data['payment_method'],
            idempotency_key=idempotency_key,
            metadata=data.get('metadata', {}),
            status=PaymentStatus.PROCESSING
        )
        
        logger.info(f"Payment {payment.id} created for booking {payment.booking_id}")
        
        # Select provider
        provider = self._select_provider(data['payment_method'])
        
        try:
            # Process payment
            result = provider.process_payment(payment, data)
            
            if result['success']:
                payment.mark_completed(result['transaction_id'])
                payment.card_last4 = result.get('card_last4', '')
                payment.card_brand = result.get('card_brand', '')
                payment.provider_response = result
                payment.save()
                
                logger.info(f"Payment {payment.id} completed successfully")
                
                # Publish event
                self._publish_payment_completed(payment)
            else:
                payment.mark_failed(
                    result.get('error_code', 'UNKNOWN'),
                    result.get('error_message', 'Payment failed')
                )
                logger.error(f"Payment {payment.id} failed: {result.get('error_message')}")
        
        except Exception as e:
            payment.mark_failed('EXCEPTION', str(e))
            logger.error(f"Payment {payment.id} exception: {str(e)}", exc_info=True)
        
        return payment
    
    def refund_payment(self, payment_id, amount=None, reason=''):
        """
        Refund a payment
        
        Args:
            payment_id: Payment UUID
            amount: Refund amount (None for full refund)
            reason: Refund reason
            
        Returns:
            Payment instance
        """
        payment = Payment.objects.get(id=payment_id)
        
        if payment.status != PaymentStatus.COMPLETED:
            raise ValueError("Can only refund completed payments")
        
        # Select provider
        provider = self._select_provider(payment.payment_method)
        
        try:
            # Process refund
            result = provider.refund_payment(payment, amount)
            
            if result['success']:
                payment.refund(amount=amount, reason=reason)
                logger.info(f"Payment {payment.id} refunded")
                
                # Publish event
                self._publish_payment_refunded(payment)
            else:
                logger.error(f"Refund failed for payment {payment.id}")
                raise Exception(result.get('error_message', 'Refund failed'))
        
        except Exception as e:
            logger.error(f"Refund exception for payment {payment.id}: {str(e)}")
            raise
        
        return payment
    
    def _select_provider(self, payment_method):
        """Select payment provider based on method"""
        # For demo, always use mock provider
        # In production, route based on payment method
        return self.providers['mock']
    
    def _publish_payment_completed(self, payment):
        """Publish payment.completed event"""
        try:
            from .events import publish_payment_completed
            publish_payment_completed(payment)
        except Exception as e:
            logger.error(f"Failed to publish payment.completed: {str(e)}")
    
    def _publish_payment_refunded(self, payment):
        """Publish payment.refunded event"""
        try:
            from .events import publish_payment_refunded
            publish_payment_refunded(payment)
        except Exception as e:
            logger.error(f"Failed to publish payment.refunded: {str(e)}")
