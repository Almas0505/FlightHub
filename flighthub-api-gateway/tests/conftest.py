"""
Test configuration and fixtures
"""
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app
from app.config import settings


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client() -> TestClient:
    """Create test client"""
    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncGenerator:
    """Create async test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def test_token() -> str:
    """Create test JWT token"""
    from app.middleware.auth import create_access_token
    
    return create_access_token({"user_id": "test-user-123"})


@pytest.fixture
def auth_headers(test_token: str) -> dict:
    """Create authorization headers"""
    return {"Authorization": f"Bearer {test_token}"}
