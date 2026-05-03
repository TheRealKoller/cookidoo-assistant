# Python MCP Development Skill

This skill provides workflows and best practices for developing the cookidoo-mcp Python service.

## Quick Commands

### Setup Virtual Environment
```bash
cd cookidoo-mcp
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Run Tests
```bash
cd cookidoo-mcp
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=src/cookidoo_mcp --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_tools/test_recipes.py

# Run specific test function
pytest tests/test_tools/test_recipes.py::test_get_recipe_details_success

# Run in watch mode (requires pytest-watch)
ptw
```

### Code Quality
```bash
cd cookidoo-mcp
source venv/bin/activate

# Format code (modifies files)
ruff format .

# Lint code
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Type checking
mypy src/

# Run all quality checks
ruff format . && ruff check --fix . && mypy src/ && pytest
```

### Run MCP Server
```bash
cd cookidoo-mcp
source venv/bin/activate

# Development mode
python src/cookidoo_mcp/server.py

# With specific log level
LOG_LEVEL=DEBUG python src/cookidoo_mcp/server.py

# Production mode (via Docker)
docker-compose up cookidoo-mcp
```

## Creating New MCP Tools

### Step 1: Define Tool Schema

Create or update tool in `src/cookidoo_mcp/tools/<category>.py`:

```python
from typing import Optional, List
from mcp.types import Tool, TextContent
from cookidoo_api import Cookidoo
from cookidoo_api.types import CookidooRecipeDetails

async def get_recipe_details_tool(
    cookidoo: Cookidoo,
    recipe_id: str
) -> TextContent:
    """Get detailed information about a specific recipe.
    
    Args:
        cookidoo: Authenticated Cookidoo API client
        recipe_id: Recipe ID (e.g., "r59322")
        
    Returns:
        TextContent with recipe details or error message
    """
    try:
        recipe = await cookidoo.get_recipe_details(recipe_id)
        
        # Format response
        response = f"**{recipe.name}**\n\n"
        response += f"Serving Size: {recipe.serving_size}\n"
        response += f"Preparation Time: {recipe.preparation_time} min\n\n"
        
        response += "**Ingredients:**\n"
        for ingredient in recipe.ingredients:
            response += f"- {ingredient.quantity} {ingredient.unit} {ingredient.name}\n"
        
        response += "\n**Instructions:**\n"
        for i, step in enumerate(recipe.instructions, 1):
            response += f"{i}. {step}\n"
        
        return TextContent(type="text", text=response)
        
    except Exception as e:
        return TextContent(
            type="text",
            text=f"Error fetching recipe {recipe_id}: {str(e)}"
        )


# Tool metadata for MCP registration
GET_RECIPE_DETAILS_TOOL = Tool(
    name="get_recipe_details",
    description="Get detailed information about a Cookidoo recipe including ingredients, instructions, and metadata",
    inputSchema={
        "type": "object",
        "properties": {
            "recipe_id": {
                "type": "string",
                "description": "Recipe ID (e.g., 'r59322')"
            }
        },
        "required": ["recipe_id"]
    }
)
```

### Step 2: Register Tool in Server

Update `src/cookidoo_mcp/server.py`:

```python
from cookidoo_mcp.tools.recipes import (
    get_recipe_details_tool,
    GET_RECIPE_DETAILS_TOOL
)

# In server setup
@mcp.list_tools()
async def list_tools() -> list[Tool]:
    return [
        GET_RECIPE_DETAILS_TOOL,
        # ... other tools
    ]

@mcp.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_recipe_details":
        return [await get_recipe_details_tool(cookidoo, **arguments)]
    # ... handle other tools
