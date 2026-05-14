import pytest
from unittest.mock import AsyncMock, MagicMock
from src.tools.search_recipes import search_recipes, _matches_filters, _matches_diet
from src.tools.types import SearchRecipesResponse, SearchRecipeResult
from src.cookidoo_client import cookidoo_connection
from cookidoo_api.types import CookidooIngredient


@pytest.fixture
def mock_collection():
    """Mock collection with recipes."""
    collection = MagicMock()
    collection.chapters = [
        MagicMock(
            recipes=[
                MagicMock(id="r001", name="Pasta Carbonara", total_time=1800),
                MagicMock(id="r002", name="Vegetable Soup", total_time=2400),
            ]
        )
    ]
    return collection


@pytest.fixture
def mock_recipe_details_meat():
    """Mock recipe with meat."""
    from cookidoo_api.types import CookidooIngredient
    
    recipe = MagicMock()
    recipe.id = "r001"
    recipe.name = "Pasta Carbonara"
    recipe.description = "Classic Italian pasta with bacon"
    recipe.image = "http://example.com/image1.jpg"
    recipe.total_time = 1800
    recipe.difficulty = "medium"
    recipe.ingredients = [
        CookidooIngredient(id="1", name="Pasta", description="400 g"),
        CookidooIngredient(id="2", name="Bacon", description="200 g"),
        CookidooIngredient(id="3", name="Eggs", description="4 pcs"),
        CookidooIngredient(id="4", name="Parmesan", description="100 g"),
    ]
    return recipe


@pytest.fixture
def mock_recipe_details_vegan():
    """Mock vegan recipe."""
    from cookidoo_api.types import CookidooIngredient
    
    recipe = MagicMock()
    recipe.id = "r002"
    recipe.name = "Vegetable Soup"
    recipe.description = "Healthy vegetable soup"
    recipe.image = None
    recipe.total_time = 2400
    recipe.difficulty = "easy"
    recipe.ingredients = [
        CookidooIngredient(id="5", name="Carrots", description="300 g"),
        CookidooIngredient(id="6", name="Tomatoes", description="500 g"),
        CookidooIngredient(id="7", name="Onions", description="2 pcs"),
    ]
    return recipe


@pytest.mark.asyncio
async def test_search_recipes_basic(mock_collection, mock_recipe_details_meat, mock_recipe_details_vegan):
    """Test basic search without filters."""
    mock_client = AsyncMock()
    mock_client.get_managed_collections = AsyncMock(return_value=[mock_collection])
    mock_client.get_recipe_details = AsyncMock(
        side_effect=[mock_recipe_details_meat, mock_recipe_details_vegan]
    )
    cookidoo_connection._client = mock_client
    
    result = await search_recipes()
    
    assert isinstance(result, SearchRecipesResponse)
    assert result.total == 2
    assert len(result.recipes) == 2
    assert result.recipes[0].title == "Pasta Carbonara"
    assert result.recipes[1].title == "Vegetable Soup"


@pytest.mark.asyncio
async def test_search_recipes_with_query(mock_collection, mock_recipe_details_meat, mock_recipe_details_vegan):
    """Test search with text query."""
    mock_client = AsyncMock()
    mock_client.get_managed_collections = AsyncMock(return_value=[mock_collection])
    mock_client.get_recipe_details = AsyncMock(
        side_effect=[mock_recipe_details_meat, mock_recipe_details_vegan]
    )
    cookidoo_connection._client = mock_client
    
    result = await search_recipes(query="pasta")
    
    assert result.total == 1
    assert len(result.recipes) == 1
    assert result.recipes[0].title == "Pasta Carbonara"


@pytest.mark.asyncio
async def test_search_recipes_with_ingredients(mock_collection, mock_recipe_details_meat, mock_recipe_details_vegan):
    """Test search with ingredient filter."""
    mock_client = AsyncMock()
    mock_client.get_managed_collections = AsyncMock(return_value=[mock_collection])
    mock_client.get_recipe_details = AsyncMock(
        side_effect=[mock_recipe_details_meat, mock_recipe_details_vegan]
    )
    cookidoo_connection._client = mock_client
    
    result = await search_recipes(ingredients=["bacon"])
    
    assert result.total == 1
    assert len(result.recipes) == 1
    assert result.recipes[0].title == "Pasta Carbonara"


