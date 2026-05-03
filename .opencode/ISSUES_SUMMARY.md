# Issues Summary - Cookidoo Assistant Monorepo

**Repository**: https://github.com/TheRealKoller/cookidoo-assistant  
**Project Board**: https://github.com/users/TheRealKoller/projects/5

## Issue Nummerierung nach Monorepo Migration

Dieses Monorepo konsolidiert Issues aus zwei ehemaligen Repositories:

**Original cookidoo-assistant Issues**: #1-19 (unverändert)  
**Transferierte cookidoo-mcp Issues**: cookidoo-mcp#1-11 → #20-30

---

## Issues by Service

### 🔧 Setup & Infrastructure (Priority: High)

#### service:cookidoo-mcp
- **#20** - Setup: Initialize Monorepo Structure ✅ COMPLETED
  - Dependencies: None
  - Status: Done

- **#21** - Setup: Evaluate Cookidoo API Libraries
  - Dependencies: None
  - Status: Todo
  - **BLOCKS**: #19, #22, #23-28
  - Description: Evaluate miaucl/cookidoo-api (Python) vs tobim-dev/cookidoo-scraper (TypeScript)

- **#22** - Setup: Docker Configuration for cookidoo-mcp
  - Dependencies: #21 (tech stack decision)
  - Status: Todo

#### service:shared + service:assistant-mcp + service:api
- **#1** - Setup: Docker Configuration for cookidoo-assistant Services
  - Dependencies: #3, #21 (tech stack)
  - Status: Todo
  - Description: Docker setup for shared, assistant-mcp, and api services

- **#2** - Setup: GitHub Actions CI/CD Pipeline
  - Dependencies: #1, #21
  - Status: Todo
  - Description: CI/CD for all services (build, test, deploy)

#### service:shared
- **#3** - Feature: Setup cookidoo-assistant-shared Library
  - Dependencies: #21 (tech stack decision)
  - Status: Todo
  - **BLOCKS**: #4, #5, #6, #7-13, #14-15
  - Description: Initialize shared library structure

---

### 📚 Shared Library (service:shared)

- **#4** - Feature: Implement Database Schema and Migrations
  - Dependencies: #3
  - Status: Todo
  - **BLOCKS**: #5, #6
  - Description: PostgreSQL schema for users, preferences, allergies, health_data, recipe_ratings, week_plans

- **#5** - Feature: Implement Data Access Layer (Repositories)
  - Dependencies: #3, #4
  - Status: Todo
  - **BLOCKS**: #6
  - Description: Repository pattern for all entities

- **#6** - Feature: Implement Business Logic Services
  - Dependencies: #3, #4, #5
  - Status: Todo
  - **BLOCKS**: #7-13
  - Description: Service layer for business logic

---

### 🤖 MCP Server - Cookidoo API (service:cookidoo-mcp)

- **#23** - Feature: Implement MCP Server Core
  - Dependencies: #21 (tech stack)
  - Status: Todo
  - **BLOCKS**: #24-28
  - Description: MCP server initialization, authentication, error handling

- **#24** - Feature: Implement search_recipes MCP Tool
  - Dependencies: #23
  - Status: Todo
  - Description: Search recipes by text, ingredients, filters (country, category, difficulty)

- **#25** - Feature: Implement get_recipe_nutrition MCP Tool
  - Dependencies: #23
  - Status: Todo
  - Description: Get detailed nutrition info for a recipe

- **#26** - Feature: Implement get_recipe_details MCP Tool
  - Dependencies: #23
  - Status: Todo
  - Description: Get full recipe details (ingredients, steps, images, etc.)

- **#27** - Feature: Implement search_ingredients MCP Tool
  - Dependencies: #23
  - Status: Todo
  - Description: Search available ingredients

- **#28** - Feature: Implement add_recipe_to_weekplan MCP Tool
  - Dependencies: #23
  - Status: Todo
  - Description: Add recipe to Cookidoo weekplan

---

### 🤖 MCP Server - User Data (service:assistant-mcp)

