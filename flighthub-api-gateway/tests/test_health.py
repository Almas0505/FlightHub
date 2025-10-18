"""
Tests for health check endpoints
"""
import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "FlightHub API Gateway"
    assert data["status"] == "operational"


def test_liveness_probe(client: TestClient):
    """Test liveness probe"""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data


def test_readiness_probe(client: TestClient):
    """Test readiness probe"""
    response = client.get("/health/ready")
    assert response.status_code in [200, 503]
    data = response.json()
    assert "status" in data
    assert "checks" in data


def test_general_health_check(client: TestClient):
    """Test general health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "FlightHub API Gateway"
