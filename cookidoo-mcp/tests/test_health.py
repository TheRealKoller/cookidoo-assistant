import pytest
from fastapi.testclient import TestClient

def test_health_endpoint_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "cookidoo-mcp"
    assert data["version"] == "0.1.0"
    assert "cookidoo_connected" in data

def test_health_endpoint_accessible_without_auth(client):
    # Health should not require authentication
    response = client.get("/health")
    assert response.status_code == 200
