# Cookidoo Assistant - Monorepo

AI-powered meal planning assistant using Cookidoo recipes with MCP servers and REST API.

## 🎯 Project Goal

Create an intelligent meal planning system that generates weekly meal plans based on:
- Regional and seasonal availability
- User dietary preferences (omnivore, vegetarian, vegan, etc.)
- Allergies and intolerances
- Health data and nutrition goals
- User recipe preferences (liked/disliked recipes)

## 🏗️ Architecture

This is a monorepo containing multiple services:

```
cookidoo-assistant/
├── cookidoo-mcp/                    # MCP Server for Cookidoo API
├── cookidoo-assistant-shared/       # Shared business logic & data layer
├── cookidoo-assistant-mcp/          # MCP Server for user data
└── cookidoo-assistant-api/          # REST API (for future UI)
```

### Services

#### 1. cookidoo-mcp (Port 3000)
MCP Server that interfaces with Cookidoo:
- Search recipes (freetext, ingredients, filters)
- Get recipe details and nutrition info
- Manage week plans in Cookidoo

#### 2. cookidoo-assistant-shared
Shared library containing:
- Database models and repositories
- Business logic services
- Common utilities and types

#### 3. cookidoo-assistant-mcp (Port 3001)
MCP Server for managing user data:
- User profiles and preferences
- Dietary restrictions and allergies
- Health data and nutrition targets
- Recipe ratings (liked/disliked)
- Week plan management and history

#### 4. cookidoo-assistant-api (Port 3002)
REST API for future web/mobile UI (lower priority)

## 🚀 Quick Start

### Prerequisites

- Node.js >= 18 or Python >= 3.11 (tech stack TBD - see [Issue #2](https://github.com/TheRealKoller/cookidoo-mcp/issues/2))
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

- **Project Board**: https://github.com/users/TheRealKoller/projects/5
- **Instructions**: [.opencode/instructions.md](.opencode/instructions.md)
- **Skills**: [.opencode/skills/](.opencode/skills/)
- Service-specific docs in each service's README

## 🛠️ Technology Stack

**Status**: 🚧 To be decided in [Issue #2](https://github.com/TheRealKoller/cookidoo-mcp/issues/2)

Options:
- **TypeScript/Node.js** - Standard for MCP servers
- **Python** - Better integration with cookidoo-api library

## 📊 Development Status

| Service | Status | Priority |
|---------|--------|----------|
| cookidoo-mcp | 🚧 Planning | High |
| cookidoo-assistant-shared | 🚧 Planning | High |
| cookidoo-assistant-mcp | 🚧 Planning | High |
| cookidoo-assistant-api | 📋 Planned | Medium |

## 🗺️ Roadmap

### Phase 1: Foundation
- [ ] #1 - Initialize Monorepo Structure ✅ IN PROGRESS
- [ ] #2 - Evaluate Cookidoo API Libraries
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

- **GitHub Project Board**: https://github.com/users/TheRealKoller/projects/5
- **cookidoo-mcp Repository**: https://github.com/TheRealKoller/cookidoo-mcp
- **cookidoo-assistant Repository**: https://github.com/TheRealKoller/cookidoo-assistant
- **Cookidoo**: https://cookidoo.de
