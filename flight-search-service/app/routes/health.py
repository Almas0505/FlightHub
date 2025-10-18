"""
Health check endpoints
"""
from fastapi import APIRouter, status
from datetime import datetime
import structlog

from app.config import settings
from app.database.mongodb import get_database

logger = structlog.get_logger()
router = APIRouter()


@router.get("/live")
async def liveness_probe():
    """
    Liveness probe for Kubernetes
    
    Returns 200 if service is alive and running.
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "flight-search-service",
        "version": "1.0.0"
    }


@router.get("/ready")
async def readiness_probe():
    """
    Readiness probe for Kubernetes
    
    Checks if service is ready to accept traffic by verifying:
    - MongoDB connection
    - Providers availability
    """
    checks = {
        "mongodb": False,
        "providers": False,
    }
    
    # Check MongoDB
    try:
        db = get_database()
        await db.command("ping")
        checks["mongodb"] = True
    except Exception as e:
        logger.error("mongodb_health_check_failed", error=str(e))
    
    # Check providers (at least one should be available)
    try:
        from app.services.search_engine import FlightSearchEngine
        engine = FlightSearchEngine()
        checks["providers"] = len(engine.providers) > 0
    except Exception as e:
        logger.error("providers_health_check_failed", error=str(e))
    
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
        "service": "Flight Search Service",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "features": {
            "mock_provider": settings.USE_MOCK_PROVIDER,
            "amadeus_configured": bool(settings.AMADEUS_API_KEY),
        }
    }
