# Cookidoo Assistant - Agent Instructions

## Repository Structure

**Monorepo** with 4 services using npm workspaces:
- `cookidoo-mcp/` - Python 3.12+ FastAPI server (port 3000)
- `cookidoo-assistant-shared/` - TypeScript shared library
- `cookidoo-assistant-mcp/` - TypeScript MCP server (port 3001) 
- `cookidoo-assistant-api/` - TypeScript REST API (port 3002)

## Critical: Python Service is NOT Node.js

**cookidoo-mcp** is a Python service, despite being in an npm workspace:
- Run tests: `cd cookidoo-mcp && pytest`
- Format: `ruff format .`
- Lint: `ruff check .`
- Type check: `mypy .`
- The `package.json` in cookidoo-mcp has placeholder scripts - ignore them

Python dependencies are in `requirements.txt`, not package.json.

## Testing Requirements

**You MUST run tests after implementation.** This is non-negotiable:

```bash
# Python service
cd cookidoo-mcp && pytest

# All TypeScript services
npm test
```

All tests must pass before creating a PR.

## Branch & PR Workflow

1. **Branch naming:** `<issue-number>-short-description`
   - Example: `24-search-recipes-mcp-tool`
   - NOT `feature/24-...` or other prefixes

2. **Create branch from main:**
   ```bash
   git checkout main
   git pull
   git checkout -b 24-short-description
   ```

3. **Commit format:** Use Conventional Commits
   - `feat(mcp): add search_recipes tool`
   - `fix(shared): resolve db connection issue`
   - `test(mcp): add unit tests for filters`
   
   Scopes: `mcp`, `shared`, `assistant-mcp`, `api`

4. **PR title format:** `[service] Short description`
   - Example: `[cookidoo-mcp] Implement search_recipes MCP tool`

5. **PR body must include:**
   - `Resolves #<issue-number>`
   - Summary of changes
   - Test status confirmation

## cookidoo-mcp Python Service

### Structure
```
cookidoo-mcp/
├── src/
│   ├── server.py              # FastAPI app, tool endpoints
│   ├── cookidoo_client.py     # Cookidoo API connection singleton
│   ├── middleware.py          # API key auth
│   └── tools/
│       ├── types.py           # Pydantic models
│       └── {tool_name}.py     # Tool implementations
├── tests/
│   ├── conftest.py            # Shared fixtures
│   └── test_{tool_name}.py    # Tool tests
└── docs/tools/                # Tool documentation
```

### Adding a New MCP Tool

1. **Add types** to `src/tools/types.py` (Pydantic models)
2. **Implement tool** in `src/tools/{tool_name}.py`
3. **Register endpoint** in `src/server.py`:
   ```python
   @app.post("/tools/{tool_name}")
   async def handle_{tool_name}(request: RequestModel):
       try:
           result = await tool_function(...)
           return JSONResponse(result.model_dump())
       except ValueError as e:
           return JSONResponse({"error": str(e)}, status_code=400)
       except Exception as e:
           logger.error(f"Error: {e}", exc_info=True)
           return JSONResponse({"error": "Internal error"}, status_code=500)
   ```
4. **Write tests** in `tests/test_{tool_name}.py`
5. **Document** in `docs/tools/{tool_name}.md`

### Test Fixtures

Use existing fixtures from `tests/conftest.py`:
- `mock_env` - Sets test environment variables
- `mock_cookidoo` - Mocks Cookidoo API client
- `client` - FastAPI TestClient

Mock `cookidoo_connection._client` directly:
```python
from src.cookidoo_client import cookidoo_connection

mock_client = AsyncMock()
cookidoo_connection._client = mock_client
```

### cookidoo-api Library

Uses `cookidoo-api` (miaucl/cookidoo-api) which does NOT have native search:
- Available: `get_recipe_details`, `get_managed_collections`, `get_custom_collections`
- For search: use collections + client-side filtering
- Ingredient structure: `CookidooIngredient(id, name, description)` - NOT `quantity`/`unit`

## Issue Labels

Always add service label when working on issues:
- `service:cookidoo-mcp`
- `service:shared`
- `service:assistant-mcp`
- `service:api`

## CI/CD

- **CI runs on:** All pushes to main, all PRs
- **Order:** lint → format:check → type-check → test → build
- **Python tests:** Separate job with pytest + coverage
- **Coverage:** Uploaded to Codecov

Tests MUST pass in CI before merge.

## Environment Variables

cookidoo-mcp requires:
- `COOKIDOO_EMAIL` - Cookidoo account email
- `COOKIDOO_PASSWORD` - Cookidoo account password  
- `MCP_API_KEY` - API key for authentication
- `LOG_LEVEL` - Optional (default: INFO)

Copy `.env.example` → `.env` in service directories.

## Common Pitfalls

1. **Don't use npm scripts for cookidoo-mcp Python code** - use Python tools directly
2. **CookidooIngredient has no `quantity`/`unit`** - use `description` field instead
3. **Always mock `cookidoo_connection._client`** - don't try to instantiate real client in tests
4. **Run tests in service directory** - `cd cookidoo-mcp && pytest`, not from root
5. **Branch names: no prefixes** - just `24-description`, not `feature/24-description`
