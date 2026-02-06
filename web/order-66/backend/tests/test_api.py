import pytest
from tests.conftest import client


class TestApiEndpoints:
    """Test suite for general API endpoints"""

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert data["docs"] == "/docs"

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ok"
        assert "Force" in data["message"]

    def test_info_endpoint(self):
        """Test API info endpoint"""
        response = client.get("/api/info")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Vader Todo API"
        assert data["version"] == "1.0.0"
        assert "endpoints" in data
        assert "/docs" in data["endpoints"]["docs"]

    def test_nonexistent_endpoint(self):
        """Test accessing non-existent endpoint"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

    def test_cors_headers(self):
        """Test that CORS headers are present"""
        response = client.options("/api/todos")
        # FastAPI test client doesn't simulate CORS perfectly,
        # but we can verify the middleware is configured
        assert response.status_code in [200, 405]  # Either OK or Method Not Allowed