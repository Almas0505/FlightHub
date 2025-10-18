"""
Payment processing routes
"""
from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel, Field
from typing import Optional
import structlog

from app.utils.service_client import ServiceClient, ServiceType, ServiceError
from app.utils.cache import CacheService
from app.utils.security import get_current_user

logger = structlog.get_logger()

router = APIRouter()


# Schemas
class PaymentCreate(BaseModel):
    booking_id: str
    payment_method: str = Field(..., pattern="^(card|bank_transfer|wallet)$")
    card_token: Optional[str] = None  # Tokenized card data
    save_card: bool = False


class PaymentResponse(BaseModel):
    id: str
    booking_id: str
    amount: float
    currency: str
    status: str
    payment_method: str
    created_at: str


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_payment(
    request: Request,
    payment_data: PaymentCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Process payment for a booking
    
    - **booking_id**: Booking to pay for
    - **payment_method**: card, bank_transfer, or wallet
    - **card_token**: Tokenized card data (for card payments)
    - **save_card**: Save card for future use
    
    **Payment flow:**
    1. Validates booking exists and is in PENDING status
    2. Processes payment with payment provider
    3. Updates booking to CONFIRMED on success
    4. Sends confirmation email with ticket
    """
    
    # Forward Authorization header
    headers = {}
    if "authorization" in request.headers:
        headers["Authorization"] = request.headers["authorization"]
    
    # Verify booking ownership
    booking_client = ServiceClient(ServiceType.BOOKING)
    
    try:
        booking = await booking_client.get(f"/bookings/{payment_data.booking_id}", headers=headers)
        
        if booking.get("user_id") != current_user.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to pay for this booking"
            )
        
        if booking.get("status") != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Booking is not in PENDING status (current: {booking.get('status')})"
            )
        
    except ServiceError as e:
        if e.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    # Process payment
    payment_client = ServiceClient(ServiceType.PAYMENT)
    
    try:
        request_data = {
            **payment_data.dict(),
            "user_id": current_user.get("user_id"),
            "amount": booking.get("total_amount"),
            "currency": booking.get("currency", "KZT")
        }
        
        result = await payment_client.post("/payments", json=request_data, headers=headers)
        
        logger.info(
            "payment_processed",
            payment_id=result.get("id"),
            booking_id=payment_data.booking_id,
            user_id=current_user.get("user_id"),
            amount=booking.get("total_amount")
        )
        
        return result
        
    except ServiceError as e:
        logger.error("payment_processing_error", error=str(e), booking_id=payment_data.booking_id)
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.get("/{payment_id}")
async def get_payment_details(
    payment_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Get details of a specific payment
    """
    
    client = ServiceClient(ServiceType.PAYMENT)
    
    try:
        # Forward Authorization header
        headers = {}
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        
        result = await client.get(f"/payments/{payment_id}", headers=headers)
        
        # Verify user owns this payment
        if result.get("user_id") != current_user.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this payment"
            )
        
        return result
        
    except ServiceError as e:
        if e.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        
        logger.error("get_payment_error", payment_id=payment_id, error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.get("")
async def get_user_payments(
    request: Request,
    booking_id: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """
    Get all payments for the current user
    
    - **booking_id**: Filter by booking ID
    - **limit**: Results per page
    - **offset**: Pagination offset
    """
    
    client = ServiceClient(ServiceType.PAYMENT)
    
    try:
        params = {
            "user_id": current_user.get("user_id"),
            "limit": limit,
            "offset": offset
        }
        
        if booking_id:
            params["booking_id"] = booking_id
        
        # Forward Authorization header
        headers = {}
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        
        result = await client.get("/payments", params=params, headers=headers)
        return result
        
    except ServiceError as e:
        logger.error("get_payments_error", error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.post("/{payment_id}/refund")
async def request_refund(
    payment_id: str,
    request: Request,
    reason: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Request refund for a payment
    
    - **payment_id**: Payment to refund
    - **reason**: Reason for refund request
    """
    
    client = ServiceClient(ServiceType.PAYMENT)
    
    try:
        # Forward Authorization header
        headers = {}
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        
        # Verify ownership
        payment = await client.get(f"/payments/{payment_id}", headers=headers)
        
        if payment.get("user_id") != current_user.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to refund this payment"
            )
        
        # Request refund
        result = await client.post(
            f"/payments/{payment_id}/refund",
            json={"reason": reason},
            headers=headers
        )
        
        logger.info(
            "refund_requested",
            payment_id=payment_id,
            user_id=current_user.get("user_id")
        )
        
        return result
        
    except ServiceError as e:
        logger.error("refund_request_error", payment_id=payment_id, error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
