import pytest
from unittest.mock import AsyncMock, MagicMock
from src.tools.recipe_nutrition import get_recipe_nutrition
from src.tools.types import RecipeNutrition
from src.cookidoo_client import cookidoo_connection


@pytest.fixture
def mock_recipe_with_nutrition():
    """Mock recipe with complete nutrition data."""
    mock_nutrition = MagicMock()
    mock_nutrition.type = "energy"
    mock_nutrition.number = 450.0
    mock_nutrition.unittype = "kcal"
    
    mock_protein = MagicMock()
    mock_protein.type = "protein"
    mock_protein.number = 25.5
    mock_protein.unittype = "g"
    
    mock_carbs = MagicMock()
    mock_carbs.type = "carbohydrate"
    mock_carbs.number = 50.0
    mock_carbs.unittype = "g"
    
    mock_fat = MagicMock()
    mock_fat.type = "fat"
    mock_fat.number = 15.0
    mock_fat.unittype = "g"
    
    mock_fiber = MagicMock()
    mock_fiber.type = "fiber"
    mock_fiber.number = 8.0
    mock_fiber.unittype = "g"
    
    mock_sugar = MagicMock()
    mock_sugar.type = "sugar"
    mock_sugar.number = 12.0
    mock_sugar.unittype = "g"
    
    mock_sodium = MagicMock()
    mock_sodium.type = "sodium"
    mock_sodium.number = 500.0
    mock_sodium.unittype = "mg"
    
    mock_saturated = MagicMock()
    mock_saturated.type = "saturated fat"
    mock_saturated.number = 3.5
    mock_saturated.unittype = "g"
    
    mock_recipe_nutrition = MagicMock()
    mock_recipe_nutrition.nutritions = [
        mock_nutrition,
        mock_protein,
        mock_carbs,
        mock_fat,
        mock_fiber,
        mock_sugar,
        mock_sodium,
        mock_saturated,
    ]
    
    mock_nutrition_group = MagicMock()
    mock_nutrition_group.recipe_nutritions = [mock_recipe_nutrition]
    
    recipe = MagicMock()
    recipe.id = "r123456"
    recipe.serving_size = 4
    recipe.nutrition_groups = [mock_nutrition_group]
    
    return recipe


@pytest.fixture
def mock_recipe_with_kj_energy():
    """Mock recipe with energy in kJ instead of kcal."""
    mock_nutrition = MagicMock()
    mock_nutrition.type = "energy"
    mock_nutrition.number = 1884.0  # 450 kcal * 4.184
    mock_nutrition.unittype = "kJ"
    
    mock_recipe_nutrition = MagicMock()
    mock_recipe_nutrition.nutritions = [mock_nutrition]
    
    mock_nutrition_group = MagicMock()
    mock_nutrition_group.recipe_nutritions = [mock_recipe_nutrition]
    
    recipe = MagicMock()
    recipe.id = "r123456"
    recipe.serving_size = 4
    recipe.nutrition_groups = [mock_nutrition_group]
    
    return recipe


@pytest.fixture
def mock_recipe_without_nutrition():
    """Mock recipe without nutrition data."""
    recipe = MagicMock()
    recipe.id = "r999999"
    recipe.serving_size = 2
    recipe.nutrition_groups = []
    
    return recipe


@pytest.mark.asyncio
async def test_get_recipe_nutrition_success(mock_recipe_with_nutrition):
    """Test successful nutrition retrieval."""
    mock_client = AsyncMock()
    mock_client.get_recipe_details = AsyncMock(return_value=mock_recipe_with_nutrition)
    cookidoo_connection._client = mock_client
    
    result = await get_recipe_nutrition("r123456")
    
    assert isinstance(result, RecipeNutrition)
    assert result.recipe_id == "r123456"
    assert result.serving_size == 4
    assert result.calories == 450.0
    assert result.protein == 25.5
    assert result.carbohydrates == 50.0
    assert result.fat == 15.0
    assert result.fiber == 8.0
    assert result.sugar == 12.0
    assert result.sodium == 500.0
    assert result.saturated_fat == 3.5
    assert len(result.nutrients) == 8


@pytest.mark.asyncio
async def test_get_recipe_nutrition_kj_conversion(mock_recipe_with_kj_energy):
    """Test conversion of kJ to kcal."""
    mock_client = AsyncMock()
    mock_client.get_recipe_details = AsyncMock(return_value=mock_recipe_with_kj_energy)
    cookidoo_connection._client = mock_client
    
    result = await get_recipe_nutrition("r123456")
    
    assert result.calories is not None
    # 1884 kJ / 4.184 ≈ 450 kcal
    assert abs(result.calories - 450.0) < 1.0


