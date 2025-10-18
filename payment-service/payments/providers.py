"""
Payment providers (Stripe, Kaspi, Mock)
"""
import random
import uuid
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BasePaymentProvider(ABC):
    """Base payment provider"""
    
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def process_payment(self, payment, data):
        """Process payment"""
        pass
    
    @abstractmethod
    def refund_payment(self, payment, amount=None):
        """Refund payment"""
        pass


class MockPaymentProvider(BasePaymentProvider):
    """Mock payment provider for testing"""
    
    def __init__(self):
        super().__init__('mock')
    
    def process_payment(self, payment, data):
        """
        Simulate payment processing
        90% success rate
        """
        logger.info(f"[MOCK] Processing payment {payment.id}")
        
        # Simulate processing delay
        import time
        time.sleep(0.1)
        
        # 90% success rate
        success = random.random() < 0.9
        
        if success:
            transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
            
            result = {
                'success': True,
                'transaction_id': transaction_id,
                'provider': 'mock',
                'message': 'Payment processed successfully',
            }
            
            # Add card details if card payment
            if data.get('card_token'):
                result['card_last4'] = '4242'
                result['card_brand'] = 'Visa'
            
            logger.info(f"[MOCK] Payment {payment.id} succeeded: {transaction_id}")
            return result
        
        else:
            error_messages = [
                'Insufficient funds',
                'Card declined',
                'Invalid card number',
                'Transaction limit exceeded',
            ]
            
            result = {
                'success': False,
                'error_code': 'PAYMENT_DECLINED',
                'error_message': random.choice(error_messages),
                'provider': 'mock'
            }
            
            logger.warning(f"[MOCK] Payment {payment.id} failed: {result['error_message']}")
            return result
    
    def refund_payment(self, payment, amount=None):
        """Simulate refund"""
        logger.info(f"[MOCK] Refunding payment {payment.id}")
        
        refund_amount = amount or payment.amount
        
        # Always succeed for mock
        return {
            'success': True,
            'refund_id': f"RFD-{uuid.uuid4().hex[:12].upper()}",
            'refund_amount': float(refund_amount),
            'provider': 'mock'
        }


class StripeProvider(BasePaymentProvider):
    """Stripe payment provider"""
    
    def __init__(self):
        super().__init__('stripe')
        # In production, initialize with API key
        # import stripe
        # stripe.api_key = settings.STRIPE_API_KEY
    
    def process_payment(self, payment, data):
        """Process payment via Stripe"""
        # TODO: Implement real Stripe integration
        logger.warning("[STRIPE] Not implemented, using mock")
        return MockPaymentProvider().process_payment(payment, data)
    
    def refund_payment(self, payment, amount=None):
        """Refund payment via Stripe"""
        # TODO: Implement real Stripe refund
        logger.warning("[STRIPE] Refund not implemented, using mock")
        return MockPaymentProvider().refund_payment(payment, amount)


class KaspiProvider(BasePaymentProvider):
    """Kaspi Pay provider"""
    
    def __init__(self):
        super().__init__('kaspi')
    
    def process_payment(self, payment, data):
        """Process payment via Kaspi"""
        # TODO: Implement Kaspi integration
        logger.warning("[KASPI] Not implemented, using mock")
        return MockPaymentProvider().process_payment(payment, data)
    
    def refund_payment(self, payment, amount=None):
        """Refund payment via Kaspi"""
        # TODO: Implement Kaspi refund
        logger.warning("[KASPI] Refund not implemented, using mock")
        return MockPaymentProvider().refund_payment(payment, amount)
