"""
Flight Search Service - Main Application
Асинхронный поиск авиарейсов с агрегацией данных от разных провайдеров
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog
from contextlib import asynccontextmanager

from app.config import settings
from app.database.mongodb import connect_to_mongo, close_mongo_connection
from app.routes import flights, airports, health
from app.tasks.celery_app import celery_app

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("flight_search_service_starting", environment=settings.ENVIRONMENT)
    await connect_to_mongo()
    logger.info("mongodb_connected")
    
    yield
    
    # Shutdown
    logger.info("flight_search_service_shutting_down")
    await close_mongo_connection()


# FastAPI application
app = FastAPI(
    title="Flight Search Service",
    description="Асинхронный поиск и агрегация авиарейсов",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all exceptions"""
    logger.error(
        "unhandled_exception",
        error=str(exc),
        path=request.url.path,
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        }
    )


# Include routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(airports.router, prefix="/airports", tags=["Airports"])
app.include_router(flights.router, prefix="", tags=["Flights"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Flight Search Service",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Multi-provider flight search",
            "Real-time availability",
            "Price comparison",
            "MongoDB caching",
            "Async processing"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.DEBUG
    )
