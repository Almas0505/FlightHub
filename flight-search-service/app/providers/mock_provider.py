"""
Mock flight provider for testing and development
Генерирует реалистичные тестовые данные
"""
from typing import List
import random
from datetime import datetime, timedelta
import uuid

from app.providers.base_provider import BaseFlightProvider
from app.models.flight import (
    SearchRequest,
    Flight,
    FlightSegment,
    FlightPoint,
    Airline,
    PriceBreakdown,
    Baggage,
    CabinClass
)


class MockFlightProvider(BaseFlightProvider):
    """Mock provider with realistic test data"""
    
    # Sample airlines
    AIRLINES = [
        {"code": "KC", "name": "Air Astana"},
        {"code": "FZ", "name": "FlyDubai"},
        {"code": "EK", "name": "Emirates"},
        {"code": "QR", "name": "Qatar Airways"},
        {"code": "TK", "name": "Turkish Airlines"},
        {"code": "SU", "name": "Aeroflot"},
    ]
    
    # Sample airports
    AIRPORTS = {
        "ALA": {"name": "Almaty International", "city": "Almaty", "country": "Kazakhstan"},
        "DXB": {"name": "Dubai International", "city": "Dubai", "country": "UAE"},
        "IST": {"name": "Istanbul Airport", "city": "Istanbul", "country": "Turkey"},
        "DOH": {"name": "Hamad International", "city": "Doha", "country": "Qatar"},
        "SVO": {"name": "Sheremetyevo", "city": "Moscow", "country": "Russia"},
        "TSE": {"name": "Nursultan Nazarbayev", "city": "Astana", "country": "Kazakhstan"},
    }
    
    # Aircraft types
    AIRCRAFT_TYPES = [
        "Boeing 737-800",
        "Airbus A320",
        "Boeing 787-9",
        "Airbus A321",
        "Boeing 777-300ER",
    ]
    
    def __init__(self):
        super().__init__("mock")
    
    async def search_flights(self, search_request: SearchRequest) -> List[Flight]:
        """Generate mock flight data"""
        
        self.logger.info(
            "mock_search_started",
            from_airport=search_request.from_airport,
            to_airport=search_request.to_airport
        )
        
        flights = []
        
        # Generate 5-10 random flights
        num_flights = random.randint(5, 10)
        
        for i in range(num_flights):
            # Decide if direct or with stops
            has_stop = random.random() < 0.3 and not search_request.direct_only
            
            if has_stop:
                flight = self._generate_connecting_flight(search_request)
            else:
                flight = self._generate_direct_flight(search_request)
            
            flights.append(flight)
        
        # Sort by price
        flights.sort(key=lambda x: x.price.total)
        
        self.logger.info("mock_search_completed", flights_count=len(flights))
        
        return flights
    
    def _generate_direct_flight(self, search_request: SearchRequest) -> Flight:
        """Generate a direct flight"""
        
        airline = random.choice(self.AIRLINES)
        aircraft = random.choice(self.AIRCRAFT_TYPES)
        
        # Flight duration (random between 2-6 hours)
        duration_minutes = random.randint(120, 360)
        
        # Departure time
        departure_datetime = search_request.departure_date.replace(
            hour=random.randint(6, 22),
            minute=random.choice([0, 15, 30, 45])
        )
        
        arrival_datetime = departure_datetime + timedelta(minutes=duration_minutes)
        
        # Create segment
        segment = FlightSegment(
            id=f"SEG-{uuid.uuid4().hex[:8]}",
            airline=Airline(**airline),
            flight_number=f"{airline['code']}{random.randint(100, 999)}",
            aircraft_type=aircraft,
            departure=FlightPoint(
                airport_code=search_request.from_airport,
                airport_name=self.AIRPORTS[search_request.from_airport]["name"],
                city=self.AIRPORTS[search_request.from_airport]["city"],
                country=self.AIRPORTS[search_request.from_airport]["country"],
                terminal=f"Terminal {random.randint(1, 3)}",
                datetime=departure_datetime
            ),
            arrival=FlightPoint(
                airport_code=search_request.to_airport,
                airport_name=self.AIRPORTS[search_request.to_airport]["name"],
                city=self.AIRPORTS[search_request.to_airport]["city"],
                country=self.AIRPORTS[search_request.to_airport]["country"],
                terminal=f"Terminal {random.randint(1, 3)}",
                datetime=arrival_datetime
            ),
            duration_minutes=duration_minutes,
            cabin_class=search_request.cabin_class,
            available_seats=random.randint(5, 50),
            baggage=Baggage(),
            meal_included=random.choice([True, False]),
            wifi_available=random.choice([True, False])
        )
        
        # Generate price
        base_fare = self._generate_price(search_request.cabin_class, distance_factor=1.0)
        taxes = base_fare * 0.15
        fees = 2000.0
        
        price = PriceBreakdown(
            base_fare=base_fare,
            taxes=taxes,
            fees=fees,
            total=base_fare + taxes + fees,
            currency="KZT"
        )
        
        # Create flight
        flight = Flight(
            id=f"FL-{uuid.uuid4().hex[:12]}",
            segments=[segment],
            price=price,
            cabin_class=search_request.cabin_class,
            total_duration_minutes=duration_minutes,
            stops=0,
            refundable=random.choice([True, False]),
            changeable=True,
            change_fee=5000.0 if random.choice([True, False]) else None,
            baggage=Baggage(),
            provider="mock",
            cached_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=1),
            valid_until=departure_datetime - timedelta(hours=2)
        )
        
        return flight
    
    def _generate_connecting_flight(self, search_request: SearchRequest) -> Flight:
        """Generate a flight with one stop"""
        
        # Choose random hub
        possible_hubs = [code for code in self.AIRPORTS.keys() 
                        if code not in [search_request.from_airport, search_request.to_airport]]
        hub_code = random.choice(possible_hubs)
        
        segments = []
        
        # First segment
        airline1 = random.choice(self.AIRLINES)
        duration1 = random.randint(90, 240)
        
        departure_datetime = search_request.departure_date.replace(
            hour=random.randint(6, 18),
            minute=random.choice([0, 15, 30, 45])
        )
        arrival_datetime = departure_datetime + timedelta(minutes=duration1)
        
        segment1 = FlightSegment(
            id=f"SEG-{uuid.uuid4().hex[:8]}",
            airline=Airline(**airline1),
            flight_number=f"{airline1['code']}{random.randint(100, 999)}",
            aircraft_type=random.choice(self.AIRCRAFT_TYPES),
            departure=FlightPoint(
                airport_code=search_request.from_airport,
                airport_name=self.AIRPORTS[search_request.from_airport]["name"],
                city=self.AIRPORTS[search_request.from_airport]["city"],
                country=self.AIRPORTS[search_request.from_airport]["country"],
                terminal=f"Terminal {random.randint(1, 3)}",
                datetime=departure_datetime
            ),
            arrival=FlightPoint(
                airport_code=hub_code,
                airport_name=self.AIRPORTS[hub_code]["name"],
                city=self.AIRPORTS[hub_code]["city"],
                country=self.AIRPORTS[hub_code]["country"],
                terminal=f"Terminal {random.randint(1, 3)}",
                datetime=arrival_datetime
            ),
            duration_minutes=duration1,
            cabin_class=search_request.cabin_class,
            available_seats=random.randint(5, 50),
            baggage=Baggage(),
            meal_included=True,
            wifi_available=random.choice([True, False])
        )
        
        # Layover (1-4 hours)
        layover_minutes = random.randint(60, 240)
        
        # Second segment
        airline2 = random.choice(self.AIRLINES)
        duration2 = random.randint(90, 240)
        
        departure_datetime2 = arrival_datetime + timedelta(minutes=layover_minutes)
        arrival_datetime2 = departure_datetime2 + timedelta(minutes=duration2)
        
        segment2 = FlightSegment(
            id=f"SEG-{uuid.uuid4().hex[:8]}",
            airline=Airline(**airline2),
            flight_number=f"{airline2['code']}{random.randint(100, 999)}",
            aircraft_type=random.choice(self.AIRCRAFT_TYPES),
            departure=FlightPoint(
                airport_code=hub_code,
                airport_name=self.AIRPORTS[hub_code]["name"],
                city=self.AIRPORTS[hub_code]["city"],
                country=self.AIRPORTS[hub_code]["country"],
                terminal=f"Terminal {random.randint(1, 3)}",
                datetime=departure_datetime2
            ),
            arrival=FlightPoint(
                airport_code=search_request.to_airport,
                airport_name=self.AIRPORTS[search_request.to_airport]["name"],
                city=self.AIRPORTS[search_request.to_airport]["city"],
                country=self.AIRPORTS[search_request.to_airport]["country"],
                terminal=f"Terminal {random.randint(1, 3)}",
                datetime=arrival_datetime2
            ),
            duration_minutes=duration2,
            cabin_class=search_request.cabin_class,
            available_seats=random.randint(5, 50),
            baggage=Baggage(),
            meal_included=True,
            wifi_available=random.choice([True, False])
        )
        
        segments = [segment1, segment2]
        
        # Price (connecting flights usually cheaper)
        base_fare = self._generate_price(search_request.cabin_class, distance_factor=0.85)
        taxes = base_fare * 0.15
        fees = 2000.0
        
        price = PriceBreakdown(
            base_fare=base_fare,
            taxes=taxes,
            fees=fees,
            total=base_fare + taxes + fees,
            currency="KZT"
        )
        
        total_duration = duration1 + layover_minutes + duration2
        
        flight = Flight(
            id=f"FL-{uuid.uuid4().hex[:12]}",
            segments=segments,
            price=price,
            cabin_class=search_request.cabin_class,
            total_duration_minutes=total_duration,
            stops=1,
            refundable=False,
            changeable=True,
            change_fee=8000.0,
            baggage=Baggage(),
            provider="mock",
            cached_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=1),
            valid_until=departure_datetime - timedelta(hours=2)
        )
        
        return flight
    
    def _generate_price(self, cabin_class: CabinClass, distance_factor: float = 1.0) -> float:
        """Generate realistic price based on cabin class"""
        
        base_prices = {
            CabinClass.ECONOMY: random.randint(35000, 80000),
            CabinClass.PREMIUM_ECONOMY: random.randint(60000, 120000),
            CabinClass.BUSINESS: random.randint(150000, 350000),
            CabinClass.FIRST: random.randint(400000, 800000),
        }
        
        return base_prices[cabin_class] * distance_factor
