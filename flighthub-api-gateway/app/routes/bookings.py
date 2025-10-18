"""
Booking management routes
"""
from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date
import structlog

from app.utils.service_client import ServiceClient, ServiceType, ServiceError
from app.utils.cache import CacheService
from app.utils.security import get_current_user

logger = structlog.get_logger()

router = APIRouter()


# Schemas
class PassengerCreate(BaseModel):
    title: str = Field(..., pattern="^(MR|MS|MRS)$")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    passport_number: str = Field(..., min_length=5, max_length=20)
    nationality: str = Field(..., min_length=2, max_length=3, description="ISO country code")


class BookingCreate(BaseModel):
    flight_id: str
    passengers: List[PassengerCreate] = Field(..., min_length=1, max_length=9)
    contact_email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    contact_phone: str = Field(..., min_length=10, max_length=20)


class BookingResponse(BaseModel):
    id: str
    pnr: str
    status: str
    flight_details: dict
    passengers: List[dict]
    total_amount: float
    currency: str
    expires_at: Optional[str] = None
    created_at: str


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new flight booking
    
    This endpoint:
    1. Creates a booking with PENDING status
    2. Holds the seats for 15 minutes
    3. Sends confirmation email
    4. Returns booking details with PNR
    
    **Note**: Booking must be paid within 15 minutes or it will expire
    """
    
    client = ServiceClient(ServiceType.BOOKING)
    
    try:
        # Add user_id to booking data and serialize dates
        request_data = booking_data.dict()
        request_data["user_id"] = current_user.get("user_id")
        
        # Convert date objects to strings for JSON serialization
        for passenger in request_data.get("passengers", []):
            if "date_of_birth" in passenger and passenger["date_of_birth"]:
                passenger["date_of_birth"] = str(passenger["date_of_birth"])
        
        # Forward Authorization header to Booking Service
        headers = {}
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        
        result = await client.post("/bookings/", json=request_data, headers=headers)
        
        logger.info(
            "booking_created",
            booking_id=result.get("id"),
            user_id=current_user.get("user_id"),
            pnr=result.get("pnr")
        )
        
        return result
        
    except ServiceError as e:
        logger.error("booking_creation_error", error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.get("")
async def get_user_bookings(
    request: Request,
    status_filter: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """
    Get all bookings for the current user
    
    - **status**: Filter by booking status (PENDING, CONFIRMED, CANCELLED, etc.)
    - **limit**: Number of results per page (default: 20)
    - **offset**: Pagination offset (default: 0)
    """
    
    client = ServiceClient(ServiceType.BOOKING)
    
    try:
        params = {
            "user_id": current_user.get("user_id"),
            "limit": limit,
            "offset": offset
        }
        
        if status_filter:
            params["status"] = status_filter
        
        # Forward Authorization header to Booking Service
        headers = {}
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        
        result = await client.get("/bookings/", params=params, headers=headers)
        return result
        
    except ServiceError as e:
        logger.error("get_bookings_error", error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.get("/{booking_id}")
async def get_booking_details(
    booking_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Get details of a specific booking
    
    - **booking_id**: Unique booking identifier or PNR
    """
    
    client = ServiceClient(ServiceType.BOOKING)
    
    try:
        # Forward Authorization header to Booking Service
        headers = {}
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        
        result = await client.get(f"/bookings/{booking_id}", headers=headers)
        
        # Verify user owns this booking
        if result.get("user_id") != current_user.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this booking"
            )
        
        return result
        
    except ServiceError as e:
        if e.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        
        logger.error("get_booking_error", booking_id=booking_id, error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.post("/{booking_id}/cancel")
async def cancel_booking(
    booking_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Cancel a booking
    
    - **booking_id**: Unique booking identifier
    
    **Note**: Cancellation policy and refund depend on fare rules
    """
    
    client = ServiceClient(ServiceType.BOOKING)
    
    try:
        # Forward Authorization header to Booking Service
        headers = {}
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        
        # Get booking to verify ownership
        booking = await client.get(f"/bookings/{booking_id}", headers=headers)
        
        if booking.get("user_id") != current_user.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to cancel this booking"
            )
        
        # Cancel booking
        result = await client.post(f"/bookings/{booking_id}/cancel", json={}, headers=headers)
        
        logger.info(
            "booking_cancelled",
            booking_id=booking_id,
            user_id=current_user.get("user_id")
        )
        
        return result
        
    except ServiceError as e:
        logger.error("cancel_booking_error", booking_id=booking_id, error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.get("/{booking_id}/ticket")
async def get_ticket(
    booking_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Get ticket PDF for a confirmed booking
    
    - **booking_id**: Unique booking identifier
    """
    
    client = ServiceClient(ServiceType.BOOKING)
    
    try:
        # Forward Authorization header to Booking Service
        headers = {}
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        
        # Verify ownership
        booking = await client.get(f"/bookings/{booking_id}", headers=headers)
        
        if booking.get("user_id") != current_user.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this ticket"
            )
        
        # Get ticket
        result = await client.get(f"/bookings/{booking_id}/ticket", headers=headers)
        return result
        
    except ServiceError as e:
        if e.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found or booking not confirmed yet"
            )
        
        logger.error("get_ticket_error", booking_id=booking_id, error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
