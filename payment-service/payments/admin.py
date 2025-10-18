"""
Payment admin
"""
from django.contrib import admin
from .models import Payment, PaymentWebhook


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Payment admin"""
    list_display = [
        'id', 'booking_id', 'amount', 'currency',
        'status', 'payment_method', 'created_at'
    ]
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['id', 'booking_id', 'transaction_id', 'idempotency_key']
    readonly_fields = ['created_at', 'updated_at', 'completed_at', 'failed_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'booking_id', 'user_id', 'status')
        }),
        ('Payment Details', {
            'fields': ('amount', 'currency', 'payment_method', 'provider')
        }),
        ('Transaction', {
            'fields': ('transaction_id', 'idempotency_key', 'card_last4', 'card_brand')
        }),
        ('Refund', {
            'fields': ('refund_amount', 'refunded_at', 'refund_reason')
        }),
        ('Error Details', {
            'fields': ('error_code', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at', 'failed_at')
        }),
    )


@admin.register(PaymentWebhook)
class PaymentWebhookAdmin(admin.ModelAdmin):
    """Payment webhook admin"""
    list_display = ['id', 'payment', 'provider', 'event_type', 'processed', 'created_at']
    list_filter = ['provider', 'processed', 'created_at']
    search_fields = ['payment__id', 'event_type']
