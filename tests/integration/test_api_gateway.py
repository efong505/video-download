"""
Integration tests for API Gateway endpoints
"""
import pytest
import requests
import json


# API Gateway base URL
API_BASE_URL = "https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod"


@pytest.mark.integration
class TestAPIGatewayEndpoints:
    """Integration tests for API Gateway endpoints"""
    
    def test_cors_preflight_auth_endpoint(self):
        """Test CORS preflight request to /auth endpoint"""
        response = requests.options(
            f"{API_BASE_URL}/auth",
            headers={
                "Origin": "https://example.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        assert response.status_code == 200
        assert "Access-Control-Allow-Origin" in response.headers
        assert "Access-Control-Allow-Methods" in response.headers
        assert "Access-Control-Allow-Headers" in response.headers
    
    def test_cors_preflight_articles_endpoint(self):
        """Test CORS preflight request to /articles endpoint"""
        response = requests.options(
            f"{API_BASE_URL}/articles",
            headers={
                "Origin": "https://example.com",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        assert response.status_code == 200
        assert response.headers.get("Access-Control-Allow-Origin") == "*"
    
    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoint returns 404"""
        response = requests.get(f"{API_BASE_URL}/nonexistent")
        
        assert response.status_code in [403, 404]  # API Gateway returns 403 for missing resources
    
    def test_auth_endpoint_requires_body(self):
        """Test that /auth endpoint requires request body"""
        response = requests.post(
            f"{API_BASE_URL}/auth?action=login",
            headers={"Content-Type": "application/json"}
        )
        
        # Should return 400 or 500 for missing body
        assert response.status_code in [400, 500]
    
    def test_articles_endpoint_accessible(self):
        """Test that /articles endpoint is accessible"""
        response = requests.get(f"{API_BASE_URL}/articles?action=list")
        
        # Should return 200 or 401 (if auth required)
        assert response.status_code in [200, 401, 403]
    
    @pytest.mark.slow
    def test_all_endpoints_respond(self):
        """Test that all API endpoints respond (smoke test)"""
        endpoints = [
            "/auth",
            "/admin",
            "/articles",
            "/news",
            "/comments",
            "/contributors",
            "/resources",
            "/videos",
            "/tags",
            "/download",
            "/paypal",
            "/analyze",
            "/prayer",
            "/notifications"
        ]
        
        for endpoint in endpoints:
            response = requests.options(f"{API_BASE_URL}{endpoint}")
            
            # OPTIONS should always return 200 for CORS
            assert response.status_code == 200, f"Endpoint {endpoint} failed CORS preflight"
            assert "Access-Control-Allow-Origin" in response.headers


@pytest.mark.integration
class TestAPIGatewayErrorHandling:
    """Test API Gateway error handling"""
    
    def test_malformed_json_returns_error(self):
        """Test that malformed JSON returns appropriate error"""
        response = requests.post(
            f"{API_BASE_URL}/auth?action=login",
            headers={"Content-Type": "application/json"},
            data="invalid json {{"
        )
        
        assert response.status_code in [400, 500]
    
    def test_missing_content_type_header(self):
        """Test request without Content-Type header"""
        response = requests.post(
            f"{API_BASE_URL}/auth?action=login",
            data=json.dumps({"email": "test@example.com", "password": "test"})
        )
        
        # Should still process or return appropriate error
        assert response.status_code in [200, 400, 401, 500]


# Skip integration tests by default (run with: pytest -m integration)
pytestmark = pytest.mark.integration
