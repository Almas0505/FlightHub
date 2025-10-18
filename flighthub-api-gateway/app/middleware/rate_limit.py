"""
Rate limiting middleware using Redis
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import structlog
import time

from app.config import settings
from app.utils.redis_client import get_redis

logger = structlog.get_logger()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting"""
        
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)
        
        # Get client identifier
        client_id = self._get_client_id(request)
        
        # Check rate limit
        redis = await get_redis()
        is_allowed, remaining, reset_time = await self._check_rate_limit(
            redis, client_id
        )
        
        if not is_allowed:
            logger.warning(
                "rate_limit_exceeded",
                client_id=client_id,
                path=request.url.path
            )
            
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Try again in {reset_time} seconds."
                },
                headers={
                    "X-RateLimit-Limit": str(settings.RATE_LIMIT_REQUESTS),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_time),
                    "Retry-After": str(reset_time)
                }
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_REQUESTS)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset_time)
        
        return response
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier (IP or user_id)"""
        # Use user_id if authenticated
        if hasattr(request.state, "user_id") and request.state.user_id:
            return f"user:{request.state.user_id}"
        
        # Otherwise use IP address
        client_ip = request.client.host
        forwarded_for = request.headers.get("X-Forwarded-For")
        
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        
        return f"ip:{client_ip}"
    
    async def _check_rate_limit(self, redis, client_id: str) -> tuple[bool, int, int]:
        """
        Check rate limit using sliding window algorithm
        Returns: (is_allowed, remaining_requests, reset_time)
        """
        key = f"rate_limit:{client_id}"
        now = int(time.time())
        window_start = now - settings.RATE_LIMIT_WINDOW
        
        # Use Redis pipeline for atomic operations
        pipe = redis.pipeline()
        
        # Remove old entries outside the window
        pipe.zremrangebyscore(key, 0, window_start)
        
        # Count current requests in window
        pipe.zcard(key)
        
        # Add current request
        pipe.zadd(key, {str(now): now})
        
        # Set expiry
        pipe.expire(key, settings.RATE_LIMIT_WINDOW)
        
        results = await pipe.execute()
        current_count = results[1]
        
        # Check if limit exceeded
        is_allowed = current_count < settings.RATE_LIMIT_REQUESTS
        remaining = max(0, settings.RATE_LIMIT_REQUESTS - current_count - 1)
        reset_time = settings.RATE_LIMIT_WINDOW
        
        return is_allowed, remaining, reset_time
