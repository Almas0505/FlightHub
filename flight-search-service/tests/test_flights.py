"""
Tests for Flight Search Service
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """Test health check endpoint"""
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Flight Search Service"


@pytest.mark.asyncio
async def test_liveness_probe(async_client: AsyncClient):
    """Test liveness probe"""
    response = await async_client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"


@pytest.mark.asyncio
async def test_search_flights_invalid_params(async_client: AsyncClient):
    """Test search with invalid parameters"""
    # Same departure and arrival
    response = await async_client.get(
        "/search",
        params={
            "from_airport": "ALA",
            "to_airport": "ALA",
            "departure_date": "2025-11-01"
        }
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_search_flights_valid(async_client: AsyncClient):
    """Test successful flight search"""
    response = await async_client.get(
        "/search",
        params={
            "from_airport": "ALA",
            "to_airport": "DXB",
            "departure_date": "2025-11-01",
            "passengers": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "flights" in data
    assert "search_id" in data
    assert data["total"] >= 0


@pytest.mark.asyncio
async def test_airport_search(async_client: AsyncClient):
    """Test airport search"""
    response = await async_client.get(
        "/airports",
        params={"query": "Almaty"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "airports" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_popular_routes(async_client: AsyncClient):
    """Test popular routes endpoint"""
    response = await async_client.get("/popular-routes")
    assert response.status_code == 200
    data = response.json()
    assert "routes" in data
    assert len(data["routes"]) > 0
