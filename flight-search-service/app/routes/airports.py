"""
Airport search API routes
"""
from fastapi import APIRouter, Query, HTTPException, status
import structlog

from app.models.airport import AirportSearchResponse
from app.repositories.airport_repository import AirportRepository

logger = structlog.get_logger()
router = APIRouter()


@router.get("", response_model=AirportSearchResponse)
async def search_airports(
    query: str = Query(..., min_length=2, description="Search query (city name or IATA code)")
):
    """
    Search for airports by city name or IATA code
    
    **Examples:**
    - Search by IATA code: `?query=ALA`
    - Search by city: `?query=Almaty`
    - Search by country: `?query=Kazakhstan`
    
    Returns up to 20 matching airports.
    """
    
    try:
        airports = await AirportRepository.search(query)
        
        logger.info("airport_search", query=query, results_count=len(airports))
        
        return AirportSearchResponse(
            airports=airports,
            total=len(airports)
        )
    
    except Exception as e:
        logger.error("airport_search_error", query=query, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search airports"
        )


@router.get("/{iata_code}")
async def get_airport(iata_code: str):
    """
    Get airport details by IATA code
    
    - **iata_code**: 3-letter IATA code (e.g., ALA, DXB)
    """
    
    if len(iata_code) != 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IATA code must be 3 characters"
        )
    
    try:
        airport = await AirportRepository.get_by_iata(iata_code)
        
        if not airport:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Airport with code {iata_code} not found"
            )
        
        return airport
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_airport_error", iata_code=iata_code, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve airport details"
        )


@router.get("/popular/list")
async def get_popular_airports():
    """
    Get list of popular airports
    
    Returns frequently used airports for quick selection.
    """
    
    try:
        airports = await AirportRepository.get_popular()
        
        return AirportSearchResponse(
            airports=airports,
            total=len(airports)
        )
    
    except Exception as e:
        logger.error("get_popular_airports_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve popular airports"
        )


@router.post("/seed")
async def seed_airport_data():
    """
    Seed database with sample airport data
    
    **Note:** This is for development/testing only.
    Should be removed or secured in production.
    """
    
    try:
        await AirportRepository.seed_sample_data()
        
        return {
            "message": "Sample airport data seeded successfully"
        }
    
    except Exception as e:
        logger.error("seed_data_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to seed airport data"
        )
