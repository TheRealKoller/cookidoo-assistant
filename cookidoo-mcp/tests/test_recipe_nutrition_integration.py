import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient


@pytest.fixture
def mock_nutrition_result():
    """Mock nutrition result."""
    return {
        "recipe_id": "r123456",
        "serving_size": 4,
        "calories": 450.0,
        "protein": 25.5,
        "carbohydrates": 50.0,
        "fat": 15.0,
        "fiber": 8.0,
        "sugar": 12.0,
        "sodium": 500.0,
        "saturated_fat": 3.5,
        "nutrients": [
            {"value": 450.0, "unit": "kcal", "type": "energy"},
            {"value": 25.5, "unit": "g", "type": "protein"},
            {"value": 50.0, "unit": "g", "type": "carbohydrate"},
            {"value": 15.0, "unit": "g", "type": "fat"},
            {"value": 8.0, "unit": "g", "type": "fiber"},
            {"value": 12.0, "unit": "g", "type": "sugar"},
            {"value": 500.0, "unit": "mg", "type": "sodium"},
            {"value": 3.5, "unit": "g", "type": "saturated fat"},
        ],
    }


def test_get_recipe_nutrition_endpoint_success(client, mock_nutrition_result):
    """Test get_recipe_nutrition endpoint with successful request."""
    with patch("src.server.get_recipe_nutrition") as mock_get:
        mock_get.return_value = MagicMock(model_dump=lambda: mock_nutrition_result)
        
        response = client.post(
            "/tools/get_recipe_nutrition",
            params={"recipe_id": "r123456"},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["recipe_id"] == "r123456"
        assert data["serving_size"] == 4
        assert data["calories"] == 450.0
        assert data["protein"] == 25.5
        assert data["carbohydrates"] == 50.0
        assert data["fat"] == 15.0
        assert data["fiber"] == 8.0
        assert data["sugar"] == 12.0
        assert data["sodium"] == 500.0
        assert data["saturated_fat"] == 3.5
        assert len(data["nutrients"]) == 8


def test_get_recipe_nutrition_endpoint_no_nutrition(client):
    """Test endpoint with recipe that has no nutrition data."""
    mock_result = {
        "recipe_id": "r999999",
        "serving_size": 2,
        "calories": None,
        "protein": None,
        "carbohydrates": None,
        "fat": None,
        "fiber": None,
        "sugar": None,
        "sodium": None,
        "saturated_fat": None,
        "nutrients": [],
    }
    
    with patch("src.server.get_recipe_nutrition") as mock_get:
        mock_get.return_value = MagicMock(model_dump=lambda: mock_result)
        
        response = client.post(
            "/tools/get_recipe_nutrition",
            params={"recipe_id": "r999999"},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["recipe_id"] == "r999999"
        assert data["calories"] is None
        assert data["protein"] is None
        assert len(data["nutrients"]) == 0


def test_get_recipe_nutrition_endpoint_invalid_id(client):
    """Test endpoint with invalid recipe ID."""
    with patch("src.server.get_recipe_nutrition") as mock_get:
        mock_get.side_effect = ValueError("recipe_id is required")
        
        response = client.post(
            "/tools/get_recipe_nutrition",
            params={"recipe_id": ""},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 404
        assert "error" in response.json()


def test_get_recipe_nutrition_endpoint_recipe_not_found(client):
    """Test endpoint with non-existent recipe."""
    with patch("src.server.get_recipe_nutrition") as mock_get:
        mock_get.side_effect = ValueError("Failed to get recipe nutrition")
        
        response = client.post(
            "/tools/get_recipe_nutrition",
            params={"recipe_id": "invalid_recipe"},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 404
        assert "error" in response.json()


def test_get_recipe_nutrition_endpoint_internal_error(client):
    """Test endpoint with internal error."""
    with patch("src.server.get_recipe_nutrition") as mock_get:
        mock_get.side_effect = Exception("Internal error")
        
        response = client.post(
            "/tools/get_recipe_nutrition",
            params={"recipe_id": "r123456"},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 500
        assert "error" in response.json()


def test_get_recipe_nutrition_endpoint_no_auth(client):
    """Test endpoint without authentication."""
    response = client.post(
        "/tools/get_recipe_nutrition",
        params={"recipe_id": "r123456"},
    )
    
    assert response.status_code == 401


def test_get_recipe_nutrition_endpoint_invalid_auth(client):
    """Test endpoint with invalid API key."""
    response = client.post(
        "/tools/get_recipe_nutrition",
        params={"recipe_id": "r123456"},
        headers={"X-API-Key": "wrong_key"},
    )
    
    assert response.status_code == 401


def test_get_recipe_nutrition_endpoint_partial_data(client):
    """Test endpoint with partial nutrition data."""
    mock_result = {
        "recipe_id": "r555555",
        "serving_size": 2,
        "calories": 300.0,
        "protein": 20.0,
        "carbohydrates": None,
        "fat": None,
        "fiber": None,
        "sugar": None,
        "sodium": None,
        "saturated_fat": None,
        "nutrients": [
            {"value": 300.0, "unit": "kcal", "type": "energy"},
            {"value": 20.0, "unit": "g", "type": "protein"},
        ],
    }
    
    with patch("src.server.get_recipe_nutrition") as mock_get:
        mock_get.return_value = MagicMock(model_dump=lambda: mock_result)
        
        response = client.post(
            "/tools/get_recipe_nutrition",
            params={"recipe_id": "r555555"},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["calories"] == 300.0
        assert data["protein"] == 20.0
        assert data["carbohydrates"] is None
        assert data["fat"] is None
        assert len(data["nutrients"]) == 2
