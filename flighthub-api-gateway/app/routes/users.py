"""
User management routes
"""
from fastapi import APIRouter, HTTPException, status, Depends, Request, Body
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import structlog

from app.utils.service_client import ServiceClient, ServiceType, ServiceError
from app.utils.cache import CacheService
from app.utils.security import get_current_user

logger = structlog.get_logger()

router = APIRouter()


# Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone: Optional[str] = None
    username: Optional[str] = None
    date_of_birth: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserProfile(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    created_at: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister):
    """
    Register a new user account
    
    - **email**: Valid email address
    - **password**: Minimum 8 characters
    - **first_name**: First name
    - **last_name**: Last name
    - **phone**: Optional phone number
    """
    
    client = ServiceClient(ServiceType.USER)
    
    try:
        # Prepare data for user service
        user_dict = user_data.dict()
        
        # Add username if not provided (use email prefix)
        if not user_dict.get('username'):
            user_dict['username'] = user_data.email.split('@')[0]
        
        # Add password_confirm for Django validation
        user_dict['password_confirm'] = user_dict['password']
        
        result = await client.post("/users/register/", json=user_dict)
        
        logger.info(
            "user_registered",
            user_id=result.get("id"),
            email=user_data.email
        )
        
        return result
        
    except ServiceError as e:
        if e.status_code == 400 and "already exists" in e.message.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        logger.error("user_registration_error", error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.post("/login")
async def login_user(credentials: UserLogin):
    """
    Login with email and password
    
    Returns JWT access token and refresh token
    """
    
    client = ServiceClient(ServiceType.USER)
    
    try:
        # Authenticate with user service - it returns tokens
        result = await client.post("/users/login/", json=credentials.dict())
        
        logger.info("user_logged_in", user_id=result.get("user", {}).get("id"))
        
        # Return tokens from user service directly
        return result
        
    except ServiceError as e:
        if e.status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        logger.error("user_login_error", error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.post("/refresh")
async def refresh_access_token(refresh_token: str = Body(..., embed=True)):
    """
    Refresh access token using refresh token
    Forwards request to User Service
    """
    
    client = ServiceClient(ServiceType.USER)
    
    try:
        result = await client.post("/users/refresh/", json={"refresh_token": refresh_token})
        return result
        
    except ServiceError as e:
        logger.error("token_refresh_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed"
        )


@router.get("/me")
async def get_current_user_profile(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Get current user profile
    """
    
    client = ServiceClient(ServiceType.USER)
    
    try:
        # Forward Authorization header to User Service
        headers = {}
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        
        # Use /users/profile/ endpoint instead of /users/{id}/
        result = await client.get("/users/profile/", headers=headers)
        return result
        
    except ServiceError as e:
        logger.error("get_profile_error", error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.put("/me")
async def update_profile(
    request: Request,
    profile_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Update current user profile
    """
    
    client = ServiceClient(ServiceType.USER)
    
    try:
        # Forward Authorization header to User Service
        headers = {}
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        
        # Use /users/update_profile/ endpoint
        result = await client.put("/users/update_profile/", json=profile_data, headers=headers)
        
        logger.info("profile_updated", user_id=current_user.get("user_id"))
        return result
        
    except ServiceError as e:
        logger.error("update_profile_error", error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )


@router.post("/change-password")
async def change_password(
    request: Request,
    old_password: str = Body(...),
    new_password: str = Body(..., min_length=8),
    current_user: dict = Depends(get_current_user)
):
    """
    Change user password
    """
    
    client = ServiceClient(ServiceType.USER)
    
    try:
        user_id = current_user.get("user_id")
        
        # Forward Authorization header to User Service
        headers = {}
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        
        result = await client.post(
            f"/users/{user_id}/change-password",
            json={
                "old_password": old_password,
                "new_password": new_password
            },
            headers=headers
        )
        
        logger.info("password_changed", user_id=user_id)
        return {"message": "Password changed successfully"}
        
    except ServiceError as e:
        if e.status_code == 400:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid old password"
            )
        
        logger.error("change_password_error", error=str(e))
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
