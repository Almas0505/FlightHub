"""
Payment models
"""
from django.db import models
from django.utils import timezone
import uuid


class PaymentStatus(models.TextChoices):
    """Payment status choices"""
    PENDING = 'PENDING', 'Pending'
    PROCESSING = 'PROCESSING', 'Processing'
    COMPLETED = 'COMPLETED', 'Completed'
    FAILED = 'FAILED', 'Failed'
    REFUNDED = 'REFUNDED', 'Refunded'
    CANCELLED = 'CANCELLED', 'Cancelled'


class PaymentMethod(models.TextChoices):
    """Payment method choices"""
    CARD = 'CARD', 'Credit/Debit Card'
    KASPI = 'KASPI', 'Kaspi Pay'
    WALLET = 'WALLET', 'E-Wallet'
    BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer'


class Payment(models.Model):
    """Payment model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Booking reference
    booking_id = models.UUIDField(db_index=True)
    user_id = models.UUIDField(db_index=True)
    
    # Amount
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KZT')
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        db_index=True
    )
    
    # Payment details
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices
    )
    
    # Provider details
    provider = models.CharField(max_length=50, default='mock')
    transaction_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    provider_response = models.JSONField(default=dict, blank=True)
    
    # Card details (last 4 digits only)
    card_last4 = models.CharField(max_length=4, blank=True)
    card_brand = models.CharField(max_length=20, blank=True)
    
    # Idempotency
    idempotency_key = models.CharField(max_length=100, unique=True, db_index=True)
    
    # Refund
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    refund_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)
    
    # Error details
    error_code = models.CharField(max_length=50, blank=True)
    error_message = models.TextField(blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['booking_id', '-created_at']),
            models.Index(fields=['user_id', '-created_at']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['transaction_id']),
        ]
    
    def __str__(self):
        return f"Payment {self.id} - {self.status} - {self.amount} {self.currency}"
    
    def mark_completed(self, transaction_id):
        """Mark payment as completed"""
        self.status = PaymentStatus.COMPLETED
        self.transaction_id = transaction_id
        self.completed_at = timezone.now()
        self.save()
    
    def mark_failed(self, error_code, error_message):
        """Mark payment as failed"""
        self.status = PaymentStatus.FAILED
        self.error_code = error_code
        self.error_message = error_message
        self.failed_at = timezone.now()
        self.save()
    
    def refund(self, amount=None, reason=''):
        """Refund payment"""
        if self.status != PaymentStatus.COMPLETED:
            raise ValueError("Can only refund completed payments")
        
        refund_amount = amount or self.amount
        
        self.status = PaymentStatus.REFUNDED
        self.refund_amount = refund_amount
        self.refunded_at = timezone.now()
        self.refund_reason = reason
        self.save()


class PaymentWebhook(models.Model):
    """Payment webhook log"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='webhooks')
    
    provider = models.CharField(max_length=50)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'payment_webhooks'
        ordering = ['-created_at']
