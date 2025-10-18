"""
Payment views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import logging

from .models import Payment, PaymentStatus
from .serializers import (
    PaymentSerializer,
    PaymentCreateSerializer,
    PaymentRefundSerializer,
    PaymentListSerializer
)
from .services import PaymentService

logger = logging.getLogger(__name__)


class PaymentViewSet(viewsets.ModelViewSet):
    """Payment API ViewSet"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def get_serializer_class(self):
        """Return appropriate serializer"""
        if self.action == 'create':
            return PaymentCreateSerializer
        elif self.action == 'list':
            return PaymentListSerializer
        return PaymentSerializer
    
    def get_queryset(self):
        """Filter payments by query params"""
        queryset = Payment.objects.all()
        
        # Filter by booking_id
        booking_id = self.request.query_params.get('booking_id')
        if booking_id:
            queryset = queryset.filter(booking_id=booking_id)
        
        # Filter by user_id
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def create(self, request):
        """
        Create and process payment
        
        POST /payments/
        {
            "booking_id": "uuid",
            "user_id": "uuid",
            "amount": 150000,
            "currency": "KZT",
            "payment_method": "CARD",
            "card_token": "tok_visa_4242"
        }
        """
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            payment_service = PaymentService()
            payment = payment_service.create_payment(serializer.validated_data)
            
            response_serializer = PaymentSerializer(payment)
            
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            logger.error(f"Payment creation failed: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Payment processing failed', 'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """
        Refund a payment
        
        POST /payments/{id}/refund/
        {
            "amount": 50000,  # optional, null for full refund
            "reason": "Customer request"
        }
        """
        payment = self.get_object()
        
        if payment.status != PaymentStatus.COMPLETED:
            return Response(
                {'error': f'Cannot refund payment with status {payment.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = PaymentRefundSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            payment_service = PaymentService()
            payment = payment_service.refund_payment(
                payment.id,
                amount=serializer.validated_data.get('amount'),
                reason=serializer.validated_data.get('reason', '')
            )
            
            response_serializer = PaymentSerializer(payment)
            return Response(response_serializer.data)
        
        except Exception as e:
            logger.error(f"Refund failed: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Refund failed', 'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get payment statistics
        
        GET /payments/stats/
        """
        from django.db.models import Sum, Count, Avg
        
        stats = {
            'total_payments': Payment.objects.count(),
            'completed': Payment.objects.filter(status=PaymentStatus.COMPLETED).count(),
            'failed': Payment.objects.filter(status=PaymentStatus.FAILED).count(),
            'pending': Payment.objects.filter(status=PaymentStatus.PENDING).count(),
            'total_amount': Payment.objects.filter(
                status=PaymentStatus.COMPLETED
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            'average_amount': Payment.objects.filter(
                status=PaymentStatus.COMPLETED
            ).aggregate(Avg('amount'))['amount__avg'] or 0,
        }
        
        return Response(stats)
