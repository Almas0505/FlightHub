"""
Amadeus GDS provider
Реальная интеграция с Amadeus API
"""
from typing import List
import aiohttp
from datetime import datetime, timedelta
import uuid

from app.providers.base_provider import BaseFlightProvider
from app.models.flight import SearchRequest, Flight
from app.config import settings


class AmadeusProvider(BaseFlightProvider):
    """Amadeus GDS integration"""
    
    def __init__(self):
        super().__init__("amadeus")
        self.api_key = settings.AMADEUS_API_KEY
        self.api_secret = settings.AMADEUS_API_SECRET
        self.base_url = settings.AMADEUS_BASE_URL
        self._access_token = None
        self._token_expires_at = None
    
    async def search_flights(self, search_request: SearchRequest) -> List[Flight]:
        """
        Search flights via Amadeus API
        
        Note: Requires valid Amadeus API credentials
        For production, implement full OAuth flow and response parsing
        """
        
        if not self.api_key or not self.api_secret:
            self.logger.warning("amadeus_credentials_missing")
            return []
        
        try:
            # Get access token
            token = await self._get_access_token()
            
            if not token:
                return []
            
            # Build search params
            params = {
                "originLocationCode": search_request.from_airport,
                "destinationLocationCode": search_request.to_airport,
                "departureDate": search_request.departure_date.strftime("%Y-%m-%d"),
                "adults": search_request.passengers,
                "travelClass": search_request.cabin_class.value.upper(),
                "nonStop": search_request.direct_only,
                "max": settings.MAX_RESULTS_PER_PROVIDER,
            }
            
            if search_request.return_date:
                params["returnDate"] = search_request.return_date.strftime("%Y-%m-%d")
            
            # Make API request
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/shopping/flight-offers",
                    params=params,
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=aiohttp.ClientTimeout(total=settings.SEARCH_TIMEOUT_SECONDS)
                ) as response:
                    
                    if response.status != 200:
                        self.logger.error(
                            "amadeus_search_failed",
                            status=response.status,
                            response=await response.text()
                        )
                        return []
                    
                    data = await response.json()
                    
                    # Parse response and convert to our Flight model
                    flights = self._parse_amadeus_response(data)
                    
                    self.logger.info(
                        "amadeus_search_completed",
                        flights_count=len(flights)
                    )
                    
                    return flights
        
        except Exception as e:
            self.logger.error("amadeus_search_error", error=str(e), exc_info=True)
            return []
    
    async def _get_access_token(self) -> str:
        """Get OAuth access token from Amadeus"""
        
        # Check if token is still valid
        if self._access_token and self._token_expires_at:
            if datetime.utcnow() < self._token_expires_at:
                return self._access_token
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url.replace('/v2', '')}/v1/security/oauth2/token",
                    data={
                        "grant_type": "client_credentials",
                        "client_id": self.api_key,
                        "client_secret": self.api_secret,
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                ) as response:
                    
                    if response.status != 200:
                        self.logger.error("amadeus_auth_failed", status=response.status)
                        return None
                    
                    data = await response.json()
                    
                    self._access_token = data.get("access_token")
                    expires_in = data.get("expires_in", 1800)
                    self._token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in - 60)
                    
                    self.logger.info("amadeus_token_obtained")
                    
                    return self._access_token
        
        except Exception as e:
            self.logger.error("amadeus_auth_error", error=str(e))
            return None
    
    def _parse_amadeus_response(self, data: dict) -> List[Flight]:
        """
        Parse Amadeus API response to our Flight model
        
        Note: This is a simplified example. Real implementation needs
        to handle complex Amadeus response structure with:
        - Multiple segments
        - Price variations
        - Fare rules
        - Baggage allowances
        - etc.
        """
        
        flights = []
        
        # Amadeus returns data in specific format
        offers = data.get("data", [])
        
        for offer in offers:
            try:
                # Convert Amadeus offer to our Flight model
                # This is simplified - real implementation is more complex
                
                flight_id = offer.get("id", f"AM-{uuid.uuid4().hex[:12]}")
                
                # Parse itineraries, prices, etc.
                # For production, use proper Amadeus SDK or detailed parsing
                
                # For now, skip if invalid format
                if not offer.get("itineraries"):
                    continue
                
                # TODO: Implement full Amadeus response parsing
                # This requires understanding Amadeus data structure
                
                self.logger.debug("amadeus_offer_parsed", offer_id=flight_id)
            
            except Exception as e:
                self.logger.warning("amadeus_offer_parse_error", error=str(e))
                continue
        
        return flights
    
    async def health_check(self) -> bool:
        """Check Amadeus API availability"""
        try:
            token = await self._get_access_token()
            return token is not None
        except Exception:
            return False
