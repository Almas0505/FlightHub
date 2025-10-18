"""
Cache utilities for Redis
"""
import json
from typing import Optional, Any
import structlog
from functools import wraps

from app.utils.redis_client import get_redis
from app.config import settings

logger = structlog.get_logger()


class CacheService:
    """Redis cache service"""
    
    @staticmethod
    async def get(key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            redis = await get_redis()
            value = await redis.get(key)
            
            if value:
                return json.loads(value)
            return None
            
        except Exception as e:
            logger.error("cache_get_error", key=key, error=str(e))
            return None
    
    @staticmethod
    async def set(key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache"""
        try:
            redis = await get_redis()
            ttl = ttl or settings.REDIS_CACHE_TTL
            
            serialized = json.dumps(value)
            await redis.setex(key, ttl, serialized)
            
            logger.debug("cache_set", key=key, ttl=ttl)
            return True
            
        except Exception as e:
            logger.error("cache_set_error", key=key, error=str(e))
            return False
    
    @staticmethod
    async def delete(key: str) -> bool:
        """Delete key from cache"""
        try:
            redis = await get_redis()
            await redis.delete(key)
            logger.debug("cache_deleted", key=key)
            return True
            
        except Exception as e:
            logger.error("cache_delete_error", key=key, error=str(e))
            return False
    
    @staticmethod
    async def invalidate_pattern(pattern: str) -> int:
        """Delete all keys matching pattern"""
        try:
            redis = await get_redis()
            keys = await redis.keys(pattern)
            
            if keys:
                count = await redis.delete(*keys)
                logger.info("cache_invalidated", pattern=pattern, count=count)
                return count
            
            return 0
            
        except Exception as e:
            logger.error("cache_invalidate_error", pattern=pattern, error=str(e))
            return 0


def cache_key(*args, **kwargs) -> str:
    """Generate cache key from arguments"""
    parts = [str(arg) for arg in args]
    parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    return ":".join(parts)


def cached(prefix: str, ttl: int = None):
    """
    Decorator for caching function results
    
    Usage:
        @cached("flight_search", ttl=300)
        async def search_flights(from_city, to_city):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{prefix}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_result = await CacheService.get(key)
            if cached_result is not None:
                logger.debug("cache_hit", key=key)
                return cached_result
            
            # Execute function
            logger.debug("cache_miss", key=key)
            result = await func(*args, **kwargs)
            
            # Store in cache
            await CacheService.set(key, result, ttl)
            
            return result
        
        return wrapper
    return decorator
