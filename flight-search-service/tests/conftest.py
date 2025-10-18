"""
Test configuration and fixtures
"""
import pytest
import asyncio
from typing import Generator
from httpx import AsyncClient

from app.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def async_client() -> AsyncClient:
    """Create async test client"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
