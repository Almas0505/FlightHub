"""
Booking models
"""
from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid
import random
import string

class BookingStatus(models.TextChoices):
    """Booking status choices"""
    PENDING = 'PENDING', 'Pending Payment'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    TICKETED = 'TICKETED', 'Ticketed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    EXPIRED = 'EXPIRED', 'Expired'
    FAILED = 'FAILED', 'Failed'


def generate_pnr():
    """Generate 6-character PNR"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Booking(models.Model):
    """Booking model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    
    # PNR (Passenger Name Record)
    pnr = models.CharField(max_length=6, unique=True, default=generate_pnr, db_index=True)
    
    # Flight information (denormalized for performance)
    flight_id = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    departure_airport = models.CharField(max_length=3)
    arrival_airport = models.CharField(max_length=3)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
        db_index=True
    )
    
    # Pricing
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KZT')
    
    # Contact information
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional data (JSON)
    flight_data = models.JSONField(default=dict)
    metadata = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', '-created_at']),
            models.Index(fields=['status', 'expires_at']),
            models.Index(fields=['pnr']),
        ]
    
    def __str__(self):
        return f"{self.pnr} - {self.status}"
    
    def save(self, *args, **kwargs):
        """Override save to set expiry time"""
        if not self.expires_at and self.status == BookingStatus.PENDING:
            from django.conf import settings
            self.expires_at = timezone.now() + timedelta(
                minutes=settings.BOOKING_EXPIRY_MINUTES
            )
        super().save(*args, **kwargs)
    
    def is_expired(self):
        """Check if booking is expired"""
        if self.status != BookingStatus.PENDING:
            return False
        return self.expires_at and timezone.now() > self.expires_at
    
    def confirm(self):
        """Confirm booking"""
        self.status = BookingStatus.CONFIRMED
        self.confirmed_at = timezone.now()
        self.expires_at = None
        self.save()
    
    def cancel(self):
        """Cancel booking"""
        self.status = BookingStatus.CANCELLED
        self.save()
    
    def expire(self):
        """Expire booking"""
        self.status = BookingStatus.EXPIRED
        self.save()
