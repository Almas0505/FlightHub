"""
Payment serializers
"""
from rest_framework import serializers
from .models import Payment, PaymentMethod, PaymentStatus


class PaymentCreateSerializer(serializers.Serializer):
    """Create payment serializer"""
    booking_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    currency = serializers.CharField(max_length=3, default='KZT')
    payment_method = serializers.ChoiceField(choices=PaymentMethod.choices)
    
    # Card details (for CARD method)
    card_token = serializers.CharField(required=False, allow_blank=True)
    
    # Kaspi details (for KASPI method)
    kaspi_phone = serializers.CharField(required=False, allow_blank=True)
    
    # Metadata
    metadata = serializers.JSONField(required=False, default=dict)
    
    def validate(self, data):
        """Validate payment data"""
        if data['payment_method'] == PaymentMethod.CARD:
            if not data.get('card_token'):
                raise serializers.ValidationError({
                    'card_token': 'Card token is required for card payments'
                })
        
        if data['payment_method'] == PaymentMethod.KASPI:
            if not data.get('kaspi_phone'):
                raise serializers.ValidationError({
                    'kaspi_phone': 'Phone number is required for Kaspi payments'
                })
        
        return data


class PaymentSerializer(serializers.ModelSerializer):
    """Payment model serializer"""
    
    class Meta:
        model = Payment
        fields = [
            'id', 'booking_id', 'user_id',
            'amount', 'currency',
            'status', 'payment_method',
            'provider', 'transaction_id',
            'card_last4', 'card_brand',
            'idempotency_key',
            'refund_amount', 'refunded_at', 'refund_reason',
            'created_at', 'updated_at', 'completed_at', 'failed_at',
            'error_code', 'error_message',
            'metadata'
        ]
        read_only_fields = [
            'id', 'status', 'provider', 'transaction_id',
            'card_last4', 'card_brand', 'idempotency_key',
            'created_at', 'updated_at', 'completed_at', 'failed_at',
            'error_code', 'error_message'
        ]


class PaymentRefundSerializer(serializers.Serializer):
    """Refund payment serializer"""
    amount = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False,
        allow_null=True
    )
    reason = serializers.CharField(required=False, allow_blank=True)


class PaymentListSerializer(serializers.ModelSerializer):
    """Payment list serializer (lighter version)"""
    
    class Meta:
        model = Payment
        fields = [
            'id', 'booking_id', 'amount', 'currency',
            'status', 'payment_method', 'transaction_id',
            'created_at', 'completed_at'
        ]
