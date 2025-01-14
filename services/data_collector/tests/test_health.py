# tests/test_health.py
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.api.health import router
from unittest.mock import MagicMock

@pytest.fixture
def mock_s3_client():
    client = MagicMock()
    client.list_buckets.return_value = {'Buckets': []}
    return client

@pytest.fixture
def mock_opensearch_client():
    client = MagicMock()
    client.ping.return_value = True
    return client

@pytest.fixture
def test_app(mock_s3_client, mock_opensearch_client):
    # Create a FastAPI app and include our router
    app = FastAPI()
    app.include_router(router)
    
    # Add mock clients to app state
    app.state.s3_client = mock_s3_client
    app.state.os_client = mock_opensearch_client
    
    # Create test client
    return TestClient(app)

def test_health_check_healthy(test_app):
    response = test_app.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["services"]["s3"] == "healthy"
    assert data["services"]["opensearch"] == "healthy"

def test_health_check_degraded(test_app, mock_opensearch_client):
    # Make OpenSearch unhealthy
    mock_opensearch_client.ping.return_value = False
    
    response = test_app.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "degraded"
    assert data["services"]["opensearch"] == "unhealthy"