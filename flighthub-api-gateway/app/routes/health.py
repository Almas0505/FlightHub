"""
Health check endpoints
"""
from fastapi import APIRouter, status
from datetime import datetime
import structlog

from app.config import settings
from app.utils.redis_client import get_redis

logger = structlog.get_logger()

router = APIRouter()


@router.get("/live")
async def liveness_probe():
    """
    Liveness probe - checks if service is alive
    Used by Kubernetes to restart unhealthy pods
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "api-gateway",
        "version": "1.0.0"
    }


@router.get("/ready")
async def readiness_probe():
    """
    Readiness probe - checks if service is ready to serve traffic
    Used by Kubernetes to route traffic
    """
    checks = {
        "redis": False,
    }
    
    # Check Redis
    try:
        redis = await get_redis()
        await redis.ping()
        checks["redis"] = True
    except Exception as e:
        logger.error("redis_health_check_failed", error=str(e))
    
    # Determine overall status
    all_healthy = all(checks.values())
    status_code = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return {
        "status": "ready" if all_healthy else "not_ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks
    }, status_code


@router.get("")
async def health_check():
    """
    General health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "FlightHub API Gateway",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }
