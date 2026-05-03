# Created GitHub Issues - Summary

## Overview
Total Issues Created: **29 issues** across 2 repositories

---

## cookidoo-mcp Repository (11 Issues)

### Setup & Infrastructure (3 issues)
1. **#1 - Setup: Initialize Monorepo Structure** ⭐ HIGH PRIORITY
   - Initialize monorepo with workspaces
   - Create directory structure
   - Setup basic configuration

2. **#2 - Setup: Evaluate Cookidoo API Libraries** ⭐ HIGH PRIORITY
   - Evaluate miaucl/cookidoo-api (Python)
   - Evaluate tobim-dev/cookidoo-scraper (TypeScript)
   - Document comparison and recommendation

3. **#3 - Setup: Docker Configuration for cookidoo-mcp** ⭐ HIGH PRIORITY
   - Create Dockerfile
   - Setup docker-compose
   - Configure port 3000
   - Dependencies: #2

### Core Features (6 issues)
4. **#4 - Feature: Implement MCP Server Core** ⭐ HIGH PRIORITY
   - Setup MCP server framework
   - Implement authentication
   - Connect to Cookidoo API
   - Dependencies: #2, #3

5. **#5 - Feature: Implement search_recipes MCP Tool** ⭐ HIGH PRIORITY
   - Universal search (freetext + ingredients)
   - Dietary filters
   - Pagination
   - Dependencies: #4

6. **#6 - Feature: Implement get_recipe_details MCP Tool** ⭐ HIGH PRIORITY
   - Get full recipe information
   - Parse all recipe fields
   - Dependencies: #4

7. **#7 - Feature: Implement get_recipe_nutrition MCP Tool** ⭐ HIGH PRIORITY
   - Get nutritional information
   - Handle missing data
   - Dependencies: #4, #2

8. **#8 - Feature: Implement search_ingredients MCP Tool** 🔵 MEDIUM PRIORITY
   - Search and filter ingredients
   - Fuzzy matching
   - Dependencies: #4, #2

9. **#9 - Feature: Implement add_recipe_to_weekplan MCP Tool** ⭐ HIGH PRIORITY
   - Add recipes to Cookidoo week plan
   - Handle conflicts
   - Dependencies: #4, #2

### Testing & Documentation (2 issues)
10. **#10 - Testing: Setup Unit Test Infrastructure** ⭐ HIGH PRIORITY
    - Setup test framework
    - Configure coverage
    - Setup mocking

11. **#11 - Documentation: Create Comprehensive README and API Documentation** 🔵 MEDIUM PRIORITY
    - README with setup guide
    - MCP tools documentation
    - Usage examples

---

## cookidoo-assistant Repository (18 Issues)

### Setup & Infrastructure (2 issues)
1. **#1 - Setup: Docker Configuration for cookidoo-assistant Services** ⭐ HIGH PRIORITY
   - Configure all services (shared, mcp, api)
   - Setup PostgreSQL databases
   - Create docker-compose.yml

2. **#2 - Setup: GitHub Actions CI/CD Pipeline** 🔵 MEDIUM PRIORITY
   - CI workflow (tests, builds)
   - Release workflow
   - E2E test workflow

### Shared Library (4 issues)
3. **#3 - Feature: Setup cookidoo-assistant-shared Library** ⭐ HIGH PRIORITY - BLOCKING
   - Initialize shared package
   - Setup database connection
   - Create base utilities

4. **#4 - Feature: Implement Database Schema and Migrations** ⭐ HIGH PRIORITY - BLOCKING
   - Design complete schema (8 tables)
   - Create migration system
   - Add indexes and constraints

5. **#5 - Feature: Implement Data Access Layer (Repositories)** ⭐ HIGH PRIORITY
   - Implement 8 repositories
   - CRUD operations
   - Dependencies: #4

6. **#6 - Feature: Implement Business Logic Services** ⭐ HIGH PRIORITY
   - UserService
   - HealthCalculatorService
   - RecipePreferenceService
   - WeekPlanService
   - Dependencies: #5

### MCP Server (7 issues)
7. **#7 - Feature: Implement MCP Server Core for cookidoo-assistant-mcp** ⭐ HIGH PRIORITY
   - Setup MCP server
   - Connect to database
   - Integrate shared library
   - Dependencies: #1, #3

8. **#8 - Feature: Implement User Profile MCP Tools (CRUD)** ⭐ HIGH PRIORITY
   - 4 CRUD tools for user profiles
   - Dependencies: #7, #5

9. **#9 - Feature: Implement Dietary Preferences MCP Tools (CRUD)** ⭐ HIGH PRIORITY
   - 4 CRUD tools for dietary preferences
   - Dependencies: #7, #5

10. **#10 - Feature: Implement Allergies MCP Tools (CRUD)** ⭐ HIGH PRIORITY
    - 4 CRUD tools for allergies
    - Dependencies: #7, #5

11. **#11 - Feature: Implement Health Data MCP Tools (CRUD)** ⭐ HIGH PRIORITY
    - 5 CRUD tools for health data
    - Includes auto-calculation
    - Dependencies: #7, #6

12. **#12 - Feature: Implement Recipe Ratings MCP Tools (CRUD)** ⭐ HIGH PRIORITY
    - 6 CRUD tools for recipe ratings
    - Automatic tracking
    - Dependencies: #7, #6

