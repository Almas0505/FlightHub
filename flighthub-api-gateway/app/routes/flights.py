"""
Flight search routes
"""
from fastapi import APIRouter, Query, HTTPException, status, Depends
from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field
import structlog

from app.utils.service_client import ServiceClient, ServiceType, ServiceError
from app.utils.cache import CacheService, cache_key
from app.config import settings

logger = structlog.get_logger()

router = APIRouter()


# Schemas
class Airport(BaseModel):
    code: str
    name: str
    city: str
    country: str


class FlightSearchRequest(BaseModel):
    from_airport: str = Field(..., min_length=3, max_length=3, description="IATA code (e.g., ALA)")
    to_airport: str = Field(..., min_length=3, max_length=3, description="IATA code (e.g., DXB)")
    departure_date: date
    return_date: Optional[date] = None
    passengers: int = Field(default=1, ge=1, le=9)
    cabin_class: str = Field(default="economy", pattern="^(economy|business|first)$")


class FlightSearchResponse(BaseModel):
    results: List[dict]
    total: int
    from_cache: bool = False
    search_id: str


@router.get("/search")
async def search_flights(
    from_airport: str = Query(..., min_length=3, max_length=3, description="Departure airport IATA code"),
    to_airport: str = Query(..., min_length=3, max_length=3, description="Arrival airport IATA code"),
    departure_date: date = Query(..., description="Departure date (YYYY-MM-DD)"),
    return_date: Optional[date] = Query(None, description="Return date for round trip"),
    passengers: int = Query(1, ge=1, le=9, description="Number of passengers"),
    cabin_class: str = Query("economy", pattern="^(economy|business|first)$")
):
    """
    Search for available flights
    
    - **from_airport**: 3-letter IATA code (e.g., ALA for Almaty)
    - **to_airport**: 3-letter IATA code (e.g., DXB for Dubai)
    - **departure_date**: Date in YYYY-MM-DD format
    - **return_date**: Optional return date for round trip
    - **passengers**: Number of passengers (1-9)
    - **cabin_class**: economy, business, or first
    """
    
    # Validate dates
    if return_date and return_date < departure_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Return date must be after departure date"
        )
    
    # Generate cache key
    key = cache_key(
        "flight_search",
        from_airport=from_airport.upper(),
        to_airport=to_airport.upper(),
        departure_date=str(departure_date),
        return_date=str(return_date) if return_date else "none",
        passengers=passengers,
        cabin_class=cabin_class
    )
    
    # Check cache
    cached_result = await CacheService.get(key)
    if cached_result:
        logger.info("flight_search_cache_hit", key=key)
        return {
            **cached_result,
            "from_cache": True
        }
    
    # Call Flight Search Service
    client = ServiceClient(ServiceType.FLIGHT_SEARCH)
    
    try:
        # Build params, excluding None values
        params = {
            "from_airport": from_airport.upper(),
            "to_airport": to_airport.upper(),
            "departure_date": str(departure_date),
            "passengers": passengers,
            "cabin_class": cabin_class
        }
        if return_date:
            params["return_date"] = str(return_date)
        
        result = await client.get("/search", params=params)
        
        # Cache result
        await CacheService.set(key, result, ttl=settings.REDIS_CACHE_TTL)
        
        logger.info(
            "flight_search_completed",
            from_airport=from_airport,
            to_airport=to_airport,
            results_count=len(result.get("results", []))
        )
        
        return {
            **result,
            "from_cache": False
        }
        
    except ServiceError as e:
        logger.error("flight_search_error", error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.get("/airports")
async def search_airports(
    query: str = Query(..., min_length=2, description="Search query (city name or IATA code)")
):
    """
    Search for airports by city name or IATA code
    
    - **query**: City name or 3-letter IATA code
    """
    
    client = ServiceClient(ServiceType.FLIGHT_SEARCH)
    
    try:
        result = await client.get(
            "/airports",
            params={"query": query}
        )
        
        return result
        
    except ServiceError as e:
        logger.error("airport_search_error", error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.get("/popular-routes")
async def get_popular_routes():
    """
    Get popular flight routes
    """
    
    # Check cache
    cached = await CacheService.get("popular_routes")
    if cached:
        return cached
    
    client = ServiceClient(ServiceType.FLIGHT_SEARCH)
    
    try:
        result = await client.get("/popular-routes")
        
        # Cache for longer (1 hour)
        await CacheService.set("popular_routes", result, ttl=3600)
        
        return result
        
    except ServiceError as e:
        logger.error("popular_routes_error", error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.get("/{flight_id}")
async def get_flight_details(flight_id: str):
    """
    Get detailed information about a specific flight
    
    - **flight_id**: Unique flight identifier
    """
    
    client = ServiceClient(ServiceType.FLIGHT_SEARCH)
    
    try:
        result = await client.get(f"/flights/{flight_id}")
        return result
        
    except ServiceError as e:
        if e.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flight not found"
            )
        
        logger.error("flight_details_error", flight_id=flight_id, error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
