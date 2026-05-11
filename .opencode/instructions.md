# Cookidoo Assistant - Instructions

## Projekt-Übersicht

Dieses Monorepo enthält die komplette Cookidoo Assistant Platform - ein AI-powered Meal Planning System basierend auf Cookidoo Rezepten mit MCP Servern und REST API.

### Repository

- **GitHub Repository**: https://github.com/TheRealKoller/cookidoo-assistant
- **Project Board**: https://github.com/users/TheRealKoller/projects/5

## Services

Dieses Repository ist als **Monorepo** organisiert und enthält 4 Services:

1. **cookidoo-mcp** (`service:cookidoo-mcp`)
   - Python 3.11+ MCP Server für Cookidoo API Integration
   - Port: 3000
   - Library: `cookidoo-api==0.17.0`

2. **cookidoo-assistant-shared** (`service:shared`)
   - Shared Library für alle Services
   - Database Models, Repositories, Business Logic

3. **cookidoo-assistant-mcp** (`service:assistant-mcp`)
   - TypeScript MCP Server für User Data Management
   - Port: 3001
   - PostgreSQL für Datenpersistenz

4. **cookidoo-assistant-api** (`service:api`)
   - TypeScript REST API für zukünftige Web/Mobile UI
   - Port: 3002

## Arbeitsweise

### Allgemeine Regeln

1. **Tests schreiben und ausführen**: Für jede neue Funktionalität müssen Tests geschrieben und erfolgreich ausgeführt werden
2. **Code lesbar halten**: Schreibe klaren, selbsterklärenden Code - minimale zusätzliche Dokumentation sollte ausreichen
3. **Niemals ohne Bestätigung auf main pushen**: Außer bei expliziter Erlaubnis IMMER den PR-Workflow verwenden

### Issue-Workflow

Wenn ein Issue bearbeitet wird, folge diesem Ablauf:

#### 1. Issue-Status setzen
```bash
gh issue edit ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant
# Status auf Project Board auf "In Progress" setzen
```

#### 2. Feature-Branch erstellen
```bash
git checkout main
git pull origin main
git checkout -b ISSUE_NUMBER-short-description
git push -u origin ISSUE_NUMBER-short-description
```

**Branch-Naming Konventionen:**
- `ISSUE_NUMBER-short-description` (z.B. `21-implement-recipe-search-tool`)

#### 3. Implementierung durchführen
- Code schreiben
- **Tests schreiben** (ZWINGEND!)
- Commits mit Conventional Commits (siehe unten)

#### 4. Qualitätsprüfung
```bash
# Python (cookidoo-mcp)
cd cookidoo-mcp
ruff format . && ruff check . && mypy . && pytest

# TypeScript Services
npm run lint && npm run format:check && npm run type-check && npm test
```

#### 5. Pull Request erstellen
```bash
gh pr create \
  --repo TheRealKoller/cookidoo-assistant \
  --base main \
  --head ISSUE_NUMBER-short-description \
  --title "[Service] Short description" \
  --body "$(cat <<'EOF'
Closes #ISSUE_NUMBER

## Services Affected
- service:X

## Changes
- Change 1
- Change 2

## Testing
- [x] Lint passed
- [x] Format passed
- [x] Type check passed
- [x] Tests passed
EOF
)"
```

#### 6. Issue-Status auf "In Review" setzen und User informieren
```
✅ Pull Request erstellt: [PR-URL]

Bitte review das PR. Wenn alles passt, kann es gemergt werden.
```

### Service-Labels für Issues

Beim Erstellen oder Bearbeiten von Issues **immer** den passenden Service-Label hinzufügen:

- `service:cookidoo-mcp` - cookidoo-mcp Service
- `service:shared` - Shared Library
- `service:assistant-mcp` - cookidoo-assistant-mcp Service
- `service:api` - cookidoo-assistant-api Service

### Commit-Messages

Folge der [Conventional Commits](https://www.conventionalcommits.org/) Spezifikation:

**Format:** `<type>(<scope>): <description>`

**Types:**
- `feat(service):` - Neue Features
- `fix(service):` - Bugfixes
- `docs:` - Dokumentationsänderungen
- `test(service):` - Test-Änderungen
- `refactor(service):` - Code-Refactoring
- `chore:` - Maintenance (Dependencies, Config, etc.)
- `ci:` - CI/CD Änderungen

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
ci: remove nightly E2E test runs
```

## Workspace Commands

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

## Weitere Informationen

- **Project Board**: https://github.com/users/TheRealKoller/projects/5
- **Service READMEs**: Jeder Service hat ein eigenes `README.md`
