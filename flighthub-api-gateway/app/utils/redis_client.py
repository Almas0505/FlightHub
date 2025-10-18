"""
Redis client utilities
"""
from redis import asyncio as aioredis
from typing import Optional
import structlog

from app.config import settings

logger = structlog.get_logger()

# Global Redis connection pool
_redis_client: Optional[aioredis.Redis] = None


async def get_redis() -> aioredis.Redis:
    """Get or create Redis client"""
    global _redis_client
    
    if _redis_client is None:
        _redis_client = await aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=10
        )
        logger.info("redis_connected", url=settings.REDIS_URL)
    
    return _redis_client


async def close_redis():
    """Close Redis connection"""
    global _redis_client
    
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
        logger.info("redis_disconnected")
