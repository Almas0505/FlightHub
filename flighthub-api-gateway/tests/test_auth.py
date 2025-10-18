"""
Tests for authentication middleware
"""
import pytest
from fastapi.testclient import TestClient
import jwt

from app.config import settings
from app.middleware.auth import create_access_token


def test_access_public_endpoint_without_token(client: TestClient):
    """Test accessing public endpoint without authentication"""
    response = client.get("/health/live")
    assert response.status_code == 200


def test_access_protected_endpoint_without_token(client: TestClient):
    """Test accessing protected endpoint without token"""
    response = client.get("/api/v1/bookings")
    assert response.status_code == 401
    assert "Authentication required" in response.json()["error"]


def test_access_protected_endpoint_with_invalid_token(client: TestClient):
    """Test accessing protected endpoint with invalid token"""
    headers = {"Authorization": "Bearer invalid-token-here"}
    response = client.get("/api/v1/bookings", headers=headers)
    assert response.status_code == 401


def test_access_protected_endpoint_with_valid_token(client: TestClient, auth_headers: dict):
    """Test accessing protected endpoint with valid token"""
    # Note: This will fail because we don't have actual booking service running
    # But it tests that authentication passes
    response = client.get("/api/v1/bookings", headers=auth_headers)
    # Should get past auth (401) but fail on service call
    assert response.status_code != 401


def test_expired_token(client: TestClient):
    """Test expired token"""
    from datetime import datetime, timedelta
    
    # Create expired token
    payload = {
        "user_id": "test-user",
        "exp": datetime.utcnow() - timedelta(minutes=1)
    }
    expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/api/v1/bookings", headers=headers)
    assert response.status_code == 401
    assert "expired" in response.json()["error"].lower()


def test_create_access_token():
    """Test JWT token creation"""
    user_data = {"user_id": "test-123"}
    token = create_access_token(user_data)
    
    # Decode and verify
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    assert payload["user_id"] == "test-123"
    assert payload["type"] == "access"
    assert "exp" in payload