```

### Step 3: Write Tests

Create `tests/test_tools/test_recipes.py`:

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from cookidoo_api.types import CookidooRecipeDetails, CookidooIngredient
from cookidoo_mcp.tools.recipes import get_recipe_details_tool

@pytest.fixture
def mock_cookidoo():
    """Create mock Cookidoo API client."""
    cookidoo = AsyncMock()
    return cookidoo

@pytest.fixture
def sample_recipe():
    """Sample recipe data for testing."""
    return CookidooRecipeDetails(
        id="r59322",
        name="Spaghetti Carbonara",
        serving_size=4,
        preparation_time=30,
        ingredients=[
            CookidooIngredient(
                name="Spaghetti",
                quantity=400,
                unit="g"
            ),
            CookidooIngredient(
                name="Eggs",
                quantity=4,
                unit="pcs"
            )
        ],
        instructions=[
            "Cook pasta according to package",
            "Mix eggs with cheese",
            "Combine and serve"
        ]
    )

@pytest.mark.asyncio
async def test_get_recipe_details_success(mock_cookidoo, sample_recipe):
    """Test successful recipe details retrieval."""
    mock_cookidoo.get_recipe_details.return_value = sample_recipe
    
    result = await get_recipe_details_tool(mock_cookidoo, "r59322")
    
    assert result.type == "text"
    assert "Spaghetti Carbonara" in result.text
    assert "400 g Spaghetti" in result.text
    assert "4 pcs Eggs" in result.text
    mock_cookidoo.get_recipe_details.assert_called_once_with("r59322")

@pytest.mark.asyncio
async def test_get_recipe_details_not_found(mock_cookidoo):
    """Test recipe not found error handling."""
    mock_cookidoo.get_recipe_details.side_effect = Exception("Recipe not found")
    
    result = await get_recipe_details_tool(mock_cookidoo, "invalid")
    
    assert result.type == "text"
    assert "Error fetching recipe" in result.text
    assert "invalid" in result.text

@pytest.mark.asyncio
async def test_get_recipe_details_api_error(mock_cookidoo):
    """Test API error handling."""
    from cookidoo_api.exceptions import CookidooRequestException
    mock_cookidoo.get_recipe_details.side_effect = CookidooRequestException("API Error")
    
    result = await get_recipe_details_tool(mock_cookidoo, "r59322")
    
    assert result.type == "text"
    assert "Error" in result.text
```

### Step 4: Run Tests

```bash
cd cookidoo-mcp
source venv/bin/activate
pytest tests/test_tools/test_recipes.py -v
```

## Working with cookidoo-api Library

### Authentication

```python
import aiohttp
from cookidoo_api import Cookidoo
from cookidoo_api.types import CookidooConfig
from cookidoo_api.helpers import get_localization_options

async def create_cookidoo_client(email: str, password: str) -> Cookidoo:
    """Create authenticated Cookidoo client.
    
    Args:
        email: Cookidoo account email
        password: Cookidoo account password
        
    Returns:
        Authenticated Cookidoo instance
    """
    async with aiohttp.ClientSession() as session:
        # Get localization (country + language)
        localization = (
            await get_localization_options(country="de", language="de-DE")
        )[0]
        
        # Create client
        cookidoo = Cookidoo(
            session,
            cfg=CookidooConfig(
                email=email,
                password=password,
                localization=localization
            )
        )
        
        # Login
        await cookidoo.login()
        
        return cookidoo
```

### Common Operations

```python
# Recipe Details
recipe = await cookidoo.get_recipe_details("r59322")

# Custom Collections
collections = await cookidoo.get_custom_collections()
new_collection = await cookidoo.add_custom_collection("My Favorites")
await cookidoo.add_recipes_to_custom_collection(new_collection.id, ["r59322"])
await cookidoo.remove_recipe_from_custom_collection(new_collection.id, "r59322")
await cookidoo.remove_custom_collection(new_collection.id)

# Managed Collections
await cookidoo.add_managed_collection("col500401")
managed = await cookidoo.get_managed_collections()
await cookidoo.remove_managed_collection("col500401")

# Calendar/Weekplan
from datetime import date
await cookidoo.add_recipes_to_calendar(date.today(), ["r59322", "r907015"])
recipes = await cookidoo.get_recipes_in_calendar_week(date.today())
await cookidoo.remove_recipe_from_calendar(date.today(), "r59322")

# Shopping List - Ingredients
ingredients = await cookidoo.add_ingredient_items_for_recipes(["r59322"])
all_ingredients = await cookidoo.get_ingredient_items()

# Mark ingredients as owned
from cookidoo_api.types import CookidooIngredientItem
updated = await cookidoo.edit_ingredient_items_ownership([
    CookidooIngredientItem(**{**ing.__dict__, "is_owned": True})
    for ing in ingredients
])

await cookidoo.remove_ingredient_items_for_recipes(["r59322"])

# Shopping List - Additional Items
additional = await cookidoo.add_additional_items(["Milk", "Bread"])
all_additional = await cookidoo.get_additional_items()
await cookidoo.remove_additional_items([item.id for item in additional])

# Shopping List - Recipes
recipes_in_list = await cookidoo.get_shopping_list_recipes()

# Clear entire shopping list
await cookidoo.clear_shopping_list()

# User Info
user_info = await cookidoo.get_user_info()
subscription = await cookidoo.get_active_subscription()
```

