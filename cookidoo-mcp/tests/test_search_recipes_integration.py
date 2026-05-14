import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient


@pytest.fixture
def mock_search_results():
    """Mock search results."""
    return {
        "recipes": [
            {
                "id": "r001",
                "title": "Pasta Carbonara",
                "description": "Italian classic",
                "image_url": "http://example.com/image1.jpg",
                "cooking_time": 30,
                "difficulty": "medium",
            },
            {
                "id": "r002",
                "title": "Vegetable Soup",
                "description": "Healthy soup",
                "image_url": None,
                "cooking_time": 40,
                "difficulty": "easy",
            },
        ],
        "total": 2,
        "offset": 0,
        "limit": 20,
    }


def test_search_recipes_endpoint_basic(client, mock_search_results):
    """Test search_recipes endpoint with basic request."""
    with patch("src.server.search_recipes") as mock_search:
        mock_search.return_value = MagicMock(model_dump=lambda: mock_search_results)
        
        response = client.post(
            "/tools/search_recipes",
            json={},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["recipes"]) == 2
        assert data["recipes"][0]["title"] == "Pasta Carbonara"


def test_search_recipes_endpoint_with_query(client, mock_search_results):
    """Test search_recipes endpoint with query parameter."""
    with patch("src.server.search_recipes") as mock_search:
        mock_search.return_value = MagicMock(
            model_dump=lambda: {
                "recipes": [mock_search_results["recipes"][0]],
                "total": 1,
                "offset": 0,
                "limit": 20,
            }
        )
        
        response = client.post(
            "/tools/search_recipes",
            json={"query": "pasta"},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["recipes"][0]["title"] == "Pasta Carbonara"


def test_search_recipes_endpoint_with_ingredients(client, mock_search_results):
    """Test search_recipes endpoint with ingredient filter."""
    with patch("src.server.search_recipes") as mock_search:
        mock_search.return_value = MagicMock(model_dump=lambda: mock_search_results)
        
        response = client.post(
            "/tools/search_recipes",
            json={"ingredients": ["tomato", "basil"]},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "recipes" in data


def test_search_recipes_endpoint_with_diet(client, mock_search_results):
    """Test search_recipes endpoint with diet filter."""
    with patch("src.server.search_recipes") as mock_search:
        mock_search.return_value = MagicMock(model_dump=lambda: mock_search_results)
        
        response = client.post(
            "/tools/search_recipes",
            json={"diet": "vegan"},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "recipes" in data


def test_search_recipes_endpoint_with_exclude(client, mock_search_results):
    """Test search_recipes endpoint with ingredient exclusion."""
    with patch("src.server.search_recipes") as mock_search:
        mock_search.return_value = MagicMock(model_dump=lambda: mock_search_results)
        
        response = client.post(
            "/tools/search_recipes",
            json={"exclude_ingredients": ["nuts"]},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "recipes" in data


def test_search_recipes_endpoint_pagination(client, mock_search_results):
    """Test search_recipes endpoint with pagination."""
    with patch("src.server.search_recipes") as mock_search:
        paginated = mock_search_results.copy()
        paginated["recipes"] = [mock_search_results["recipes"][0]]
        paginated["offset"] = 0
        paginated["limit"] = 1
        mock_search.return_value = MagicMock(model_dump=lambda: paginated)
        
        response = client.post(
            "/tools/search_recipes",
            json={"max_results": 1, "offset": 0},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["recipes"]) == 1
        assert data["offset"] == 0
        assert data["limit"] == 1


def test_search_recipes_endpoint_combined_filters(client, mock_search_results):
    """Test search_recipes endpoint with multiple filters."""
    with patch("src.server.search_recipes") as mock_search:
        mock_search.return_value = MagicMock(model_dump=lambda: mock_search_results)
        
        response = client.post(
            "/tools/search_recipes",
            json={
                "query": "pasta",
                "ingredients": ["tomato"],
                "diet": "vegetarian",
                "exclude_ingredients": ["meat"],
                "max_results": 10,
            },
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "recipes" in data


def test_search_recipes_endpoint_invalid_max_results(client):
    """Test search_recipes endpoint with invalid max_results."""
    # Pydantic validation will catch this and return 422
    response = client.post(
        "/tools/search_recipes",
        json={"max_results": 200},
        headers={"X-API-Key": "test_api_key"},
    )
    
    # 422 is returned by Pydantic validation
    assert response.status_code == 422


def test_search_recipes_endpoint_invalid_diet(client):
    """Test search_recipes endpoint with invalid diet."""
    with patch("src.server.search_recipes") as mock_search:
        mock_search.side_effect = ValueError("Invalid diet filter")
        
        response = client.post(
            "/tools/search_recipes",
            json={"diet": "invalid"},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 400
        assert "error" in response.json()


def test_search_recipes_endpoint_internal_error(client):
    """Test search_recipes endpoint with internal error."""
    with patch("src.server.search_recipes") as mock_search:
        mock_search.side_effect = Exception("Internal error")
        
        response = client.post(
            "/tools/search_recipes",
            json={},
            headers={"X-API-Key": "test_api_key"},
        )
        
        assert response.status_code == 500
        assert "error" in response.json()


def test_search_recipes_endpoint_no_auth(client):
    """Test search_recipes endpoint without authentication."""
    response = client.post(
        "/tools/search_recipes",
        json={},
    )
    
    assert response.status_code == 401


def test_search_recipes_endpoint_invalid_auth(client):
    """Test search_recipes endpoint with invalid API key."""
    response = client.post(
        "/tools/search_recipes",
        json={},
        headers={"X-API-Key": "wrong_key"},
    )
    
    assert response.status_code == 401
