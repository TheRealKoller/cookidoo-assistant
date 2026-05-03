# Cookidoo Project - Instructions

## Projekt-Übersicht

Dieses Verzeichnis verwaltet mehrere zusammenhängende Unterprojekte rund um Cookidoo:

### Unterprojekte

1. **cookidoo-mcp**
   - Repository: https://github.com/TheRealKoller/cookidoo-mcp
   - Verzeichnis: `./cookidoo-mcp/`
   - Beschreibung: Model Context Protocol Server für Cookidoo-Integration

2. **cookidoo-assistant**
   - Repository: https://github.com/TheRealKoller/cookidoo-assistant
   - Verzeichnis: `./cookidoo-assistant/`
   - Beschreibung: Assistant-Anwendung für Cookidoo

### Zentrale Ressourcen

- **GitHub Project Board**: https://github.com/users/TheRealKoller/projects/5
  - Alle Issues/Tickets werden zentral hier verwaltet
  - Issues sind mit den jeweiligen Repositories verknüpft

## Arbeitsweise

### Projekt-Kontext wechseln

Wenn du an einem spezifischen Unterprojekt arbeitest, wechsle in das entsprechende Verzeichnis:
```bash
cd cookidoo-mcp     # für MCP Server
cd cookidoo-assistant   # für Assistant
```

### GitHub Integration

Alle GitHub-Operationen sollten über die bereitgestellten Skills erfolgen:
- `/github-workflow` - Für Issue-, Branch- und PR-Management
- `/git-workflow` - Für lokale Git-Operationen

**WICHTIG**: Alle erstellten Issues MÜSSEN automatisch zum zentralen Project Board hinzugefügt werden:
- Project Board URL: https://github.com/users/TheRealKoller/projects/5
- Project ID: 5
- Owner: TheRealKoller
- Nach jedem `gh issue create` muss `gh project item-add` aufgerufen werden

### Entwicklungs-Workflow

1. Issue erstellen UND zum Project Board hinzufügen
2. Issue aus dem Project Board auswählen
3. Feature-Branch im entsprechenden Repository erstellen
4. Änderungen implementieren und testen
5. Pull Request erstellen
6. Issue mit PR verknüpfen

## Verfügbare Skills

- **github-workflow**: GitHub Issues, Project Board, Pull Requests
- **git-workflow**: Branch-Management, Commits, Push/Pull
- **test-and-build**: Testing und CI/CD-Prozesse

## Projekt-Standards

### Branch-Naming
- `feature/` - Neue Features
- `fix/` - Bugfixes
- `docs/` - Dokumentation
- `refactor/` - Code-Refactoring

### Commit-Messages
Folge der Conventional Commits Spezifikation:
- `feat:` - Neue Features
- `fix:` - Bugfixes
- `docs:` - Dokumentationsänderungen
- `test:` - Test-Änderungen
- `refactor:` - Code-Refactoring
- `chore:` - Maintenance-Aufgaben

### Pull Requests
- Verknüpfe PRs immer mit dem entsprechenden Issue
- Füge aussagekräftige Beschreibungen hinzu
- Stelle sicher, dass alle Tests durchlaufen
