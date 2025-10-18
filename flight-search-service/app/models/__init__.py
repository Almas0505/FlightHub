"""
Models package
"""
from app.models.flight import (
    Flight,
    FlightSegment,
    SearchRequest,
    SearchResponse,
    CabinClass,
    Airport,
    Airline,
)
from app.models.airport import AirportModel, AirportSearchResponse

__all__ = [
    "Flight",
    "FlightSegment",
    "SearchRequest",
    "SearchResponse",
    "CabinClass",
    "Airport",
    "Airline",
    "AirportModel",
    "AirportSearchResponse",
]
