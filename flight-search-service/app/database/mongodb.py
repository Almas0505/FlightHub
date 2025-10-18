"""
MongoDB connection and configuration
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import structlog

from app.config import settings

logger = structlog.get_logger()

# Global MongoDB client
_mongo_client: Optional[AsyncIOMotorClient] = None
_mongo_db: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo():
    """Connect to MongoDB"""
    global _mongo_client, _mongo_db
    
    try:
        _mongo_client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            maxPoolSize=10,
            minPoolSize=1,
        )
        
        # Test connection
        await _mongo_client.admin.command('ping')
        
        _mongo_db = _mongo_client[settings.MONGODB_DB_NAME]
        
        # Create indexes
        await _create_indexes()
        
        logger.info(
            "mongodb_connected",
            database=settings.MONGODB_DB_NAME
        )
        
    except Exception as e:
        logger.error("mongodb_connection_failed", error=str(e))
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    global _mongo_client
    
    if _mongo_client:
        _mongo_client.close()
        logger.info("mongodb_disconnected")


def get_database() -> AsyncIOMotorDatabase:
    """Get MongoDB database instance"""
    if _mongo_db is None:
        raise RuntimeError("MongoDB not connected")
    return _mongo_db


async def _create_indexes():
    """Create MongoDB indexes for optimization"""
    db = get_database()
    
    # Flights collection indexes
    await db.flights.create_index([
        ("departure.airport_code", 1),
        ("arrival.airport_code", 1),
        ("departure.datetime", 1)
    ])
    
    await db.flights.create_index([("flight_number", 1)])
    await db.flights.create_index([("cached_at", 1)], expireAfterSeconds=3600)
    
    # Airports collection indexes
    await db.airports.create_index([("iata_code", 1)], unique=True)
    await db.airports.create_index([("city", "text"), ("name", "text")])
    
    # Search cache indexes
    await db.search_cache.create_index([("search_key", 1)], unique=True)
    await db.search_cache.create_index([("created_at", 1)], expireAfterSeconds=300)
    
    logger.info("mongodb_indexes_created")
