"""
User models
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    """Custom User model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Remove username, use email instead
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, db_index=True)
    
    # Additional fields
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Passport info
    passport_number = models.CharField(max_length=20, blank=True)
    passport_expiry = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=3, blank=True)  # ISO 3166-1 alpha-3
    
    # Address
    country = models.CharField(max_length=2, blank=True)  # ISO 3166-1 alpha-2
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Loyalty program
    loyalty_points = models.IntegerField(default=0)
    tier = models.CharField(
        max_length=20,
        choices=[
            ('BRONZE', 'Bronze'),
            ('SILVER', 'Silver'),
            ('GOLD', 'Gold'),
            ('PLATINUM', 'Platinum'),
        ],
        default='BRONZE'
    )
    
    # Preferences
    preferred_language = models.CharField(max_length=2, default='en')
    preferred_currency = models.CharField(max_length=3, default='KZT')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['tier']),
        ]
    
    def __str__(self):
        return f"{self.email} - {self.get_full_name()}"
    
    def add_loyalty_points(self, points):
        """Add loyalty points and update tier"""
        self.loyalty_points += points
        
        # Update tier based on points
        if self.loyalty_points >= 50000:
            self.tier = 'PLATINUM'
        elif self.loyalty_points >= 25000:
            self.tier = 'GOLD'
        elif self.loyalty_points >= 10000:
            self.tier = 'SILVER'
        else:
            self.tier = 'BRONZE'
        
        self.save()


class UserProfile(models.Model):
    """Extended user profile"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Travel preferences
    seat_preference = models.CharField(
        max_length=20,
        choices=[
            ('WINDOW', 'Window'),
            ('AISLE', 'Aisle'),
            ('MIDDLE', 'Middle'),
            ('NO_PREFERENCE', 'No Preference'),
        ],
        default='NO_PREFERENCE'
    )
    
    meal_preference = models.CharField(
        max_length=20,
        choices=[
            ('REGULAR', 'Regular'),
            ('VEGETARIAN', 'Vegetarian'),
            ('VEGAN', 'Vegan'),
            ('HALAL', 'Halal'),
            ('KOSHER', 'Kosher'),
            ('GLUTEN_FREE', 'Gluten Free'),
        ],
        default='REGULAR'
    )
    
    special_assistance = models.TextField(blank=True)
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    
    # Marketing
    marketing_consent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"Profile of {self.user.email}"