@pytest.mark.asyncio
async def test_get_recipe_nutrition_without_data(mock_recipe_without_nutrition):
    """Test recipe without nutrition data."""
    mock_client = AsyncMock()
    mock_client.get_recipe_details = AsyncMock(return_value=mock_recipe_without_nutrition)
    cookidoo_connection._client = mock_client
    
    result = await get_recipe_nutrition("r999999")
    
    assert isinstance(result, RecipeNutrition)
    assert result.recipe_id == "r999999"
    assert result.serving_size == 2
    assert result.calories is None
    assert result.protein is None
    assert result.carbohydrates is None
    assert result.fat is None
    assert len(result.nutrients) == 0


@pytest.mark.asyncio
async def test_get_recipe_nutrition_missing_recipe_id():
    """Test validation of recipe_id."""
    with pytest.raises(ValueError, match="recipe_id is required"):
        await get_recipe_nutrition("")


@pytest.mark.asyncio
async def test_get_recipe_nutrition_api_error():
    """Test handling of API errors."""
    mock_client = AsyncMock()
    mock_client.get_recipe_details = AsyncMock(side_effect=Exception("API Error"))
    cookidoo_connection._client = mock_client
    
    with pytest.raises(ValueError, match="Failed to get recipe nutrition"):
        await get_recipe_nutrition("invalid_id")


@pytest.mark.asyncio
async def test_get_recipe_nutrition_partial_data():
    """Test recipe with partial nutrition data."""
    # Only energy and protein
    mock_energy = MagicMock()
    mock_energy.type = "energy"
    mock_energy.number = 300.0
    mock_energy.unittype = "kcal"
    
    mock_protein = MagicMock()
    mock_protein.type = "protein"
    mock_protein.number = 20.0
    mock_protein.unittype = "g"
    
    mock_recipe_nutrition = MagicMock()
    mock_recipe_nutrition.nutritions = [mock_energy, mock_protein]
    
    mock_nutrition_group = MagicMock()
    mock_nutrition_group.recipe_nutritions = [mock_recipe_nutrition]
    
    recipe = MagicMock()
    recipe.id = "r555555"
    recipe.serving_size = 2
    recipe.nutrition_groups = [mock_nutrition_group]
    
    mock_client = AsyncMock()
    mock_client.get_recipe_details = AsyncMock(return_value=recipe)
    cookidoo_connection._client = mock_client
    
    result = await get_recipe_nutrition("r555555")
    
    assert result.calories == 300.0
    assert result.protein == 20.0
    assert result.carbohydrates is None
    assert result.fat is None
    assert len(result.nutrients) == 2


@pytest.mark.asyncio
async def test_get_recipe_nutrition_sodium_gram_conversion():
    """Test conversion of sodium from g to mg."""
    mock_sodium = MagicMock()
    mock_sodium.type = "sodium"
    mock_sodium.number = 1.5  # grams
    mock_sodium.unittype = "g"
    
    mock_recipe_nutrition = MagicMock()
    mock_recipe_nutrition.nutritions = [mock_sodium]
    
    mock_nutrition_group = MagicMock()
    mock_nutrition_group.recipe_nutritions = [mock_recipe_nutrition]
    
    recipe = MagicMock()
    recipe.id = "r777777"
    recipe.serving_size = 1
    recipe.nutrition_groups = [mock_nutrition_group]
    
    mock_client = AsyncMock()
    mock_client.get_recipe_details = AsyncMock(return_value=recipe)
    cookidoo_connection._client = mock_client
    
    result = await get_recipe_nutrition("r777777")
    
    # 1.5g = 1500mg
    assert result.sodium == 1500.0


@pytest.mark.asyncio
async def test_get_recipe_nutrition_default_serving_size():
    """Test default serving size when not specified."""
    mock_nutrition_group = MagicMock()
    mock_nutrition_group.recipe_nutritions = []
    
    recipe = MagicMock()
    recipe.id = "r888888"
    recipe.serving_size = None  # No serving size
    recipe.nutrition_groups = [mock_nutrition_group]
    
    mock_client = AsyncMock()
    mock_client.get_recipe_details = AsyncMock(return_value=recipe)
    cookidoo_connection._client = mock_client
    
    result = await get_recipe_nutrition("r888888")
    
    # Should default to 1
    assert result.serving_size == 1