- **#7** - Feature: Implement MCP Server Core for cookidoo-assistant-mcp
  - Dependencies: #3, #6
  - Status: Todo
  - **BLOCKS**: #8-13
  - Description: MCP server for user data management

- **#8** - Feature: Implement User Profile MCP Tools (CRUD)
  - Dependencies: #7
  - Status: Todo
  - Description: create_user, get_user, update_user, delete_user

- **#9** - Feature: Implement Dietary Preferences MCP Tools (CRUD)
  - Dependencies: #7
  - Status: Todo
  - Description: CRUD operations for dietary preferences (omnivore, vegetarian, vegan, etc.)

- **#10** - Feature: Implement Allergies MCP Tools (CRUD)
  - Dependencies: #7
  - Status: Todo
  - Description: CRUD operations for user allergies and intolerances

- **#11** - Feature: Implement Health Data MCP Tools (CRUD)
  - Dependencies: #7
  - Status: Todo
  - Description: CRUD for health data (weight, height, age, activity level, goals)
  - Note: Includes Harris-Benedict formula for BMR/TDEE calculation

- **#12** - Feature: Implement Recipe Ratings MCP Tools (CRUD)
  - Dependencies: #7
  - Status: Todo
  - Description: CRUD for recipe ratings (liked/disliked)
  - Note: Automatic tracking + manual feedback

- **#13** - Feature: Implement Week Plan MCP Tools (CRUD)
  - Dependencies: #7
  - Status: Todo
  - Description: CRUD for week plans (7 days, 1 meal initially)
  - Note: Recipes fetched from Cookidoo via cookidoo-mcp

---

### 🌐 REST API (service:api) - Lower Priority

- **#14** - Feature: Implement REST API Server for cookidoo-assistant-api
  - Dependencies: #3, #6
  - Status: Todo
  - **BLOCKS**: #15
  - Description: Express/FastAPI server with authentication, middleware, error handling

- **#15** - Feature: Implement REST API Endpoints - All CRUD Operations
  - Dependencies: #14
  - Status: Todo
  - Description: REST endpoints mirroring MCP tools functionality

---

### 🧪 Testing

- **#29** - Testing: Setup Unit Test Infrastructure (service:cookidoo-mcp)
  - Dependencies: #23
  - Status: Todo
  - Description: Jest/pytest setup, test utilities, mocking

- **#16** - Testing: Setup Unit and Integration Test Infrastructure
  - Dependencies: #3, #6, #7
  - Status: Todo
  - Services: shared, assistant-mcp, api
  - Description: Comprehensive test setup for all non-cookidoo-mcp services

- **#17** - Testing: Setup E2E Test Infrastructure
  - Dependencies: #7, #14
  - Status: Todo
  - Services: assistant-mcp, api
  - Description: End-to-end testing across services

---

### 📖 Documentation

- **#30** - Documentation: Create Comprehensive README and API Documentation (service:cookidoo-mcp)
  - Dependencies: #24-28
  - Status: Todo
  - Description: README, MCP tools reference, examples

- **#18** - Documentation: Create Comprehensive Documentation for All Services
  - Dependencies: #8-13, #15
  - Status: Todo
  - Services: shared, assistant-mcp, api
  - Description: API docs, architecture diagrams, deployment guides

---

### 🎯 Meta

- **#19** - Meta: Create Tech-Stack-Specific Instructions and Skills
  - Dependencies: #21 (tech stack decision)
  - Status: Todo
  - Services: ALL
  - **CRITICAL**: Must be done immediately after #21
  - Description: Update .opencode/ with tech-stack-specific workflows

---

## Dependency Graph

