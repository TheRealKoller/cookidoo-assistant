# Cookidoo Assistant - Instructions

## Projekt-Übersicht

Dieses Monorepo enthält die komplette Cookidoo Assistant Platform - ein AI-powered Meal Planning System basierend auf Cookidoo Rezepten mit MCP Servern und REST API.

### Repository

- **GitHub Repository**: https://github.com/TheRealKoller/cookidoo-assistant
- **Project Board**: https://github.com/users/TheRealKoller/projects/5

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
   - MCP Server für Cookidoo API Integration
   - Tools: Recipe Search, Recipe Details, Nutrition Info, Weekplan Management
   - Port: 3000

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
- `mcp` - cookidoo-mcp
- `shared` - cookidoo-assistant-shared
- `assistant-mcp` - cookidoo-assistant-mcp
- `api` - cookidoo-assistant-api

**Beispiele:**
```
feat(mcp): implement search_recipes MCP tool
fix(shared): resolve database connection pool exhaustion
docs: update README with new architecture
test(assistant-mcp): add unit tests for user profile service
refactor(api): extract middleware to separate modules
chore: update dependencies across all services
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

**Status:** 🚧 Noch nicht entschieden - siehe Issue #21

Nach Entscheidung in Issue #21 (Evaluate Cookidoo API Libraries):
- Entweder TypeScript/Node.js oder Python
- Issue #19 wird tech-stack-spezifische Instructions erstellen

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

- Node.js >= 18 (oder Python >= 3.11 nach Tech-Stack-Entscheidung)
- Docker & Docker Compose
- PostgreSQL (via Docker)
- Gültiges Cookidoo-Abo

### Setup

```bash
# Repository klonen
git clone https://github.com/TheRealKoller/cookidoo-assistant.git
cd cookidoo-assistant

# Dependencies installieren
npm install

# Environment Variables konfigurieren
cp cookidoo-mcp/.env.example cookidoo-mcp/.env
cp cookidoo-assistant-mcp/.env.example cookidoo-assistant-mcp/.env
cp cookidoo-assistant-api/.env.example cookidoo-assistant-api/.env
# .env Dateien mit echten Credentials befüllen

# Datenbank starten
docker-compose up -d postgres

# Services starten
npm run dev:mcp                  # Port 3000
npm run dev:assistant-mcp        # Port 3001
npm run dev:assistant-api        # Port 3002
```

## Weitere Informationen

- **Project Board**: https://github.com/users/TheRealKoller/projects/5
- **Issues Summary**: `.opencode/ISSUES_SUMMARY.md`
- **Service READMEs**: Jeder Service hat ein eigenes `README.md`
