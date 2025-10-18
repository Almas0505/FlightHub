"""
Configuration settings for API Gateway
"""
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "FlightHub API Gateway"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production-please-use-strong-random-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_TTL: int = 300  # 5 minutes
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Microservices URLs
    FLIGHT_SEARCH_URL: str = "http://localhost:8001"
    BOOKING_SERVICE_URL: str = "http://localhost:8002"
    PAYMENT_SERVICE_URL: str = "http://localhost:8003"
    NOTIFICATION_SERVICE_URL: str = "http://localhost:8004"
    USER_SERVICE_URL: str = "http://localhost:8005"
    
    # Timeouts
    SERVICE_TIMEOUT: int = 30
    
    # Circuit Breaker
    CIRCUIT_BREAKER_ENABLED: bool = True
    CIRCUIT_BREAKER_THRESHOLD: int = 5
    CIRCUIT_BREAKER_TIMEOUT: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
