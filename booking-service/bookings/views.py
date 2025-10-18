"""
Booking views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
import logging

from .models import Booking, BookingStatus
from .serializers import BookingSerializer, BookingCreateSerializer
from .services import BookingService

logger = logging.getLogger(__name__)

class BookingViewSet(viewsets.ModelViewSet):
    """Booking API ViewSet"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        """Filter by user_id if provided"""
        queryset = Booking.objects.all()
        user_id = self.request.query_params.get('user_id')
        status_filter = self.request.query_params.get('status')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def create(self, request):
        """Create new booking"""
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            booking_service = BookingService()
            booking = booking_service.create_booking(serializer.validated_data)
            
            response_serializer = BookingSerializer(booking)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"Booking creation failed: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel booking"""
        booking = self.get_object()
        
        if booking.status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
            return Response(
                {'error': f'Cannot cancel booking with status {booking.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.cancel()
        
        # Publish event
        from .events import publish_booking_cancelled
        publish_booking_cancelled(booking)
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def ticket(self, request, pk=None):
        """Get ticket PDF"""
        booking = self.get_object()
        
        if booking.status != BookingStatus.TICKETED:
            return Response(
                {'error': 'Booking not ticketed yet'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Return ticket URL or PDF
        from tickets.services import TicketService
        ticket_service = TicketService()
        ticket_url = ticket_service.get_ticket_url(booking)
        
        return Response({
            'ticket_url': ticket_url,
            'booking_id': str(booking.id),
            'pnr': booking.pnr
        })
