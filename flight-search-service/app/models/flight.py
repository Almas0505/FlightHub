"""
Pydantic models for Flight data
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class CabinClass(str, Enum):
    """Cabin class options"""
    ECONOMY = "economy"
    PREMIUM_ECONOMY = "premium_economy"
    BUSINESS = "business"
    FIRST = "first"


class Airport(BaseModel):
    """Airport information"""
    code: str = Field(..., min_length=3, max_length=3, description="IATA code")
    name: str
    city: str
    country: str
    terminal: Optional[str] = None


class Airline(BaseModel):
    """Airline information"""
    code: str = Field(..., min_length=2, max_length=3)
    name: str
    logo_url: Optional[str] = None


class FlightPoint(BaseModel):
    """Departure or arrival point"""
    airport_code: str = Field(..., min_length=3, max_length=3)
    airport_name: str
    city: str
    country: str
    terminal: Optional[str] = None
    datetime: datetime


class Baggage(BaseModel):
    """Baggage allowance"""
    cabin: str = "1 x 8kg"
    checked: str = "1 x 23kg"


class FlightSegment(BaseModel):
    """Single flight segment"""
    id: str
    airline: Airline
    flight_number: str
    aircraft_type: str
    
    departure: FlightPoint
    arrival: FlightPoint
    
    duration_minutes: int
    cabin_class: CabinClass
    available_seats: int
    
    baggage: Baggage
    meal_included: bool = False
    wifi_available: bool = False


class PriceBreakdown(BaseModel):
    """Price details"""
    base_fare: float
    taxes: float
    fees: float
    total: float
    currency: str = "KZT"


class Flight(BaseModel):
    """Complete flight offer"""
    id: str
    
    # Flight segments (one-way or multi-leg)
    segments: List[FlightSegment]
    
    # Pricing
    price: PriceBreakdown
    
    # Cabin class
    cabin_class: CabinClass
    
    # Total duration (all segments)
    total_duration_minutes: int
    
    # Number of stops
    stops: int
    
    # Fare conditions
    refundable: bool = False
    changeable: bool = False
    change_fee: Optional[float] = None
    
    # Baggage
    baggage: Baggage
    
    # Provider info
    provider: str  # "amadeus", "sabre", "mock"
    
    # Metadata
    cached_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    valid_until: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "FL123-ALA-DXB-20251101",
                "segments": [...],
                "price": {
                    "base_fare": 45000.0,
                    "taxes": 5000.0,
                    "fees": 500.0,
                    "total": 50500.0,
                    "currency": "KZT"
                },
                "cabin_class": "economy",
                "total_duration_minutes": 240,
                "stops": 0,
                "refundable": False,
                "provider": "amadeus"
            }
        }


class SearchRequest(BaseModel):
    """Flight search request"""
    from_airport: str = Field(..., min_length=3, max_length=3)
    to_airport: str = Field(..., min_length=3, max_length=3)
    departure_date: datetime
    return_date: Optional[datetime] = None
    passengers: int = Field(default=1, ge=1, le=9)
    cabin_class: CabinClass = CabinClass.ECONOMY
    direct_only: bool = False
    
    def cache_key(self) -> str:
        """Generate cache key for this search"""
        return (
            f"{self.from_airport}:{self.to_airport}:"
            f"{self.departure_date.date()}:"
            f"{self.return_date.date() if self.return_date else 'oneway'}:"
            f"{self.passengers}:{self.cabin_class}"
        )


class SearchResponse(BaseModel):
    """Flight search response"""
    search_id: str
    flights: List[Flight]
    total: int
    from_cache: bool = False
    search_duration_ms: float
    providers_used: List[str]
