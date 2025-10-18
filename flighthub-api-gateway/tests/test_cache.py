"""
Tests for cache functionality
"""
import pytest
from app.utils.cache import CacheService, cache_key


@pytest.mark.asyncio
async def test_cache_set_and_get():
    """Test setting and getting cache"""
    key = "test:key"
    value = {"data": "test", "number": 42}
    
    # Set cache
    result = await CacheService.set(key, value, ttl=60)
    assert result is True
    
    # Get cache
    cached = await CacheService.get(key)
    assert cached == value


@pytest.mark.asyncio
async def test_cache_get_nonexistent():
    """Test getting non-existent cache key"""
    result = await CacheService.get("nonexistent:key")
    assert result is None


@pytest.mark.asyncio
async def test_cache_delete():
    """Test deleting cache"""
    key = "test:delete"
    
    # Set cache
    await CacheService.set(key, {"test": "data"})
    
    # Verify it exists
    cached = await CacheService.get(key)
    assert cached is not None
    
    # Delete
    result = await CacheService.delete(key)
    assert result is True
    
    # Verify it's gone
    cached = await CacheService.get(key)
    assert cached is None


def test_cache_key_generation():
    """Test cache key generation"""
    key1 = cache_key("search", from_city="ALA", to_city="DXB")
    key2 = cache_key("search", to_city="DXB", from_city="ALA")  # Different order
    
    # Should be the same (sorted kwargs)
    assert key1 == key2
    
    key3 = cache_key("search", "ALA", "DXB")
    assert "ALA" in key3 and "DXB" in key3
