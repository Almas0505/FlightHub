"""
Accounts admin
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """User admin"""
    list_display = [
        'email', 'username', 'first_name', 'last_name',
        'tier', 'loyalty_points', 'is_active', 'created_at'
    ]
    list_filter = ['tier', 'is_active', 'is_staff', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {
            'fields': (
                'first_name', 'last_name', 'phone', 'date_of_birth',
                'passport_number', 'nationality'
            )
        }),
        ('Address', {
            'fields': ('country', 'city', 'address', 'postal_code')
        }),
        ('Loyalty', {
            'fields': ('loyalty_points', 'tier')
        }),
        ('Preferences', {
            'fields': (
                'preferred_language', 'preferred_currency',
                'email_notifications', 'sms_notifications'
            )
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Timestamps', {
            'fields': ('last_login', 'created_at', 'last_login_at')
        }),
    )
    
    readonly_fields = ['created_at', 'last_login_at']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'password1', 'password2',
                'first_name', 'last_name', 'phone'
            ),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User profile admin"""
    list_display = [
        'user', 'seat_preference', 'meal_preference',
        'marketing_consent', 'created_at'
    ]
    list_filter = ['seat_preference', 'meal_preference', 'marketing_consent']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
