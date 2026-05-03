# Cookidoo Assistant - Monorepo

> **Note:** This repository consolidates all Cookidoo Assistant services. The previous `cookidoo-mcp` repository has been archived and merged here.

AI-powered meal planning assistant using Cookidoo recipes with MCP servers and REST API.

## 🎯 Project Goal

Create an intelligent meal planning system that generates weekly meal plans based on:
- Regional and seasonal availability
- User dietary preferences (omnivore, vegetarian, vegan, etc.)
- Allergies and intolerances
- Health data and nutrition goals
- User recipe preferences (liked/disliked recipes)

## 🏗️ Architecture

This is a **monorepo** containing all services in a single repository:

```
cookidoo-assistant/
├── cookidoo-mcp/                    # MCP Server for Cookidoo API
├── cookidoo-assistant-shared/       # Shared business logic & data layer
├── cookidoo-assistant-mcp/          # MCP Server for user data
└── cookidoo-assistant-api/          # REST API (for future UI)
```

### Services

#### 1. cookidoo-mcp (Port 3000) - Python
MCP Server that interfaces with Cookidoo API:
- **Language**: Python 3.11+
- **Library**: `cookidoo-api==0.17.0` (miaucl/cookidoo-api)
- **Features**: Recipe details, Custom/Managed collections, Calendar/Weekplan, Shopping List
- OAuth authentication with token refresh
- Full async/await support

#### 2. cookidoo-assistant-shared - TypeScript
Shared library containing:
- **Language**: TypeScript 5+
- Database models and repositories (TypeORM/Prisma)
- Business logic services
- Common utilities and types

#### 3. cookidoo-assistant-mcp (Port 3001) - TypeScript
MCP Server for managing user data:
- **Language**: TypeScript 5+
- **MCP SDK**: `@modelcontextprotocol/sdk`
- User profiles and preferences
- Dietary restrictions and allergies
- Health data and nutrition targets
- Recipe ratings (liked/disliked)
- Week plan management and history

#### 4. cookidoo-assistant-api (Port 3002) - TypeScript
REST API for future web/mobile UI (lower priority):
- **Language**: TypeScript 5+
- **Framework**: Express.js
- RESTful endpoints
- Same business logic as assistant-mcp (via shared library)

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (for cookidoo-mcp)
- **Node.js >= 18** (for TypeScript services)
- Docker and Docker Compose
- Valid Cookidoo subscription

### Installation

```bash
# Clone the repository
git clone https://github.com/TheRealKoller/cookidoo-assistant.git
cd cookidoo-assistant

# Install dependencies
npm install

# Setup environment variables
cp cookidoo-mcp/.env.example cookidoo-mcp/.env
cp cookidoo-assistant-mcp/.env.example cookidoo-assistant-mcp/.env
cp cookidoo-assistant-api/.env.example cookidoo-assistant-api/.env
# Edit .env files with your credentials
```

### Development

```bash
# Start all services with Docker Compose
npm run docker:up

# Or start individual services
npm run dev:mcp                  # cookidoo-mcp on port 3000
npm run dev:assistant-mcp        # cookidoo-assistant-mcp on port 3001
npm run dev:assistant-api        # cookidoo-assistant-api on port 3002
```

### Testing

```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage

# Lint all code
npm run lint

# Format all code
npm run format
```

## 📚 Documentation

- **Repository**: https://github.com/TheRealKoller/cookidoo-assistant
- **Project Board**: https://github.com/users/TheRealKoller/projects/5
- **Instructions**: [.opencode/instructions.md](.opencode/instructions.md)
- **Skills**: [.opencode/skills/](.opencode/skills/)
- Service-specific docs in each service's README

## 🛠️ Technology Stack

**Status**: ✅ Decided in [Issue #21](https://github.com/TheRealKoller/cookidoo-assistant/issues/21)

### Cookidoo-MCP (Python)
- **Language**: Python 3.11+
- **MCP SDK**: `mcp` (Python SDK)
- **Cookidoo API**: `cookidoo-api==0.17.0` (miaucl/cookidoo-api)
- **Async**: `asyncio` + `aiohttp`
- **Testing**: `pytest` + `pytest-asyncio`
- **Type Hints**: Full annotations with `mypy`
- **Linting/Format**: `ruff`

### TypeScript Services (shared, assistant-mcp, api)
- **Language**: TypeScript 5+
- **Runtime**: Node.js 18+
- **MCP SDK**: `@modelcontextprotocol/sdk` (assistant-mcp only)
- **Framework**: Express.js (api)
- **ORM**: TypeORM or Prisma (shared)
- **Testing**: Jest + Supertest
- **Linting/Format**: ESLint + Prettier

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Databases**: PostgreSQL (separate instances per service)
- **Package Management**: npm workspaces (TypeScript), pip (Python)

## 📊 Development Status

| Service | Status | Priority |
|---------|--------|----------|
| cookidoo-mcp | 🚧 Planning | High |
| cookidoo-assistant-shared | 🚧 Planning | High |
| cookidoo-assistant-mcp | 🚧 Planning | High |
| cookidoo-assistant-api | 📋 Planned | Medium |

## 🗺️ Roadmap

**Note:** Issue numbers updated after monorepo migration (old cookidoo-mcp#1-11 → #20-30)

### Phase 1: Foundation
- [x] #20 - Initialize Monorepo Structure ✅ COMPLETED
- [x] #21 - Evaluate Cookidoo API Libraries ✅ COMPLETED (Decision: Python + miaucl/cookidoo-api)
- [ ] #19 - Create Tech-Stack-Specific Instructions & Skills 🚧 IN PROGRESS
- [ ] Setup Docker infrastructure
- [ ] Database schema design

### Phase 2: Core Features
- [ ] Implement cookidoo-mcp MCP tools
- [ ] Implement shared library (DB, services)
- [ ] Implement cookidoo-assistant-mcp MCP tools

### Phase 3: Testing & Documentation
- [ ] Unit and integration tests
- [ ] E2E tests
- [ ] CI/CD pipeline
- [ ] Comprehensive documentation

### Phase 4: REST API (Future)
- [ ] REST API implementation
- [ ] API documentation (OpenAPI)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

### Workflow

1. Pick an issue from the [Project Board](https://github.com/users/TheRealKoller/projects/5)
2. Create a feature branch: `git checkout -b feature/ISSUE_NUMBER-description`
3. Make changes and commit using [Conventional Commits](https://www.conventionalcommits.org/)
4. Create a Pull Request referencing the issue
5. Ensure all tests pass and code is reviewed

## 📝 Project Standards

### Branch Naming
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring

### Commit Messages
Follow Conventional Commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

## 📄 License

MIT

## 🔗 Links

- **GitHub Repository**: https://github.com/TheRealKoller/cookidoo-assistant
- **GitHub Project Board**: https://github.com/users/TheRealKoller/projects/5
- **Archived cookidoo-mcp Repository**: https://github.com/TheRealKoller/cookidoo-mcp (archived, moved to monorepo)
- **Cookidoo**: https://cookidoo.de

## 📝 Project History

This repository consolidates the following projects:
- `cookidoo-mcp` (Issues #1-11 → transferred as #20-30)
- `cookidoo-assistant` (Issues #1-19 → unchanged)

All development now happens in this single monorepo.
