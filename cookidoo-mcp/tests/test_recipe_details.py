import pytest
from unittest.mock import AsyncMock, MagicMock
from src.tools.recipe_details import get_recipe_details
from src.tools.types import RecipeDetails
from src.cookidoo_client import cookidoo_connection


@pytest.fixture
def mock_recipe_response():
    mock = MagicMock()
    mock.difficulty = "easy"
    mock.notes = [{"text": "Step 1", "duration": 120}, {"text": "Step 2"}]
    mock.categories = ["main-dish", "vegetarian"]
    mock.collections = [{"name": "Quick Meals"}]
    mock.utensils = [{"name": "Thermomix"}, {"name": "Spatula"}]
    mock.serving_size = 4
    mock.active_time = 600
    mock.total_time = 1800
    mock.nutrition_groups = [
        {"ingredients": [
            {"name": "Tomatoes", "quantity": 500, "unit": "g"},
            {"name": "Onions", "quantity": 2, "unit": "pcs"}
        ]}
    ]
    mock.get = lambda k, d=None: {"title": "Test Recipe", "description": "Test desc", "image_url": "http://img.com"}.get(k, d)
    return mock


@pytest.mark.asyncio
async def test_get_recipe_details_success(mock_recipe_response):
    mock_client = AsyncMock()
    mock_client.get_recipe_details = AsyncMock(return_value=mock_recipe_response)
    cookidoo_connection._client = mock_client
    
    result = await get_recipe_details("r123456")
    
    assert isinstance(result, RecipeDetails)
    assert result.id == "r123456"
    assert result.title == "Test Recipe"
    assert result.description == "Test desc"
    assert result.difficulty == "easy"
    assert result.servings == 4
    assert result.cooking_time == 30
    assert result.prep_time == 10
    assert len(result.ingredients) == 2
    assert result.ingredients[0].name == "Tomatoes"
    assert result.ingredients[0].quantity == 500
    assert len(result.instructions) == 2
    assert result.instructions[0].step_number == 1
    assert len(result.equipment) == 2
    assert "vegetarian" in result.tags


@pytest.mark.asyncio
async def test_get_recipe_details_missing_recipe_id():
    with pytest.raises(ValueError, match="recipe_id is required"):
        await get_recipe_details("")


@pytest.mark.asyncio
async def test_get_recipe_details_api_error():
    mock_client = AsyncMock()
    mock_client.get_recipe_details = AsyncMock(side_effect=Exception("API Error"))
    cookidoo_connection._client = mock_client
    
    with pytest.raises(ValueError, match="Recipe not found or API error"):
        await get_recipe_details("invalid_id")


@pytest.mark.asyncio
async def test_get_recipe_details_minimal_data():
    minimal = MagicMock(
        difficulty=None,
        notes=None,
        categories=None,
        collections=None,
        utensils=None,
        serving_size=None,
        active_time=None,
        total_time=None,
        nutrition_groups=[]
    )
    minimal.get = lambda k, d=None: d
    
    mock_client = AsyncMock()
    mock_client.get_recipe_details = AsyncMock(return_value=minimal)
    cookidoo_connection._client = mock_client
    
    result = await get_recipe_details("r999")
    
    assert result.id == "r999"
    assert result.title == "Unknown"
    assert len(result.ingredients) == 0
    assert len(result.instructions) == 0
