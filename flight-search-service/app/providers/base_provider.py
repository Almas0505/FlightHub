"""
Base provider interface for flight search
"""
from abc import ABC, abstractmethod
from typing import List
import structlog

from app.models.flight import SearchRequest, Flight

logger = structlog.get_logger()


class BaseFlightProvider(ABC):
    """Base class for flight providers"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logger.bind(provider=name)
    
    @abstractmethod
    async def search_flights(self, search_request: SearchRequest) -> List[Flight]:
        """
        Search for flights
        
        Args:
            search_request: Search parameters
            
        Returns:
            List of Flight objects
        """
        pass
    
    async def health_check(self) -> bool:
        """
        Check if provider is available
        
        Returns:
            True if provider is healthy
        """
        try:
            # Override in subclass if needed
            return True
        except Exception as e:
            self.logger.error("provider_health_check_failed", error=str(e))
            return False