### Error Handling

```python
from cookidoo_api.exceptions import (
    CookidooException,
    CookidooAuthException,
    CookidooRequestException,
    CookidooResponseException,
    CookidooParseException
)

try:
    recipe = await cookidoo.get_recipe_details("r59322")
except CookidooAuthException as e:
    # Authentication failed - refresh token or re-login
    await cookidoo.refresh_token()
except CookidooRequestException as e:
    # Network/API request error
    logger.error(f"API request failed: {e}")
except CookidooResponseException as e:
    # Invalid API response
    logger.error(f"Invalid response: {e}")
except CookidooParseException as e:
    # Failed to parse response
    logger.error(f"Parse error: {e}")
except CookidooException as e:
    # Generic Cookidoo error
    logger.error(f"Cookidoo error: {e}")
```

## Best Practices

### 1. Always Use Type Hints
```python
# Good
async def get_recipe(recipe_id: str) -> Optional[CookidooRecipeDetails]:
    pass

# Bad
async def get_recipe(recipe_id):
    pass
```

### 2. Use Proper Exception Handling
```python
# Good
try:
    recipe = await cookidoo.get_recipe_details(recipe_id)
    return TextContent(type="text", text=format_recipe(recipe))
except CookidooException as e:
    logger.error(f"Failed to fetch recipe: {e}")
    return TextContent(type="text", text=f"Error: {str(e)}")

# Bad
recipe = await cookidoo.get_recipe_details(recipe_id)  # Can crash
return format_recipe(recipe)
```

### 3. Use Fixtures for Testing
```python
# conftest.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_cookidoo():
    return AsyncMock()

# test_recipes.py
def test_something(mock_cookidoo):  # Fixture auto-injected
    pass
```

### 4. Keep Tools Focused
```python
# Good - Single responsibility
async def get_recipe_details_tool(...)
async def search_recipes_tool(...)

# Bad - Too many responsibilities
async def recipe_operations_tool(operation: str, ...)
```

### 5. Document Everything
```python
async def get_recipe_details(cookidoo: Cookidoo, recipe_id: str) -> Optional[CookidooRecipeDetails]:
    """Fetch recipe details from Cookidoo API.
    
    Args:
        cookidoo: Authenticated Cookidoo API client
        recipe_id: Recipe ID in format 'r12345'
        
    Returns:
        Recipe details object or None if not found
        
    Raises:
        CookidooAuthException: If authentication fails
        CookidooRequestException: If API request fails
    """
    pass
```

## Troubleshooting

### Virtual Environment Issues
```bash
# Remove old venv
rm -rf venv

# Create fresh venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

### Import Errors
```bash
# Ensure cookidoo-mcp is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or install in editable mode
pip install -e .
```

### Type Checking Errors
```bash
# Check mypy configuration in pyproject.toml
mypy --show-error-codes src/

# Ignore specific errors (use sparingly)
result = some_function()  # type: ignore[return-value]
```

### Test Failures
```bash
# Run with verbose output
pytest -vv

# Run with print statements visible
pytest -s

# Run with debugger on failure
pytest --pdb

# Run only failed tests from last run
pytest --lf
```

### Authentication Issues
```bash
# Verify credentials in .env
cat cookidoo-mcp/.env

# Test authentication manually
python -c "
import asyncio
from cookidoo_api import Cookidoo
# ... test login
"
```

## References

- **cookidoo-api Documentation**: https://github.com/miaucl/cookidoo-api
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **pytest Documentation**: https://docs.pytest.org/
- **ruff Documentation**: https://docs.astral.sh/ruff/
- **mypy Documentation**: https://mypy.readthedocs.io/
