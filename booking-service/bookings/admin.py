"""
Booking admin
"""
from django.contrib import admin
from .models import Booking, BookingStatus


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Booking admin"""
    list_display = [
        'pnr', 'user_id', 'flight_number',
        'departure_airport', 'arrival_airport',
        'status', 'total_amount', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'departure_time']
    search_fields = ['pnr', 'user_id', 'flight_number', 'contact_email']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'pnr', 'user_id', 'status')
        }),
        ('Flight Info', {
            'fields': (
                'flight_id', 'flight_number',
                'departure_airport', 'arrival_airport',
                'departure_time', 'arrival_time'
            )
        }),
        ('Contact', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Pricing', {
            'fields': ('total_amount', 'currency')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'expires_at', 'confirmed_at')
        }),
    )
