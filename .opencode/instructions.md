# Cookidoo Assistant - Instructions

## Projekt-Übersicht

Dieses Monorepo enthält die komplette Cookidoo Assistant Platform - ein AI-powered Meal Planning System basierend auf Cookidoo Rezepten mit MCP Servern und REST API.

### Repository

- **GitHub Repository**: https://github.com/TheRealKoller/cookidoo-assistant
- **Project Board**: https://github.com/users/TheRealKoller/projects/5

## ⚠️ CRITICAL: Issue Implementation Workflow

**BEFORE implementing ANY GitHub issue, you MUST:**

1. **Load the workflow skill**: `github-workflow`
2. **Follow steps 1-9 EXACTLY** as documented in the skill
3. **NEVER commit directly to `main`** (except for approved exceptions below)
4. **ALWAYS create a feature branch**: `ISSUE_NUMBER-short-description`
5. **ALWAYS create a Pull Request** linking to the issue
6. **ALWAYS run tests** before creating PR
7. **ALWAYS update issue status** on Project Board

### Approved Exceptions for Direct `main` Commits

Direct commits to `main` are ONLY allowed for:
- **Critical hotfixes** requiring immediate deployment
- **CI/CD configuration changes** (.github/workflows/*)
- **Documentation-only changes** (*.md files) with user approval
- **Dependency updates** with passing CI

**ALL OTHER CHANGES MUST GO THROUGH PR WORKFLOW**

### Quick Reference

```bash
# 1. Load skill first
skill load github-workflow

# 2. Create feature branch
git checkout -b ISSUE_NUMBER-description

# 3. Implement, test, commit

# 4. Push and create PR
git push -u origin ISSUE_NUMBER-description
gh pr create --base main --head ISSUE_NUMBER-description
```

**Violation of this workflow is a critical error and must be corrected immediately.**

### Monorepo-Struktur

Dieses Repository ist als **Monorepo** organisiert und enthält 4 Services:

```
cookidoo-assistant/
├── cookidoo-mcp/              # MCP Server für Cookidoo API (Port 3000)
├── cookidoo-assistant-shared/ # Shared Library (Business Logic & Data Access)
├── cookidoo-assistant-mcp/    # MCP Server für User Data (Port 3001)
└── cookidoo-assistant-api/    # REST API für UI (Port 3002)
```

#### Service-Beschreibungen

1. **cookidoo-mcp** (`service:cookidoo-mcp`)
   - **Language:** Python 3.11+
   - **Purpose:** MCP Server für Cookidoo API Integration
   - **Library:** `cookidoo-api==0.17.0` (miaucl/cookidoo-api)
   - **Tools:** Recipe Details, Collections (Custom/Managed), Custom Recipes, Calendar/Weekplan, Shopping List (Ingredients + Additional Items)
   - **Port:** 3000
   - **Features:** OAuth authentication, async/await, comprehensive CRUD operations

2. **cookidoo-assistant-shared** (`service:shared`)
   - Shared Library für alle Services
   - Database Models, Repositories, Business Logic
   - Als npm workspace package von anderen Services genutzt

3. **cookidoo-assistant-mcp** (`service:assistant-mcp`)
   - MCP Server für User Data Management
   - Tools: User Profiles, Dietary Preferences, Allergies, Health Data, Recipe Ratings
   - Port: 3001
   - Nutzt PostgreSQL für Datenpersistenz

4. **cookidoo-assistant-api** (`service:api`)
   - REST API für zukünftige Web/Mobile UI
   - Port: 3002
   - Niedrigere Priorität (später)

## Arbeitsweise

### GitHub Integration

**WICHTIG**: Alle erstellten Issues MÜSSEN automatisch zum zentralen Project Board hinzugefügt werden:
- Project Board URL: https://github.com/users/TheRealKoller/projects/5
- Project ID: 5
- Owner: TheRealKoller
- Nach jedem `gh issue create` muss `gh project item-add` aufgerufen werden

### Service-Labels für Issues

Beim Erstellen oder Bearbeiten von Issues **immer** den passenden Service-Label hinzufügen:

- `service:cookidoo-mcp` - Issues für cookidoo-mcp Service
- `service:shared` - Issues für Shared Library
- `service:assistant-mcp` - Issues für cookidoo-assistant-mcp Service
- `service:api` - Issues für cookidoo-assistant-api Service

**Beispiel:**
```bash
gh issue create --title "Add new MCP tool" --body "Description" \
  --label "service:cookidoo-mcp" \
  --repo TheRealKoller/cookidoo-assistant

# Issue MUSS zum Project Board hinzugefügt werden:
gh project item-add 5 --owner TheRealKoller --url <issue-url>
```

### Entwicklungs-Workflow

1. Issue aus dem Project Board auswählen
2. Feature-Branch erstellen (mit Conventional Naming)
3. Änderungen im entsprechenden Service implementieren
4. Tests schreiben und ausführen
5. Commit mit Conventional Commits
6. Pull Request erstellen und mit Issue verknüpfen

### Workspace Commands

Als npm workspace können alle Services zentral verwaltet werden:

```bash
# Alle Services: Dependencies installieren
npm install

# Alle Services: Tests ausführen
npm test

# Alle Services: Build ausführen
npm run build

# Alle Services: Linting
npm run lint

# Einzelner Service
npm run dev --workspace=cookidoo-mcp
npm test --workspace=cookidoo-assistant-shared
```

## Verfügbare Skills

- **github-workflow**: GitHub Issues, Project Board, Pull Requests
- **git-workflow**: Branch-Management, Commits, Push/Pull
- **test-and-build**: Testing und CI/CD-Prozesse

## Projekt-Standards

### Branch-Naming
- `feature/ISSUE_NUMBER-description` - Neue Features
- `fix/ISSUE_NUMBER-description` - Bugfixes
- `docs/ISSUE_NUMBER-description` - Dokumentation
- `refactor/ISSUE_NUMBER-description` - Code-Refactoring

**Beispiel:** `feature/21-implement-recipe-search-tool`

### Commit-Messages

Folge der [Conventional Commits](https://www.conventionalcommits.org/) Spezifikation:

- `feat(service):` - Neue Features (z.B. `feat(mcp): add recipe search tool`)
- `fix(service):` - Bugfixes (z.B. `fix(shared): correct database connection`)
- `docs:` - Dokumentationsänderungen
- `test(service):` - Test-Änderungen
- `refactor(service):` - Code-Refactoring
- `chore:` - Maintenance-Aufgaben (Dependencies, Config, etc.)

**Service Scopes:**
- `mcp` - cookidoo-mcp (Python)
- `shared` - cookidoo-assistant-shared (TypeScript)
- `assistant-mcp` - cookidoo-assistant-mcp (TypeScript)
- `api` - cookidoo-assistant-api (TypeScript)

**Beispiele:**
```
feat(mcp): implement search_recipes MCP tool
fix(shared): resolve database connection pool exhaustion
docs: update README with new architecture
test(assistant-mcp): add unit tests for user profile service
refactor(api): extract middleware to separate modules
chore: update dependencies across all services
chore(mcp): upgrade cookidoo-api to 0.18.0
```

### Python Code Style (cookidoo-mcp)

**Formatter & Linter:** `ruff` (all-in-one: linting, formatting, import sorting)

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Fix auto-fixable issues
ruff check --fix .
```

**Naming Conventions:**
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions/Methods: `snake_case()`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore()`
- Module-level private: `_single_underscore`

**Type Hints:**
- Use type hints for all function signatures
- Use `typing` module for complex types
- Run `mypy` for type checking

**Example:**
```python
from typing import Optional, List
from cookidoo_api import Cookidoo
from cookidoo_api.types import CookidooRecipeDetails

async def get_recipe_details(
    cookidoo: Cookidoo,
    recipe_id: str
) -> Optional[CookidooRecipeDetails]:
    """Fetch recipe details from Cookidoo API.
    
    Args:
        cookidoo: Authenticated Cookidoo instance
        recipe_id: Recipe ID (e.g., "r59322")
        
    Returns:
        Recipe details or None if not found
    """
    try:
        return await cookidoo.get_recipe_details(recipe_id)
    except CookidooException as e:
        logger.error(f"Failed to fetch recipe {recipe_id}: {e}")
        return None
```

**Docstrings:**
- Use Google-style docstrings
- Document all public functions, classes, and methods
- Include Args, Returns, Raises sections

**Imports:**
- Standard library first
- Third-party libraries second
- Local modules last
- Sorted alphabetically within each group
- `ruff` handles this automatically

**Testing:**
- Use `pytest` for all tests
- Place tests in `tests/` directory mirroring `src/` structure
- Test file naming: `test_<module>.py`
- Test function naming: `test_<function>_<scenario>()`
- Use `pytest-asyncio` for async tests
- Use fixtures for common setup

**Example:**
```python
import pytest
from cookidoo_mcp.tools import get_recipe_details

@pytest.mark.asyncio
async def test_get_recipe_details_success(mock_cookidoo):
    """Test successful recipe details retrieval."""
    result = await get_recipe_details(mock_cookidoo, "r59322")
    assert result is not None
    assert result.id == "r59322"

@pytest.mark.asyncio
async def test_get_recipe_details_not_found(mock_cookidoo):
    """Test recipe not found returns None."""
    result = await get_recipe_details(mock_cookidoo, "invalid")
    assert result is None
```

### TypeScript Code Style (shared, assistant-mcp, api)

**Formatter & Linter:** ESLint + Prettier

```bash
# Format code
npm run format

# Lint code
npm run lint

# Fix auto-fixable issues
npm run lint:fix
```

**Naming Conventions:**
- Files: `kebab-case.ts` or `PascalCase.ts` (for classes)
- Classes/Interfaces/Types: `PascalCase`
- Functions/Variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Private properties: `#privateField` or `_privateField`

**Type Safety:**
- Use strict TypeScript mode
- Avoid `any` - use `unknown` or proper types
- Use `interface` for object shapes, `type` for unions/intersections
- Export types alongside implementations

**Example:**
```typescript
interface RecipeSearchParams {
  query?: string;
  ingredients?: string[];
  maxResults?: number;
}

interface RecipeDetails {
  id: string;
  title: string;
  ingredients: Ingredient[];
  instructions: string[];
}

async function searchRecipes(
  params: RecipeSearchParams
): Promise<RecipeDetails[]> {
  // Implementation
}
```

**Testing:**
- Use `Jest` for unit tests
- Use `Supertest` for API integration tests
- Test file naming: `<module>.test.ts` or `<module>.spec.ts`
- Place tests next to source files or in `tests/` directory

**Example:**
```typescript
import { searchRecipes } from './recipes';

describe('searchRecipes', () => {
  it('should return recipes matching query', async () => {
    const results = await searchRecipes({ query: 'pasta' });
    expect(results).toHaveLength(10);
    expect(results[0].title).toContain('Pasta');
  });

  it('should filter by ingredients', async () => {
    const results = await searchRecipes({ ingredients: ['tomato'] });
    expect(results.every(r => 
      r.ingredients.some(i => i.name.includes('tomato'))
    )).toBe(true);
  });
});
```

### Project Structure

#### cookidoo-mcp (Python)
```
cookidoo-mcp/
├── src/
│   ├── cookidoo_mcp/
│   │   ├── __init__.py
│   │   ├── server.py              # MCP server entry point
│   │   ├── tools/                 # MCP tool implementations
│   │   │   ├── __init__.py
│   │   │   ├── recipes.py         # Recipe-related tools
│   │   │   ├── collections.py     # Collection tools
│   │   │   ├── calendar.py        # Calendar/weekplan tools
│   │   │   └── shopping_list.py   # Shopping list tools
│   │   ├── auth.py                # Authentication logic
│   │   ├── config.py              # Configuration
│   │   └── utils.py               # Utility functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── test_tools/
│   │   ├── test_recipes.py
│   │   ├── test_collections.py
│   │   ├── test_calendar.py
│   │   └── test_shopping_list.py
│   └── test_auth.py
├── docs/                          # Documentation
├── .env.example                   # Environment template
├── requirements.txt               # Python dependencies
├── requirements-dev.txt           # Dev dependencies (pytest, mypy, ruff)
├── pyproject.toml                 # Python project config (ruff, mypy)
├── Dockerfile                     # Python 3.11+ runtime
└── README.md
```

#### TypeScript Services (shared, assistant-mcp, api)
```
<service-name>/
├── src/
│   ├── config/                    # Configuration
│   ├── models/                    # Data models (TypeORM/Prisma)
│   ├── repositories/              # Data access layer
│   ├── services/                  # Business logic
│   ├── tools/                     # MCP tools (assistant-mcp only)
│   ├── routes/                    # Express routes (api only)
│   ├── middleware/                # Middleware
│   ├── types/                     # TypeScript type definitions
│   ├── utils/                     # Utility functions
│   └── index.ts                   # Entry point
├── tests/
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   ├── fixtures/                  # Test data
│   └── helpers/                   # Test utilities
├── migrations/                    # Database migrations
├── docs/                          # Documentation
├── .env.example                   # Environment template
├── package.json
├── tsconfig.json
├── Dockerfile
└── README.md
```

### Pull Requests

- Verknüpfe PRs immer mit dem entsprechenden Issue (`Closes #X`)
- Füge aussagekräftige Beschreibungen hinzu
- Liste alle betroffenen Services auf
- Stelle sicher, dass alle Tests durchlaufen
- Referenziere Service-Labels in der Beschreibung

**PR Title Format:** `[Service] Short description (#ISSUE_NUMBER)`

**Beispiel:**
```
Title: [cookidoo-mcp] Implement recipe search tool (#24)

Description:
Implements the `search_recipes` MCP tool for cookidoo-mcp service.

Services affected:
- cookidoo-mcp

Closes #24
```

## Issue-Nummerierung (nach Migration)

**Hinweis:** Issues wurden von zwei Repositories in dieses Monorepo konsolidiert:

**Original cookidoo-assistant Issues:**
- #1-19 (unverändert)

**Transferierte cookidoo-mcp Issues:**
- cookidoo-mcp#1 → cookidoo-assistant#20
- cookidoo-mcp#2 → cookidoo-assistant#21
- ...
- cookidoo-mcp#11 → cookidoo-assistant#30

Bei Referenzen auf alte Issues aus `cookidoo-mcp` immer die neuen Nummern verwenden.

## Tech Stack

**Status:** ✅ Entschieden - siehe Issue #21

### Cookidoo-MCP Service (Python)
- **Language:** Python 3.11+
- **MCP SDK:** `mcp` Python SDK (Model Context Protocol)
- **Cookidoo API:** `cookidoo-api==0.17.0` (miaucl/cookidoo-api)
- **Async:** `asyncio` + `aiohttp`
- **Testing:** `pytest` + `pytest-asyncio`
- **Type Hints:** Full type annotations with `mypy`
- **Linting:** `ruff` (replaces flake8, isort, black)
- **Package Management:** `pip` + `requirements.txt`

### Other Services (TypeScript)
- **Language:** TypeScript 5+
- **Runtime:** Node.js 18+
- **MCP SDK:** `@modelcontextprotocol/sdk` (cookidoo-assistant-mcp only)
- **Framework:** Express.js (cookidoo-assistant-api)
- **ORM:** TypeORM or Prisma (shared library)
- **Testing:** Jest + Supertest
- **Linting:** ESLint + Prettier
- **Package Management:** npm workspaces

### Why Python for cookidoo-mcp?
- Native integration with `cookidoo-api` library (no bridge needed)
- 85% feature completeness out-of-the-box
- Actively maintained upstream (last release Apr 2026)
- Comprehensive test coverage and documentation
- MCP Python SDK available with async/await support

## Deployment

### Docker

Alle Services haben eigene Dockerfiles und werden via `docker-compose.yml` orchestriert:

```bash
# Alle Services starten
docker-compose up

# Einzelner Service
docker-compose up cookidoo-mcp

# Mit rebuild
docker-compose up --build
```

### Datenbanken

- `cookidoo-assistant-mcp`: Eigene PostgreSQL-Instanz
- `cookidoo-assistant-api`: Eigene PostgreSQL-Instanz
- `cookidoo-assistant-shared`: Stellt DB-Connection-Management bereit

## Entwicklungsumgebung

### Prerequisites

- **Python 3.11+** (für cookidoo-mcp)
- **Node.js >= 18** (für TypeScript Services)
- Docker & Docker Compose
- PostgreSQL (via Docker)
- Gültiges Cookidoo-Abo (für Testing und Development)

### Setup

```bash
# Repository klonen
git clone https://github.com/TheRealKoller/cookidoo-assistant.git
cd cookidoo-assistant

# TypeScript Services: Dependencies installieren
npm install

# Python Service (cookidoo-mcp): Virtual Environment + Dependencies
cd cookidoo-mcp
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder: venv\Scripts\activate  # Windows
pip install -r requirements.txt
cd ..

# Environment Variables konfigurieren
cp cookidoo-mcp/.env.example cookidoo-mcp/.env
cp cookidoo-assistant-mcp/.env.example cookidoo-assistant-mcp/.env
cp cookidoo-assistant-api/.env.example cookidoo-assistant-api/.env
# .env Dateien mit echten Credentials befüllen

# Datenbank starten
docker-compose up -d postgres

# Services starten
cd cookidoo-mcp && source venv/bin/activate && python src/server.py  # Port 3000
npm run dev:assistant-mcp                                              # Port 3001
npm run dev:assistant-api                                              # Port 3002
```

## Weitere Informationen

- **Project Board**: https://github.com/users/TheRealKoller/projects/5
- **Issues Summary**: `.opencode/ISSUES_SUMMARY.md`
- **Service READMEs**: Jeder Service hat ein eigenes `README.md`
