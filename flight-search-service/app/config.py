"""
Configuration settings for Flight Search Service
"""
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Flight Search Service"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # MongoDB
    MONGODB_URL: str = "mongodb://admin:secret@localhost:27017"
    MONGODB_DB_NAME: str = "flight_search"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL_SECONDS: int = 300  # 5 minutes
    
    # Celery
    CELERY_BROKER_URL: str = "amqp://admin:secret@localhost:5672"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # GDS Providers (API keys should be in .env)
    AMADEUS_API_KEY: str = ""
    AMADEUS_API_SECRET: str = ""
    AMADEUS_BASE_URL: str = "https://test.api.amadeus.com/v2"
    
    SABRE_API_KEY: str = ""
    SABRE_BASE_URL: str = "https://api.sabre.com/v1"
    
    # Mock provider (for testing)
    USE_MOCK_PROVIDER: bool = True
    
    # Search configuration
    MAX_CONCURRENT_SEARCHES: int = 3
    SEARCH_TIMEOUT_SECONDS: int = 30
    MAX_RESULTS_PER_PROVIDER: int = 50
    
    # Cache settings
    POPULAR_ROUTES_CACHE_HOURS: int = 24
    AIRPORT_DATA_CACHE_DAYS: int = 7
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
