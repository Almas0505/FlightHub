"""
FlightHub API Gateway - Main Application
Единая точка входа для всех микросервисов
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import structlog
import time

from app.config import settings
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.logging import LoggingMiddleware
from app.routes import flights, bookings, users, payments, health

# Structured logging
logger = structlog.get_logger()

# FastAPI приложение
app = FastAPI(
    title="FlightHub API Gateway",
    description="Unified API Gateway for FlightHub microservices",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)


# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.error("validation_error", errors=exc.errors(), body=exc.body)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "details": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error("unhandled_exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    logger.info(
        "api_gateway_starting",
        environment=settings.ENVIRONMENT,
        version="1.0.0"
    )


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown"""
    logger.info("api_gateway_shutting_down")


# Include routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(flights.router, prefix="/api/v1/flights", tags=["Flights"])
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["Bookings"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "FlightHub API Gateway",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
