"""
Celery tasks for updating flight data
"""
import asyncio
from datetime import datetime, timedelta
import structlog

from app.tasks.celery_app import celery_app
from app.database.mongodb import connect_to_mongo, close_mongo_connection, get_database

logger = structlog.get_logger()


@celery_app.task(name="app.tasks.update_flights.update_flight_schedules")
def update_flight_schedules():
    """
    Periodic task to update flight schedules from providers
    
    This task runs every 30 minutes to keep flight data fresh.
    """
    
    logger.info("update_flight_schedules_started")
    
    try:
        # Run async update in sync context
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_update_flight_schedules_async())
        
        logger.info("update_flight_schedules_completed")
        return {"status": "success"}
    
    except Exception as e:
        logger.error("update_flight_schedules_failed", error=str(e), exc_info=True)
        return {"status": "failed", "error": str(e)}


async def _update_flight_schedules_async():
    """Async implementation of flight schedule update"""
    
    await connect_to_mongo()
    
    try:
        db = get_database()
        
        # Update logic here:
        # 1. Fetch latest schedules from providers
        # 2. Update MongoDB with new data
        # 3. Invalidate affected caches
        
        # For now, just log
        logger.info("flight_schedules_updated")
    
    finally:
        await close_mongo_connection()


@celery_app.task(name="app.tasks.update_flights.cleanup_expired_cache")
def cleanup_expired_cache():
    """
    Periodic task to cleanup expired cache entries
    
    Runs every hour to remove old cache data.
    """
    
    logger.info("cleanup_expired_cache_started")
    
    try:
        loop = asyncio.get_event_loop()
        deleted_count = loop.run_until_complete(_cleanup_expired_cache_async())
        
        logger.info("cleanup_expired_cache_completed", deleted_count=deleted_count)
        return {"status": "success", "deleted": deleted_count}
    
    except Exception as e:
        logger.error("cleanup_expired_cache_failed", error=str(e), exc_info=True)
        return {"status": "failed", "error": str(e)}


async def _cleanup_expired_cache_async() -> int:
    """Async implementation of cache cleanup"""
    
    await connect_to_mongo()
    
    try:
        db = get_database()
        
        # Delete cache entries older than TTL
        cutoff_time = datetime.utcnow() - timedelta(seconds=300)  # 5 minutes
        
        result = await db.search_cache.delete_many({
            "created_at": {"$lt": cutoff_time}
        })
        
        return result.deleted_count
    
    finally:
        await close_mongo_connection()


@celery_app.task(name="app.tasks.update_flights.refresh_popular_routes")
def refresh_popular_routes():
    """
    Task to refresh popular routes data
    
    Can be triggered manually or scheduled.
    """
    
    logger.info("refresh_popular_routes_started")
    
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_refresh_popular_routes_async())
        
        logger.info("refresh_popular_routes_completed")
        return {"status": "success"}
    
    except Exception as e:
        logger.error("refresh_popular_routes_failed", error=str(e))
        return {"status": "failed", "error": str(e)}


async def _refresh_popular_routes_async():
    """Async implementation of popular routes refresh"""
    
    await connect_to_mongo()
    
    try:
        db = get_database()
        
        # Analyze search patterns and update popular routes
        # This would involve aggregating search_cache data
        
        logger.info("popular_routes_refreshed")
    
    finally:
        await close_mongo_connection()