@pytest.mark.asyncio
async def test_search_recipes_exclude_ingredients(mock_collection, mock_recipe_details_meat, mock_recipe_details_vegan):
    """Test search with ingredient exclusion."""
    mock_client = AsyncMock()
    mock_client.get_managed_collections = AsyncMock(return_value=[mock_collection])
    mock_client.get_recipe_details = AsyncMock(
        side_effect=[mock_recipe_details_meat, mock_recipe_details_vegan]
    )
    cookidoo_connection._client = mock_client
    
    result = await search_recipes(exclude_ingredients=["bacon"])
    
    assert result.total == 1
    assert len(result.recipes) == 1
    assert result.recipes[0].title == "Vegetable Soup"


@pytest.mark.asyncio
async def test_search_recipes_diet_vegan(mock_collection, mock_recipe_details_meat, mock_recipe_details_vegan):
    """Test search with vegan diet filter."""
    mock_client = AsyncMock()
    mock_client.get_managed_collections = AsyncMock(return_value=[mock_collection])
    mock_client.get_recipe_details = AsyncMock(
        side_effect=[mock_recipe_details_meat, mock_recipe_details_vegan]
    )
    cookidoo_connection._client = mock_client
    
    result = await search_recipes(diet="vegan")
    
    assert result.total == 1
    assert len(result.recipes) == 1
    assert result.recipes[0].title == "Vegetable Soup"


@pytest.mark.asyncio
async def test_search_recipes_diet_vegetarian(mock_collection, mock_recipe_details_meat, mock_recipe_details_vegan):
    """Test search with vegetarian diet filter."""
    mock_client = AsyncMock()
    mock_client.get_managed_collections = AsyncMock(return_value=[mock_collection])
    mock_client.get_recipe_details = AsyncMock(
        side_effect=[mock_recipe_details_meat, mock_recipe_details_vegan]
    )
    cookidoo_connection._client = mock_client
    
    result = await search_recipes(diet="vegetarian")
    
    # Only vegan recipe should match (no meat/fish)
    assert result.total == 1
    assert result.recipes[0].title == "Vegetable Soup"


@pytest.mark.asyncio
async def test_search_recipes_pagination(mock_collection, mock_recipe_details_meat, mock_recipe_details_vegan):
    """Test pagination."""
    mock_client = AsyncMock()
    mock_client.get_managed_collections = AsyncMock(return_value=[mock_collection])
    mock_client.get_recipe_details = AsyncMock(
        side_effect=[mock_recipe_details_meat, mock_recipe_details_vegan]
    )
    cookidoo_connection._client = mock_client
    
    result = await search_recipes(max_results=1, offset=0)
    
    assert result.total == 2
    assert len(result.recipes) == 1
    assert result.offset == 0
    assert result.limit == 1


@pytest.mark.asyncio
async def test_search_recipes_pagination_offset(mock_collection, mock_recipe_details_meat, mock_recipe_details_vegan):
    """Test pagination with offset."""
    mock_client = AsyncMock()
    mock_client.get_managed_collections = AsyncMock(return_value=[mock_collection])
    mock_client.get_recipe_details = AsyncMock(
        side_effect=[mock_recipe_details_meat, mock_recipe_details_vegan]
    )
    cookidoo_connection._client = mock_client
    
    result = await search_recipes(max_results=1, offset=1)
    
    assert result.total == 2
    assert len(result.recipes) == 1
    assert result.recipes[0].title == "Vegetable Soup"


@pytest.mark.asyncio
async def test_search_recipes_invalid_max_results():
    """Test validation of max_results."""
    with pytest.raises(ValueError, match="max_results must be between 1 and 100"):
        await search_recipes(max_results=0)
    
    with pytest.raises(ValueError, match="max_results must be between 1 and 100"):
        await search_recipes(max_results=101)


@pytest.mark.asyncio
async def test_search_recipes_invalid_offset():
    """Test validation of offset."""
    with pytest.raises(ValueError, match="offset must be non-negative"):
        await search_recipes(offset=-1)


@pytest.mark.asyncio
async def test_search_recipes_invalid_diet():
    """Test validation of diet parameter."""
    with pytest.raises(ValueError, match="Invalid diet filter"):
        await search_recipes(diet="invalid_diet")


