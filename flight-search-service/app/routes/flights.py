"""
Flight search API routes
"""
from fastapi import APIRouter, Query, HTTPException, status
from datetime import date, datetime
from typing import Optional
import structlog

from app.models.flight import SearchRequest, SearchResponse, CabinClass
from app.services.search_engine import FlightSearchEngine

logger = structlog.get_logger()
router = APIRouter()

# Initialize search engine
search_engine = FlightSearchEngine()


@router.get("/search", response_model=SearchResponse)
async def search_flights(
    from_airport: str = Query(..., min_length=3, max_length=3, description="Departure airport IATA code"),
    to_airport: str = Query(..., min_length=3, max_length=3, description="Arrival airport IATA code"),
    departure_date: date = Query(..., description="Departure date (YYYY-MM-DD)"),
    return_date: Optional[date] = Query(None, description="Return date for round trip"),
    passengers: int = Query(1, ge=1, le=9, description="Number of passengers"),
    cabin_class: CabinClass = Query(CabinClass.ECONOMY, description="Cabin class"),
    direct_only: bool = Query(False, description="Show only direct flights"),
):
    """
    Search for available flights
    
    This endpoint aggregates flight data from multiple providers (GDS systems):
    - Amadeus
    - Sabre  
    - Mock provider (for testing)
    
    Results are cached for 5 minutes to improve performance.
    
    **Example:**
    ```
    GET /search?from_airport=ALA&to_airport=DXB&departure_date=2025-11-01&passengers=1
    ```
    """
    
    # Validate airports are different
    if from_airport.upper() == to_airport.upper():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Departure and arrival airports must be different"
        )
    
    # Validate dates
    today = date.today()
    if departure_date < today:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Departure date cannot be in the past"
        )
    
    if return_date and return_date < departure_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Return date must be after departure date"
        )
    
    # Create search request
    search_request = SearchRequest(
        from_airport=from_airport.upper(),
        to_airport=to_airport.upper(),
        departure_date=datetime.combine(departure_date, datetime.min.time()),
        return_date=datetime.combine(return_date, datetime.min.time()) if return_date else None,
        passengers=passengers,
        cabin_class=cabin_class,
        direct_only=direct_only
    )
    
    try:
        # Execute search
        result = await search_engine.search(search_request)
        
        logger.info(
            "search_request_completed",
            from_airport=from_airport,
            to_airport=to_airport,
            flights_found=result.total
        )
        
        return result
    
    except Exception as e:
        logger.error("search_request_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search flights. Please try again."
        )


@router.get("/flights/{flight_id}")
async def get_flight_details(flight_id: str):
    """
    Get detailed information about a specific flight
    
    - **flight_id**: Unique flight identifier from search results
    """
    
    try:
        flight = await search_engine.get_flight_by_id(flight_id)
        
        if not flight:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flight not found or expired"
            )
        
        return flight
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_flight_error", flight_id=flight_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve flight details"
        )


@router.get("/popular-routes")
async def get_popular_routes():
    """
    Get popular flight routes
    
    Returns a list of frequently searched routes with their popularity score.
    """
    
    # Sample popular routes from Kazakhstan
    popular_routes = [
        {
            "from": {"code": "ALA", "city": "Almaty", "country": "Kazakhstan"},
            "to": {"code": "DXB", "city": "Dubai", "country": "UAE"},
            "popularity": 95
        },
        {
            "from": {"code": "ALA", "city": "Almaty", "country": "Kazakhstan"},
            "to": {"code": "IST", "city": "Istanbul", "country": "Turkey"},
            "popularity": 92
        },
        {
            "from": {"code": "ALA", "city": "Almaty", "country": "Kazakhstan"},
            "to": {"code": "TSE", "city": "Astana", "country": "Kazakhstan"},
            "popularity": 88
        },
        {
            "from": {"code": "TSE", "city": "Astana", "country": "Kazakhstan"},
            "to": {"code": "DXB", "city": "Dubai", "country": "UAE"},
            "popularity": 85
        },
        {
            "from": {"code": "ALA", "city": "Almaty", "country": "Kazakhstan"},
            "to": {"code": "SVO", "city": "Moscow", "country": "Russia"},
            "popularity": 82
        },
    ]
    
    return {
        "routes": popular_routes,
        "total": len(popular_routes)
    }