13. **#13 - Feature: Implement Week Plan MCP Tools (CRUD)** ⭐ HIGH PRIORITY
    - 8 CRUD tools for week plans
    - Automatic dislike tracking
    - Dependencies: #7, #6, #12

### REST API (2 issues)
14. **#14 - Feature: Implement REST API Server for cookidoo-assistant-api** 🔵 MEDIUM PRIORITY
    - Setup REST API framework
    - Port 3002
    - OpenAPI documentation
    - Dependencies: #1, #3

15. **#15 - Feature: Implement REST API Endpoints - All CRUD Operations** 🔵 MEDIUM PRIORITY
    - Implement all REST endpoints
    - Request/response validation
    - Dependencies: #14, #5, #6

### Testing (2 issues)
16. **#16 - Testing: Setup Unit and Integration Test Infrastructure** ⭐ HIGH PRIORITY
    - Setup test framework
    - Configure test database
    - Coverage reporting

17. **#17 - Testing: Setup E2E Test Infrastructure** 🔵 MEDIUM PRIORITY
    - E2E test scenarios
    - Docker test environment
    - Dependencies: #16

### Documentation (1 issue)
18. **#18 - Documentation: Create Comprehensive Documentation for All Services** 🔵 MEDIUM PRIORITY
    - README for all services
    - Architecture diagrams
    - API documentation

---

## Next Steps

### 1. Add Issues to Project Board
You need to refresh GitHub CLI authentication with project scope:
```bash
gh auth refresh -s project
```

Then add all issues to the project board:
```bash
# Add cookidoo-mcp issues
for i in {1..11}; do
  gh project item-add 5 --owner TheRealKoller --url "https://github.com/TheRealKoller/cookidoo-mcp/issues/$i"
done

# Add cookidoo-assistant issues
for i in {1..18}; do
  gh project item-add 5 --owner TheRealKoller --url "https://github.com/TheRealKoller/cookidoo-assistant/issues/$i"
done
```

### 2. Prioritized Implementation Order

#### Phase 1: Foundation (MUST DO FIRST)
1. cookidoo-mcp #1 - Initialize Monorepo Structure
2. cookidoo-mcp #2 - Evaluate Cookidoo API Libraries
3. cookidoo-assistant #3 - Setup shared library
4. cookidoo-assistant #4 - Database Schema and Migrations

#### Phase 2: Core Infrastructure
5. cookidoo-mcp #3 - Docker Configuration
6. cookidoo-assistant #1 - Docker Configuration
7. cookidoo-mcp #10 - Unit Test Infrastructure
8. cookidoo-assistant #16 - Test Infrastructure

#### Phase 3: Core Features
9. cookidoo-mcp #4 - MCP Server Core
10. cookidoo-assistant #5 - Data Access Layer
11. cookidoo-assistant #6 - Business Logic Services
12. cookidoo-assistant #7 - MCP Server Core

#### Phase 4: MCP Tools
13. cookidoo-mcp #5-9 - All MCP tools for Cookidoo
14. cookidoo-assistant #8-13 - All MCP tools for Assistant

#### Phase 5: REST API (Lower Priority)
15. cookidoo-assistant #14-15 - REST API implementation

#### Phase 6: Advanced Testing & Documentation
16. cookidoo-assistant #17 - E2E Tests
17. cookidoo-assistant #2 - GitHub Actions CI/CD
18. cookidoo-mcp #11 - Documentation
19. cookidoo-assistant #18 - Documentation

---

## Issue Statistics

### By Priority
- ⭐ **HIGH Priority**: 21 issues (72%)
- 🔵 **MEDIUM Priority**: 8 issues (28%)

### By Category
- **Setup & Infrastructure**: 5 issues
- **Core Features**: 16 issues
- **Testing**: 4 issues
- **Documentation**: 2 issues
- **CI/CD**: 1 issue
- **REST API**: 2 issues

### By Repository
- **cookidoo-mcp**: 11 issues
- **cookidoo-assistant**: 18 issues

---

## Dependencies Graph

### Critical Path (Blocking Issues)
```
#1 Monorepo Setup
  └─> #2 Evaluate APIs
       └─> #3 Docker (mcp)
            └─> #4 MCP Core (mcp)
                 └─> #5-9 MCP Tools (mcp)

#3 Shared Library Setup
  └─> #4 Database Schema
       └─> #5 Data Access Layer
            └─> #6 Business Logic
                 └─> #7 MCP Core (assistant)
                      └─> #8-13 MCP Tools (assistant)
```

### Parallel Tracks
- **Testing**: Can be setup in parallel with feature development
- **Documentation**: Can be done continuously or at the end
- **REST API**: Independent from MCP implementation
- **CI/CD**: Can be setup anytime after basic structure exists

---

## Labels Used
- `setup`, `infrastructure` - Setup and configuration
- `feature` - New features
- `mcp-server`, `mcp-tool` - MCP-related
- `api`, `rest` - REST API-related
- `database`, `schema` - Database-related
- `testing`, `unit-tests`, `integration-tests`, `e2e` - Testing
- `documentation` - Documentation
- `ci/cd`, `github-actions` - CI/CD
- `crud` - CRUD operations

---

## Total Estimated Effort
Based on the scope and complexity, this is a **multi-month project** with:
- **Phase 1-2 (Foundation)**: 2-3 weeks
- **Phase 3-4 (Core Features)**: 4-6 weeks
- **Phase 5-6 (Polish)**: 2-3 weeks

**Total**: 8-12 weeks for full implementation with testing and documentation
