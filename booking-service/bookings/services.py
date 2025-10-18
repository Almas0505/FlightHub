"""
Booking service - Business logic
"""
from .models import Booking, BookingStatus
from passengers.models import Passenger
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from decimal import Decimal
import logging
import httpx

logger = logging.getLogger(__name__)


class BookingService:
    """Main booking service"""
    
    def _fetch_flight_details(self, flight_id):
        """
        Fetch flight details from Flight Search Service
        
        Args:
            flight_id: Flight ID to fetch
            
        Returns:
            dict: Flight details or None if not found
        """
        flight_search_url = settings.FLIGHT_SEARCH_SERVICE_URL
        
        try:
            response = httpx.get(
                f"{flight_search_url}/flights/{flight_id}",
                timeout=5.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Flight {flight_id} not found: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to fetch flight details: {str(e)}")
            return None
    
    def create_booking(self, validated_data):
        """
        Create a new booking
        
        Args:
            validated_data: Validated data from serializer
            
        Returns:
            Booking instance
        """
        # Extract passengers data
        passengers_data = validated_data.pop('passengers')
        flight_id = validated_data.get('flight_id')
        
        # Fetch flight details from Flight Search Service
        flight_details = self._fetch_flight_details(flight_id)
        
        if not flight_details:
            raise ValueError(f"Flight {flight_id} not found")
        
        # Extract flight information
        validated_data['flight_number'] = flight_details.get('flight_number', '')
        validated_data['departure_airport'] = flight_details.get('origin', '')
        validated_data['arrival_airport'] = flight_details.get('destination', '')
        validated_data['departure_time'] = flight_details.get('departure_time')
        validated_data['arrival_time'] = flight_details.get('arrival_time')
        
        # Calculate total amount (price per passenger * number of passengers)
        price_per_passenger = Decimal(str(flight_details.get('price', 0)))
        num_passengers = len(passengers_data)
        validated_data['total_amount'] = price_per_passenger * num_passengers
        validated_data['currency'] = flight_details.get('currency', 'KZT')
        
        # Store full flight data for reference
        validated_data['flight_data'] = flight_details
        
        # Set expiry time (15 minutes from now)
        validated_data['expires_at'] = timezone.now() + timedelta(minutes=15)
        
        # Create booking
        booking = Booking.objects.create(**validated_data)
        
        logger.info(f"Booking {booking.pnr} created for flight {booking.flight_number}")
        
        # Create passengers
        for passenger_data in passengers_data:
            Passenger.objects.create(
                booking=booking,
                **passenger_data
            )
        
        # Publish event
        from .events import publish_booking_created
        publish_booking_created(booking)
        
        return booking
    
    def cancel_booking(self, booking):
        """
        Cancel a booking
        
        Args:
            booking: Booking instance
        """
        if booking.status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
            raise ValueError(f"Cannot cancel booking with status {booking.status}")
        
        booking.cancel()
        
        # Publish event
        from .events import publish_booking_cancelled
        publish_booking_cancelled(booking)
        
        logger.info(f"Booking {booking.pnr} cancelled")
        
        return booking
