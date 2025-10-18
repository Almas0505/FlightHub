"""
Request/Response logging middleware
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import structlog
import time
import uuid

logger = structlog.get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    """Request/Response logging middleware"""
    
    async def dispatch(self, request: Request, call_next):
        """Process request with logging"""
        
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Log request
        start_time = time.time()
        
        logger.info(
            "request_started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host,
            user_agent=request.headers.get("user-agent", "unknown")
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            logger.info(
                "request_completed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=round(duration * 1000, 2)
            )
            
            # Add custom headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{round(duration * 1000, 2)}ms"
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            
            logger.error(
                "request_failed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                error=str(e),
                duration_ms=round(duration * 1000, 2)
            )
            raise
