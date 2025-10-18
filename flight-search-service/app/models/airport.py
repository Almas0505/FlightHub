"""
Pydantic models for Airport data
"""
from pydantic import BaseModel, Field
from typing import Optional


class AirportModel(BaseModel):
    """Airport data model"""
    iata_code: str = Field(..., min_length=3, max_length=3, description="3-letter IATA code")
    icao_code: Optional[str] = Field(None, min_length=4, max_length=4, description="4-letter ICAO code")
    
    name: str = Field(..., description="Airport name")
    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country name")
    country_code: str = Field(..., min_length=2, max_length=2, description="ISO country code")
    
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    timezone: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "iata_code": "ALA",
                "icao_code": "UAAA",
                "name": "Almaty International Airport",
                "city": "Almaty",
                "country": "Kazakhstan",
                "country_code": "KZ",
                "latitude": 43.3521,
                "longitude": 77.0405,
                "timezone": "Asia/Almaty"
            }
        }


class AirportSearchResponse(BaseModel):
    """Airport search response"""
    airports: list[AirportModel]
    total: int
