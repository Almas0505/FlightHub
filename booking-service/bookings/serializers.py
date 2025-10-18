"""
Booking serializers
"""
from rest_framework import serializers
from .models import Booking, BookingStatus
from passengers.models import Passenger

class PassengerSerializer(serializers.Serializer):
    """Passenger data serializer"""
    title = serializers.ChoiceField(choices=['MR', 'MS', 'MRS'])
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()
    passport_number = serializers.CharField(max_length=20)
    nationality = serializers.CharField(max_length=3)

class BookingCreateSerializer(serializers.Serializer):
    """Create booking serializer"""
    user_id = serializers.UUIDField()
    flight_id = serializers.CharField()
    passengers = PassengerSerializer(many=True)
    contact_email = serializers.EmailField()
    contact_phone = serializers.CharField()
    
    def validate_passengers(self, value):
        if len(value) < 1 or len(value) > 9:
            raise serializers.ValidationError("1-9 passengers allowed")
        return value

class BookingSerializer(serializers.ModelSerializer):
    """Booking model serializer"""
    passengers = PassengerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'pnr', 'user_id', 'status',
            'flight_id', 'flight_number',
            'departure_airport', 'arrival_airport',
            'departure_time', 'arrival_time',
            'total_amount', 'currency',
            'contact_email', 'contact_phone',
            'passengers', 'created_at', 'expires_at'
        ]
        read_only_fields = ['id', 'pnr', 'created_at']