```
#21 (Evaluate Tech Stack) - BLOCKS EVERYTHING
├── #19 (Tech-Stack Instructions) - CRITICAL
├── #22 (Docker cookidoo-mcp)
├── #23 (MCP Core cookidoo-mcp)
│   ├── #24 (search_recipes)
│   ├── #25 (get_recipe_nutrition)
│   ├── #26 (get_recipe_details)
│   ├── #27 (search_ingredients)
│   ├── #28 (add_recipe_to_weekplan)
│   └── #29 (Testing cookidoo-mcp)
│       └── #30 (Docs cookidoo-mcp)
└── #3 (Setup Shared Library)
    ├── #4 (Database Schema)
    │   └── #5 (Data Access Layer)
    │       └── #6 (Business Logic)
    │           ├── #1 (Docker assistant services)
    │           │   └── #2 (CI/CD)
    │           ├── #7 (MCP Core assistant-mcp)
    │           │   ├── #8 (User Profile)
    │           │   ├── #9 (Dietary Preferences)
    │           │   ├── #10 (Allergies)
    │           │   ├── #11 (Health Data)
    │           │   ├── #12 (Recipe Ratings)
    │           │   └── #13 (Week Plan)
    │           └── #14 (REST API Server)
    │               └── #15 (REST API Endpoints)
    └── #16 (Testing shared/assistant-mcp/api)
        └── #17 (E2E Testing)
            └── #18 (Docs shared/assistant-mcp/api)
```

---

## Development Phases

### Phase 1: Foundation ⏳ IN PROGRESS
1. ✅ #20 - Initialize Monorepo (DONE)
2. ⏳ #21 - Evaluate Tech Stack (NEXT - CRITICAL)
3. 🚨 #19 - Tech-Stack Instructions (IMMEDIATELY after #21)
4. #22 - Docker cookidoo-mcp
5. #3 - Setup Shared Library
6. #1 - Docker assistant services
7. #2 - CI/CD Pipeline

### Phase 2: Core Features
1. #23 - MCP Core cookidoo-mcp
2. #24-28 - Cookidoo MCP Tools
3. #4 - Database Schema
4. #5 - Data Access Layer
5. #6 - Business Logic Services
6. #7 - MCP Core assistant-mcp
7. #8-13 - Assistant MCP Tools

### Phase 3: Testing & Documentation
1. #29 - Testing cookidoo-mcp
2. #16 - Testing shared/assistant-mcp/api
3. #17 - E2E Testing
4. #30 - Docs cookidoo-mcp
5. #18 - Docs shared/assistant-mcp/api

### Phase 4: REST API (Lower Priority)
1. #14 - REST API Server
2. #15 - REST API Endpoints

---

## Quick Reference: Issue Numbers

### Old → New Mapping (Transferred Issues)
```
cookidoo-mcp#1  → cookidoo-assistant#20 (Initialize Monorepo) ✅
cookidoo-mcp#2  → cookidoo-assistant#21 (Evaluate Tech Stack)
cookidoo-mcp#3  → cookidoo-assistant#22 (Docker cookidoo-mcp)
cookidoo-mcp#4  → cookidoo-assistant#23 (MCP Core)
cookidoo-mcp#5  → cookidoo-assistant#24 (search_recipes)
cookidoo-mcp#6  → cookidoo-assistant#26 (get_recipe_details)
cookidoo-mcp#7  → cookidoo-assistant#25 (get_recipe_nutrition)
cookidoo-mcp#8  → cookidoo-assistant#27 (search_ingredients)
cookidoo-mcp#9  → cookidoo-assistant#28 (add_recipe_to_weekplan)
cookidoo-mcp#10 → cookidoo-assistant#29 (Testing)
cookidoo-mcp#11 → cookidoo-assistant#30 (Documentation)
```

### By Service Label
- **service:cookidoo-mcp**: #19, #20, #21, #22, #23, #24, #25, #26, #27, #28, #29, #30
- **service:shared**: #1, #2, #3, #4, #5, #6, #16, #18, #19
- **service:assistant-mcp**: #1, #2, #7, #8, #9, #10, #11, #12, #13, #16, #17, #18, #19
- **service:api**: #1, #2, #14, #15, #16, #17, #18, #19

---

## Next Actions

1. **Start #21** - Evaluate Cookidoo API Libraries (Python vs TypeScript)
2. **Immediately after #21**: Do #19 - Create Tech-Stack Instructions
3. **Then**: Begin parallel work on #22 (Docker cookidoo-mcp) and #3 (Setup Shared)

All 30 issues are tracked on the [Project Board](https://github.com/users/TheRealKoller/projects/5).
