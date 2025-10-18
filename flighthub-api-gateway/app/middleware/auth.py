"""
Authentication middleware for JWT token validation
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional
import jwt
import structlog

from app.config import settings

logger = structlog.get_logger()

# Public paths that don't require authentication
PUBLIC_PATHS = [
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
    "/health/live",
    "/health/ready",
    "/api/v1/users/register",
    "/api/v1/users/login",
    "/api/v1/flights/search",
]


class AuthMiddleware(BaseHTTPMiddleware):
    """JWT Authentication Middleware"""
    
    async def dispatch(self, request: Request, call_next):
        """Process request"""
        
        # Skip authentication for public paths
        if self._is_public_path(request.url.path):
            return await call_next(request)
        
        # Extract token
        token = self._extract_token(request)
        
        logger.info(
            "auth_middleware_processing",
            path=request.url.path,
            has_token=bool(token),
            auth_header=request.headers.get("Authorization", "")[:50]
        )
        
        if not token:
            logger.warning("auth_no_token", path=request.url.path)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Authentication required", "message": "Missing authorization token"}
            )
        
        # Verify token
        try:
            payload = self._verify_token(token)
            request.state.user = payload
            request.state.user_id = payload.get("user_id")
            
            logger.info(
                "request_authenticated",
                user_id=payload.get("user_id"),
                path=request.url.path
            )
            
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Token expired", "message": "Your session has expired. Please login again."}
            )
        except jwt.InvalidTokenError as e:
            logger.warning("invalid_token", error=str(e))
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid token", "message": "Authentication token is invalid"}
            )
        
        response = await call_next(request)
        return response
    
    def _is_public_path(self, path: str) -> bool:
        """Check if path is public"""
        for public_path in PUBLIC_PATHS:
            if path.startswith(public_path):
                return True
        return False
    
    def _extract_token(self, request: Request) -> Optional[str]:
        """Extract JWT token from Authorization header"""
        authorization: str = request.headers.get("Authorization")
        
        if not authorization:
            return None
        
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                return None
            return token
        except ValueError:
            return None
    
    def _verify_token(self, token: str) -> dict:
        """Verify JWT token"""
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload


def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    from datetime import datetime, timedelta
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    from datetime import datetime, timedelta
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def get_current_user(request: Request) -> dict:
    """Dependency to get current authenticated user"""
    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return request.state.user
