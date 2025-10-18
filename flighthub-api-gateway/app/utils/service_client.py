"""
HTTP client for communicating with microservices
"""
import aiohttp
import asyncio
from typing import Optional, Dict, Any
import structlog
from enum import Enum

from app.config import settings

logger = structlog.get_logger()


class ServiceType(str, Enum):
    """Microservice types"""
    FLIGHT_SEARCH = "flight_search"
    BOOKING = "booking"
    PAYMENT = "payment"
    NOTIFICATION = "notification"
    USER = "user"


class ServiceClient:
    """HTTP client for microservices with circuit breaker"""
    
    # Service URL mapping
    SERVICE_URLS = {
        ServiceType.FLIGHT_SEARCH: settings.FLIGHT_SEARCH_URL,
        ServiceType.BOOKING: settings.BOOKING_SERVICE_URL,
        ServiceType.PAYMENT: settings.PAYMENT_SERVICE_URL,
        ServiceType.NOTIFICATION: settings.NOTIFICATION_SERVICE_URL,
        ServiceType.USER: settings.USER_SERVICE_URL,
    }
    
    # Circuit breaker state
    _circuit_state: Dict[str, Dict] = {}
    
    def __init__(self, service: ServiceType):
        self.service = service
        self.base_url = self.SERVICE_URLS[service]
        self.timeout = aiohttp.ClientTimeout(total=settings.SERVICE_TIMEOUT)
        
        # Initialize circuit breaker state
        if service not in self._circuit_state:
            self._circuit_state[service] = {
                "failures": 0,
                "last_failure": None,
                "state": "closed"  # closed, open, half_open
            }
    
    async def get(self, path: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[Any, Any]:
        """GET request"""
        return await self._request("GET", path, params=params, headers=headers)
    
    async def post(self, path: str, json: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[Any, Any]:
        """POST request"""
        return await self._request("POST", path, json=json, headers=headers)
    
    async def put(self, path: str, json: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[Any, Any]:
        """PUT request"""
        return await self._request("PUT", path, json=json, headers=headers)
    
    async def delete(self, path: str, headers: Optional[Dict] = None) -> Dict[Any, Any]:
        """DELETE request"""
        return await self._request("DELETE", path, headers=headers)
    
    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[Any, Any]:
        """Execute HTTP request with circuit breaker"""
        
        # Check circuit breaker
        if not await self._check_circuit_breaker():
            raise ServiceUnavailableError(
                f"Service {self.service} is temporarily unavailable (circuit breaker open)"
            )
        
        url = f"{self.base_url}{path}"
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                # Log outgoing request data
                logger.info(
                    "service_request_sending",
                    service=self.service,
                    method=method,
                    path=path,
                    json_data=json
                )
                
                async with session.request(
                    method,
                    url,
                    params=params,
                    json=json,
                    headers=headers
                ) as response:
                    
                    # Log request
                    logger.info(
                        "service_request",
                        service=self.service,
                        method=method,
                        path=path,
                        status=response.status
                    )
                    
                    # Handle response
                    if response.status >= 500:
                        await self._record_failure()
                        raise ServiceError(
                            f"Service {self.service} returned {response.status}",
                            status_code=response.status
                        )
                    
                    if response.status >= 400:
                        try:
                            error_data = await response.json()
                        except:
                            error_text = await response.text()
                            logger.error(
                                "service_error_response",
                                service=self.service,
                                status=response.status,
                                response_text=error_text
                            )
                            raise ServiceError(
                                f"Service error: {error_text}",
                                status_code=response.status
                            )
                        
                        logger.error(
                            "service_error_response",
                            service=self.service,
                            status=response.status,
                            error_data=error_data
                        )
                        raise ServiceError(
                            error_data.get("message", "Service error"),
                            status_code=response.status,
                            details=error_data
                        )
                    
                    # Success
                    await self._record_success()
                    return await response.json()
        
        except aiohttp.ClientError as e:
            await self._record_failure()
            logger.error(
                "service_request_failed",
                service=self.service,
                error=str(e)
            )
            raise ServiceUnavailableError(f"Failed to connect to {self.service}: {str(e)}")
        
        except asyncio.TimeoutError:
            await self._record_failure()
            logger.error("service_timeout", service=self.service)
            raise ServiceTimeoutError(f"Request to {self.service} timed out")
    
    async def _check_circuit_breaker(self) -> bool:
        """Check if circuit breaker allows request"""
        if not settings.CIRCUIT_BREAKER_ENABLED:
            return True
        
        state = self._circuit_state[self.service]
        
        if state["state"] == "closed":
            return True
        
        if state["state"] == "open":
            # Check if timeout has passed
            import time
            if state["last_failure"] and \
               time.time() - state["last_failure"] > settings.CIRCUIT_BREAKER_TIMEOUT:
                state["state"] = "half_open"
                logger.info("circuit_breaker_half_open", service=self.service)
                return True
            return False
        
        if state["state"] == "half_open":
            return True
        
        return False
    
    async def _record_failure(self):
        """Record service failure"""
        if not settings.CIRCUIT_BREAKER_ENABLED:
            return
        
        import time
        state = self._circuit_state[self.service]
        state["failures"] += 1
        state["last_failure"] = time.time()
        
        if state["failures"] >= settings.CIRCUIT_BREAKER_THRESHOLD:
            state["state"] = "open"
            logger.warning(
                "circuit_breaker_opened",
                service=self.service,
                failures=state["failures"]
            )
    
    async def _record_success(self):
        """Record service success"""
        if not settings.CIRCUIT_BREAKER_ENABLED:
            return
        
        state = self._circuit_state[self.service]
        
        if state["state"] == "half_open":
            state["state"] = "closed"
            state["failures"] = 0
            logger.info("circuit_breaker_closed", service=self.service)
        else:
            state["failures"] = max(0, state["failures"] - 1)


# Custom exceptions
class ServiceError(Exception):
    """Base service error"""
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict] = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class ServiceUnavailableError(ServiceError):
    """Service unavailable error"""
    def __init__(self, message: str):
        super().__init__(message, status_code=503)


class ServiceTimeoutError(ServiceError):
    """Service timeout error"""
    def __init__(self, message: str):
        super().__init__(message, status_code=504)
