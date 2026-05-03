---
name: python-mcp-development
description: Python MCP development workflows and best practices for the cookidoo-mcp service
---

# Python MCP Development

Python MCP-Entwicklung für cookidoo-mcp Service.

## Quick Commands

### Setup
```bash
cd cookidoo-mcp
python3 -m venv venv
source venv/bin/activate           # Linux/Mac
pip install -r requirements.txt -r requirements-dev.txt
```

### Tests
```bash
cd cookidoo-mcp && source venv/bin/activate

pytest                             # Alle
pytest --cov=src/cookidoo_mcp --cov-report=html --cov-report=term
pytest tests/test_tools/test_recipes.py
pytest tests/test_tools/test_recipes.py::test_get_recipe_details_success
ptw                                # Watch mode
```

### Quality
```bash
cd cookidoo-mcp && source venv/bin/activate

ruff format .                      # Format
ruff check .                       # Lint
ruff check --fix .                 # Auto-fix
mypy src/                          # Type check
ruff format . && ruff check --fix . && mypy src/ && pytest
```

### Run
```bash
cd cookidoo-mcp && source venv/bin/activate
python src/cookidoo_mcp/server.py
LOG_LEVEL=DEBUG python src/cookidoo_mcp/server.py
```

## MCP Tool erstellen

### 1. Tool-Schema (`src/cookidoo_mcp/tools/<category>.py`)
```python
from typing import Optional
from mcp.types import Tool, TextContent
from cookidoo_api import Cookidoo

async def get_recipe_details_tool(
    cookidoo: Cookidoo,
    recipe_id: str
) -> TextContent:
    """Get detailed recipe information.
    
    Args:
        cookidoo: Authenticated Cookidoo API client
        recipe_id: Recipe ID (e.g., "r59322")
        
    Returns:
        TextContent with recipe details or error
    """
    try:
        recipe = await cookidoo.get_recipe_details(recipe_id)
        
        response = f"**{recipe.name}**\n\n"
        response += f"Serving Size: {recipe.serving_size}\n"
        response += f"Prep Time: {recipe.preparation_time} min\n\n"
        
        response += "**Ingredients:**\n"
        for ing in recipe.ingredients:
            response += f"- {ing.quantity} {ing.unit} {ing.name}\n"
        
        response += "\n**Instructions:**\n"
        for i, step in enumerate(recipe.instructions, 1):
            response += f"{i}. {step}\n"
        
        return TextContent(type="text", text=response)
    except Exception as e:
        return TextContent(type="text", text=f"Error: {str(e)}")


GET_RECIPE_DETAILS_TOOL = Tool(
    name="get_recipe_details",
    description="Get recipe details including ingredients and instructions",
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

### 2. Server-Integration (`src/cookidoo_mcp/server.py`)
```python
from cookidoo_mcp.tools.recipes import (
    get_recipe_details_tool,
    GET_RECIPE_DETAILS_TOOL
)

@mcp.list_tools()
async def list_tools() -> list[Tool]:
    return [GET_RECIPE_DETAILS_TOOL, ...]

@mcp.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_recipe_details":
        return [await get_recipe_details_tool(cookidoo, **arguments)]
```

### 3. Tests (`tests/test_tools/test_recipes.py`)
```python
import pytest
from unittest.mock import AsyncMock
from cookidoo_mcp.tools.recipes import get_recipe_details_tool

@pytest.fixture
def mock_cookidoo():
    return AsyncMock()

@pytest.fixture
def sample_recipe():
    return CookidooRecipeDetails(
        id="r59322",
        name="Spaghetti Carbonara",
        serving_size=4,
        preparation_time=30,
        ingredients=[...],
        instructions=[...]
    )

@pytest.mark.asyncio
async def test_get_recipe_details_success(mock_cookidoo, sample_recipe):
    mock_cookidoo.get_recipe_details.return_value = sample_recipe
    
    result = await get_recipe_details_tool(mock_cookidoo, "r59322")
    
    assert result.type == "text"
    assert "Spaghetti Carbonara" in result.text
    mock_cookidoo.get_recipe_details.assert_called_once_with("r59322")

@pytest.mark.asyncio
async def test_get_recipe_details_not_found(mock_cookidoo):
    mock_cookidoo.get_recipe_details.side_effect = Exception("Not found")
    
    result = await get_recipe_details_tool(mock_cookidoo, "invalid")
    
    assert "Error" in result.text
```

## cookidoo-api Library

### Authentication
```python
from cookidoo_api import Cookidoo
from cookidoo_api.types import CookidooConfig
from cookidoo_api.helpers import get_localization_options

async def create_client(email: str, password: str) -> Cookidoo:
    async with aiohttp.ClientSession() as session:
        localization = (
            await get_localization_options(country="de", language="de-DE")
        )[0]
        
        cookidoo = Cookidoo(
            session,
            cfg=CookidooConfig(
                email=email,
                password=password,
                localization=localization
            )
        )
        await cookidoo.login()
        return cookidoo
```

### Common Operations
```python
# Recipes
recipe = await cookidoo.get_recipe_details("r59322")

# Collections
collections = await cookidoo.get_custom_collections()
new = await cookidoo.add_custom_collection("Favorites")
await cookidoo.add_recipes_to_custom_collection(new.id, ["r59322"])

# Calendar
from datetime import date
await cookidoo.add_recipes_to_calendar(date.today(), ["r59322"])
recipes = await cookidoo.get_recipes_in_calendar_week(date.today())

# Shopping List
ingredients = await cookidoo.add_ingredient_items_for_recipes(["r59322"])
all_items = await cookidoo.get_ingredient_items()
additional = await cookidoo.add_additional_items(["Milk", "Bread"])
await cookidoo.clear_shopping_list()
```

### Error Handling
```python
from cookidoo_api.exceptions import (
    CookidooAuthException,
    CookidooRequestException,
    CookidooException
)

try:
    recipe = await cookidoo.get_recipe_details("r59322")
except CookidooAuthException:
    await cookidoo.refresh_token()
except CookidooRequestException as e:
    logger.error(f"API error: {e}")
except CookidooException as e:
    logger.error(f"General error: {e}")
```

## Best Practices

1. **Type Hints**: Immer verwenden
```python
# Good
async def get_recipe(recipe_id: str) -> Optional[CookidooRecipeDetails]:
    pass

# Bad
async def get_recipe(recipe_id):
    pass
```

2. **Exception Handling**: Alle API-Calls absichern
3. **Fixtures**: Wiederverwendbare Test-Fixtures in `conftest.py`
4. **Fokus**: Ein Tool = eine Aufgabe
5. **Docs**: Docstrings für alle Public Functions

## Troubleshooting

```bash
# Venv Probleme
rm -rf venv
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# Import Errors
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Type Errors
mypy --show-error-codes src/

# Test Failures
pytest -vv                         # Verbose
pytest -s                          # Mit prints
pytest --pdb                       # Debugger bei Fehler
```
