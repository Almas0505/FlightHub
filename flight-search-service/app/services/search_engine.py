"""
Flight Search Engine
Агрегирует результаты от нескольких провайдеров параллельно
"""
import asyncio
from typing import List
import time
import uuid
import structlog

from app.models.flight import SearchRequest, SearchResponse, Flight
from app.providers import MockFlightProvider, AmadeusProvider
from app.config import settings
from app.database.mongodb import get_database

logger = structlog.get_logger()


class FlightSearchEngine:
    """Main flight search engine"""
    
    def __init__(self):
        self.providers = []
        
        # Initialize providers based on configuration
        if settings.USE_MOCK_PROVIDER:
            self.providers.append(MockFlightProvider())
        
        if settings.AMADEUS_API_KEY:
            self.providers.append(AmadeusProvider())
        
        # Add more providers here (Sabre, etc.)
        
        logger.info("search_engine_initialized", providers_count=len(self.providers))
    
    async def search(self, search_request: SearchRequest) -> SearchResponse:
        """
        Search for flights across all providers
        
        Args:
            search_request: Search parameters
            
        Returns:
            SearchResponse with aggregated results
        """
        
        search_id = str(uuid.uuid4())
        start_time = time.time()
        
        logger.info(
            "search_started",
            search_id=search_id,
            from_airport=search_request.from_airport,
            to_airport=search_request.to_airport,
            providers_count=len(self.providers)
        )
        
        # Check cache first
        cache_key = search_request.cache_key()
        cached_result = await self._get_from_cache(cache_key)
        
        if cached_result:
            duration_ms = (time.time() - start_time) * 1000
            logger.info("search_cache_hit", search_id=search_id, duration_ms=duration_ms)
            
            return SearchResponse(
                search_id=search_id,
                flights=cached_result["flights"],
                total=len(cached_result["flights"]),
                from_cache=True,
                search_duration_ms=duration_ms,
                providers_used=cached_result.get("providers", [])
            )
        
        # Search across all providers in parallel
        tasks = []
        for provider in self.providers:
            task = self._search_with_provider(provider, search_request)
            tasks.append(task)
        
        # Gather results with timeout
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            logger.error("search_gather_error", error=str(e))
            results = []
        
        # Aggregate flights from all providers
        all_flights = []
        providers_used = []
        
        for result in results:
            if isinstance(result, list):
                all_flights.extend(result)
                if result:  # Provider returned results
                    providers_used.append(result[0].provider if result else "unknown")
            elif isinstance(result, Exception):
                logger.warning("provider_error", error=str(result))
        
        # Deduplicate and sort
        flights = self._deduplicate_flights(all_flights)
        flights = self._sort_flights(flights)
        
        # Limit results
        flights = flights[:settings.MAX_RESULTS_PER_PROVIDER * len(self.providers)]
        
        duration_ms = (time.time() - start_time) * 1000
        
        logger.info(
            "search_completed",
            search_id=search_id,
            flights_count=len(flights),
            duration_ms=duration_ms,
            providers_used=providers_used
        )
        
        # Save individual flights to database for later retrieval
        await self._save_flights_to_db(flights)
        
        # Cache results
        await self._save_to_cache(cache_key, flights, providers_used)
        
        return SearchResponse(
            search_id=search_id,
            flights=flights,
            total=len(flights),
            from_cache=False,
            search_duration_ms=duration_ms,
            providers_used=list(set(providers_used))
        )
    
    async def _search_with_provider(
        self,
        provider,
        search_request: SearchRequest
    ) -> List[Flight]:
        """Search with a single provider with timeout"""
        
        try:
            # Wrap provider search in timeout
            return await asyncio.wait_for(
                provider.search_flights(search_request),
                timeout=settings.SEARCH_TIMEOUT_SECONDS
            )
        
        except asyncio.TimeoutError:
            logger.warning(
                "provider_timeout",
                provider=provider.name,
                timeout=settings.SEARCH_TIMEOUT_SECONDS
            )
            return []
        
        except Exception as e:
            logger.error(
                "provider_search_error",
                provider=provider.name,
                error=str(e),
                exc_info=True
            )
            return []
    
    def _deduplicate_flights(self, flights: List[Flight]) -> List[Flight]:
        """Remove duplicate flights"""
        
        seen = set()
        unique_flights = []
        
        for flight in flights:
            # Create unique key based on flight details
            key = (
                flight.segments[0].flight_number,
                flight.segments[0].departure.datetime,
                flight.segments[0].departure.airport_code,
                flight.segments[0].arrival.airport_code,
            )
            
            if key not in seen:
                seen.add(key)
                unique_flights.append(flight)
        
        return unique_flights
    
    def _sort_flights(self, flights: List[Flight]) -> List[Flight]:
        """Sort flights by price (cheapest first)"""
        return sorted(flights, key=lambda x: x.price.total)
    
    async def _get_from_cache(self, cache_key: str) -> dict:
        """Get cached search results"""
        
        try:
            db = get_database()
            cached = await db.search_cache.find_one({"search_key": cache_key})
            
            if cached:
                return {
                    "flights": [Flight(**f) for f in cached.get("flights", [])],
                    "providers": cached.get("providers", [])
                }
            
            return None
        
        except Exception as e:
            logger.error("cache_get_error", error=str(e))
            return None
    
    async def _save_flights_to_db(self, flights: List[Flight]):
        """Save individual flights to database for later retrieval"""
        
        try:
            db = get_database()
            
            # Convert flights to dict and add expiry timestamp (24 hours)
            current_time = time.time()
            expiry_time = current_time + (24 * 60 * 60)  # 24 hours
            
            for flight in flights:
                flight_data = flight.model_dump()
                flight_data['created_at'] = current_time
                flight_data['expires_at'] = expiry_time
                
                # Upsert flight by id
                await db.flights.update_one(
                    {"id": flight.id},
                    {"$set": flight_data},
                    upsert=True
                )
            
            # Create TTL index on expires_at field (auto-delete expired flights)
            await db.flights.create_index("expires_at", expireAfterSeconds=0)
            
            logger.debug("flights_saved_to_db", count=len(flights))
        
        except Exception as e:
            logger.error("flights_save_error", error=str(e))
    
    async def _save_to_cache(
        self,
        cache_key: str,
        flights: List[Flight],
        providers: List[str]
    ):
        """Save search results to cache"""
        
        try:
            db = get_database()
            
            # Convert flights to dict
            flights_data = [flight.model_dump() for flight in flights]
            
            await db.search_cache.update_one(
                {"search_key": cache_key},
                {
                    "$set": {
                        "search_key": cache_key,
                        "flights": flights_data,
                        "providers": providers,
                        "created_at": time.time(),
                    }
                },
                upsert=True
            )
            
            logger.debug("cache_saved", cache_key=cache_key)
        
        except Exception as e:
            logger.error("cache_save_error", error=str(e))
    
    async def get_flight_by_id(self, flight_id: str) -> Flight:
        """Get specific flight details"""
        
        try:
            db = get_database()
            flight_data = await db.flights.find_one({"id": flight_id})
            
            if flight_data:
                return Flight(**flight_data)
            
            return None
        
        except Exception as e:
            logger.error("get_flight_error", flight_id=flight_id, error=str(e))
            return None