@pytest.mark.asyncio
async def test_search_recipes_empty_collections():
    """Test search with no collections."""
    mock_client = AsyncMock()
    mock_client.get_managed_collections = AsyncMock(return_value=[])
    cookidoo_connection._client = mock_client
    
    result = await search_recipes()
    
    assert result.total == 0
    assert len(result.recipes) == 0


@pytest.mark.asyncio
async def test_search_recipes_api_error_handling(mock_collection):
    """Test handling of API errors."""
    mock_client = AsyncMock()
    mock_client.get_managed_collections = AsyncMock(return_value=[mock_collection])
    mock_client.get_recipe_details = AsyncMock(side_effect=Exception("API Error"))
    cookidoo_connection._client = mock_client
    
    # Should not raise, just skip failed recipes
    result = await search_recipes()
    
    assert result.total == 0
    assert len(result.recipes) == 0


def test_matches_diet_vegan():
    """Test vegan diet matching."""
    # Vegan recipe
    assert _matches_diet(["tomatoes", "carrots", "onions"], "vegan")
    
    # Not vegan (has meat)
    assert not _matches_diet(["chicken", "tomatoes"], "vegan")
    
    # Not vegan (has dairy)
    assert not _matches_diet(["milk", "tomatoes"], "vegan")
    
    # Not vegan (has eggs)
    assert not _matches_diet(["eggs", "flour"], "vegan")


def test_matches_diet_vegetarian():
    """Test vegetarian diet matching."""
    # Vegetarian (no meat/fish)
    assert _matches_diet(["eggs", "cheese", "tomatoes"], "vegetarian")
    
    # Not vegetarian (has meat)
    assert not _matches_diet(["beef", "potatoes"], "vegetarian")
    
    # Not vegetarian (has fish)
    assert not _matches_diet(["salmon", "rice"], "vegetarian")


def test_matches_diet_pescetarian():
    """Test pescetarian diet matching."""
    # Pescetarian (fish ok, no meat)
    assert _matches_diet(["salmon", "vegetables"], "pescetarian")
    
    # Not pescetarian (has meat)
    assert not _matches_diet(["chicken", "fish"], "pescetarian")


def test_matches_diet_omnivor():
    """Test omnivore diet (allows everything)."""
    assert _matches_diet(["chicken", "beef", "pork"], "omnivor")
    assert _matches_diet(["vegetables"], "omnivor")


def test_matches_filters_query():
    """Test query filtering."""
    recipe = MagicMock()
    recipe.name = "Pasta Carbonara"
    recipe.description = "Italian classic"
    recipe.ingredients = []
    
    # Match in title
    assert _matches_filters(recipe, "pasta", [], [], None)
    
    # Match in description
    assert _matches_filters(recipe, "italian", [], [], None)
    
    # No match
    assert not _matches_filters(recipe, "pizza", [], [], None)


def test_matches_filters_ingredients():
    """Test ingredient filtering."""
    from cookidoo_api.types import CookidooIngredient
    
    recipe = MagicMock()
    recipe.name = "Test Recipe"
    recipe.description = None
    recipe.ingredients = [
        CookidooIngredient(id="1", name="Tomatoes", description="500 g"),
        CookidooIngredient(id="2", name="Cheese", description="100 g"),
    ]
    
    # Has required ingredient
    assert _matches_filters(recipe, None, ["tomatoes"], [], None)
    
    # Missing required ingredient
    assert not _matches_filters(recipe, None, ["bacon"], [], None)


def test_matches_filters_exclude_ingredients():
    """Test ingredient exclusion."""
    from cookidoo_api.types import CookidooIngredient
    
    recipe = MagicMock()
    recipe.name = "Test Recipe"
    recipe.description = None
    recipe.ingredients = [
        CookidooIngredient(id="1", name="Tomatoes", description="500 g"),
        CookidooIngredient(id="2", name="Cheese", description="100 g"),
    ]
    
    # Does not have excluded ingredient
    assert _matches_filters(recipe, None, [], ["bacon"], None)
    
    # Has excluded ingredient
    assert not _matches_filters(recipe, None, [], ["cheese"], None)
