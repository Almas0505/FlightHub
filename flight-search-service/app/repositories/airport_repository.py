"""
Airport repository for MongoDB operations
"""
from typing import List, Optional
import structlog

from app.database.mongodb import get_database
from app.models.airport import AirportModel

logger = structlog.get_logger()


class AirportRepository:
    """Repository for airport data"""
    
    @staticmethod
    async def search(query: str) -> List[AirportModel]:
        """
        Search airports by IATA code, city, or name
        
        Args:
            query: Search query (can be IATA code, city, or airport name)
            
        Returns:
            List of matching airports
        """
        
        try:
            db = get_database()
            
            # If query is 3 chars, search by IATA code
            if len(query) == 3:
                airports = await db.airports.find({
                    "iata_code": query.upper()
                }).to_list(length=10)
            else:
                # Text search in city and name
                airports = await db.airports.find({
                    "$or": [
                        {"city": {"$regex": query, "$options": "i"}},
                        {"name": {"$regex": query, "$options": "i"}},
                        {"country": {"$regex": query, "$options": "i"}}
                    ]
                }).limit(20).to_list(length=20)
            
            return [AirportModel(**airport) for airport in airports]
        
        except Exception as e:
            logger.error("airport_search_error", query=query, error=str(e))
            return []
    
    @staticmethod
    async def get_by_iata(iata_code: str) -> Optional[AirportModel]:
        """Get airport by IATA code"""
        
        try:
            db = get_database()
            airport = await db.airports.find_one({"iata_code": iata_code.upper()})
            
            if airport:
                return AirportModel(**airport)
            
            return None
        
        except Exception as e:
            logger.error("airport_get_error", iata_code=iata_code, error=str(e))
            return None
    
    @staticmethod
    async def get_popular() -> List[AirportModel]:
        """Get popular airports"""
        
        try:
            db = get_database()
            
            # Return most popular airports (hardcoded for now)
            popular_codes = ["ALA", "DXB", "IST", "DOH", "SVO", "TSE", "LON", "NYC"]
            
            airports = await db.airports.find({
                "iata_code": {"$in": popular_codes}
            }).to_list(length=50)
            
            return [AirportModel(**airport) for airport in airports]
        
        except Exception as e:
            logger.error("get_popular_airports_error", error=str(e))
            return []
    
    @staticmethod
    async def seed_sample_data():
        """Seed database with sample airport data"""
        
        try:
            db = get_database()
            
            sample_airports = [
                {
                    "iata_code": "ALA",
                    "icao_code": "UAAA",
                    "name": "Almaty International Airport",
                    "city": "Almaty",
                    "country": "Kazakhstan",
                    "country_code": "KZ",
                    "latitude": 43.3521,
                    "longitude": 77.0405,
                    "timezone": "Asia/Almaty"
                },
                {
                    "iata_code": "DXB",
                    "icao_code": "OMDB",
                    "name": "Dubai International Airport",
                    "city": "Dubai",
                    "country": "United Arab Emirates",
                    "country_code": "AE",
                    "latitude": 25.2532,
                    "longitude": 55.3657,
                    "timezone": "Asia/Dubai"
                },
                {
                    "iata_code": "IST",
                    "icao_code": "LTFM",
                    "name": "Istanbul Airport",
                    "city": "Istanbul",
                    "country": "Turkey",
                    "country_code": "TR",
                    "latitude": 41.2619,
                    "longitude": 28.7419,
                    "timezone": "Europe/Istanbul"
                },
                {
                    "iata_code": "DOH",
                    "icao_code": "OTHH",
                    "name": "Hamad International Airport",
                    "city": "Doha",
                    "country": "Qatar",
                    "country_code": "QA",
                    "latitude": 25.2731,
                    "longitude": 51.6086,
                    "timezone": "Asia/Qatar"
                },
                {
                    "iata_code": "SVO",
                    "icao_code": "UUEE",
                    "name": "Sheremetyevo International Airport",
                    "city": "Moscow",
                    "country": "Russia",
                    "country_code": "RU",
                    "latitude": 55.9726,
                    "longitude": 37.4146,
                    "timezone": "Europe/Moscow"
                },
                {
                    "iata_code": "TSE",
                    "icao_code": "UACC",
                    "name": "Nursultan Nazarbayev International Airport",
                    "city": "Astana",
                    "country": "Kazakhstan",
                    "country_code": "KZ",
                    "latitude": 51.0222,
                    "longitude": 71.4669,
                    "timezone": "Asia/Almaty"
                },
            ]
            
            # Insert if not exists
            for airport in sample_airports:
                await db.airports.update_one(
                    {"iata_code": airport["iata_code"]},
                    {"$set": airport},
                    upsert=True
                )
            
            logger.info("sample_airports_seeded", count=len(sample_airports))
        
        except Exception as e:
            logger.error("seed_airports_error", error=str(e))
