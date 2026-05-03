# GitHub Workflow Skill

## Beschreibung
Dieser Skill unterstützt das Management von GitHub Issues, Project Boards und Pull Requests für das Cookidoo Assistant Monorepo.

## Kontext
- **Repository**: https://github.com/TheRealKoller/cookidoo-assistant (Monorepo)
- **Project Board**: https://github.com/users/TheRealKoller/projects/5
- **Archived Repository**: https://github.com/TheRealKoller/cookidoo-mcp (nicht mehr aktiv)

## Service Labels

Dieses Monorepo enthält 4 Services. Jedes Issue MUSS mit dem entsprechenden Service-Label versehen werden:

- `service:cookidoo-mcp` - cookidoo-mcp Service
- `service:shared` - cookidoo-assistant-shared Library
- `service:assistant-mcp` - cookidoo-assistant-mcp Service
- `service:api` - cookidoo-assistant-api Service

## Workflow-Schritte

### 1. Issue-Management

#### Neues Issue erstellen
```bash
# Issue mit Service-Label erstellen
gh issue create \
  --repo TheRealKoller/cookidoo-assistant \
  --title "TITLE" \
  --body "DESCRIPTION" \
  --label "service:cookidoo-mcp"

# Beispiel für Shared Library Issue
gh issue create \
  --repo TheRealKoller/cookidoo-assistant \
  --title "Add database migration helper" \
  --body "Implement migration helper for database updates" \
  --label "service:shared"
```

#### Issue zum Project Board hinzufügen (ZWINGEND ERFORDERLICH!)
```bash
# WICHTIG: JEDES neue Issue MUSS zum Project Board hinzugefügt werden!
# Issue-URL aus vorherigem Schritt verwenden
gh project item-add 5 --owner TheRealKoller --url https://github.com/TheRealKoller/cookidoo-assistant/issues/ISSUE_NUMBER

# Beispiel - direkt nach Issue-Erstellung:
ISSUE_URL=$(gh issue create \
  --repo TheRealKoller/cookidoo-assistant \
  --title "TITLE" \
  --body "DESCRIPTION" \
  --label "service:cookidoo-mcp" \
  --format json | jq -r '.url')
gh project item-add 5 --owner TheRealKoller --url "$ISSUE_URL"
```

**KRITISCH**: Ohne Hinzufügen zum Project Board sind Issues nicht im zentralen Board sichtbar!

#### Issues anzeigen
```bash
# Alle offenen Issues
gh issue list --repo TheRealKoller/cookidoo-assistant --state open

# Issues für einen bestimmten Service
gh issue list --repo TheRealKoller/cookidoo-assistant --label "service:cookidoo-mcp"

# Project Board Items anzeigen
gh project item-list 5 --owner TheRealKoller --format json
```

### 2. Branch-Workflow mit Issue-Verknüpfung

#### Feature-Branch von Issue erstellen
```bash
# Im Monorepo root
git checkout -b feature/ISSUE_NUMBER-description

# Beispiel
git checkout -b feature/24-implement-recipe-search
```

#### Branch pushen und Tracking setzen
```bash
git push -u origin feature/ISSUE_NUMBER-description
```

### 3. Pull Request Management

#### PR erstellen und mit Issue verknüpfen
```bash
# Im Monorepo root
gh pr create \
  --repo TheRealKoller/cookidoo-assistant \
  --title "[Service] Short description (#ISSUE_NUMBER)" \
  --body "Closes #ISSUE_NUMBER

## Services Affected
- service:cookidoo-mcp

## Änderungen
- Änderung 1
- Änderung 2

## Testing
- [ ] Tests hinzugefügt
- [ ] Manuelle Tests durchgeführt" \
  --assignee @me

# Beispiel
gh pr create \
  --repo TheRealKoller/cookidoo-assistant \
  --title "[cookidoo-mcp] Implement recipe search tool (#24)" \
  --body "Closes #24

## Services Affected
- service:cookidoo-mcp

## Changes
- Implemented search_recipes MCP tool
- Added unit tests
- Updated documentation" \
  --assignee @me
```

#### PR-Status prüfen
```bash
gh pr status --repo TheRealKoller/cookidoo-assistant
gh pr view PULL_NUMBER --repo TheRealKoller/cookidoo-assistant
```

#### PR-Checks ansehen
```bash
gh pr checks PULL_NUMBER --repo TheRealKoller/cookidoo-assistant
```

#### PR mergen
```bash
# Nach erfolgreicher Review
gh pr merge PULL_NUMBER --repo TheRealKoller/cookidoo-assistant --squash --delete-branch
```

### 4. Project Board Status aktualisieren

#### Issue-Status ändern
```bash
# Status-Optionen: "Todo", "In Progress", "Done"
gh project item-edit --id ITEM_ID --project-id 5 --owner TheRealKoller --field-id STATUS_FIELD_ID --text "In Progress"
```

## Best Practices

1. **Service-Labels**: Jedes Issue MUSS mit passendem `service:*` Label versehen werden
2. **Issue zum Project Board**: Jedes Issue MUSS zum Project Board (ID: 5) hinzugefügt werden
3. **Issue-Nummern in Branches**: Verwende Issue-Nummern im Branch-Namen
4. **PR mit Issue verknüpfen**: Nutze "Closes #ISSUE_NUMBER" im PR-Body
5. **Service-Präfix in PR-Titeln**: Format `[Service] Description (#ISSUE)`
6. **Project Board aktuell halten**: Aktualisiere den Status während der Arbeit

## Häufige Aufgaben

### Issue → Branch → PR → Merge Workflow
```bash
# 1. Issue mit Service-Label erstellen
ISSUE_URL=$(gh issue create --repo TheRealKoller/cookidoo-assistant \
  --title "Feature: XYZ" \
  --body "Beschreibung" \
  --label "service:cookidoo-mcp" \
  --format json | jq -r '.url')

# 2. Issue zum Project hinzufügen
gh project item-add 5 --owner TheRealKoller --url $ISSUE_URL

# 3. Branch erstellen (im Monorepo root)
ISSUE_NUMBER=$(echo $ISSUE_URL | grep -oP '\d+$')
git checkout -b feature/$ISSUE_NUMBER-xyz
git push -u origin feature/$ISSUE_NUMBER-xyz

# 4. Nach Implementation: PR erstellen
gh pr create \
  --repo TheRealKoller/cookidoo-assistant \
  --title "[cookidoo-mcp] Implement XYZ (#$ISSUE_NUMBER)" \
  --body "Closes #$ISSUE_NUMBER"

# 5. Nach erfolgreicher Review: Mergen
gh pr merge --repo TheRealKoller/cookidoo-assistant --squash --delete-branch
```

## Troubleshooting

### gh CLI nicht authentifiziert
```bash
gh auth login
```

### Project Board Zugriff fehlgeschlagen
```bash
# Project scope hinzufügen
gh auth refresh -s project
```

### Project Board Item-ID herausfinden
```bash
gh project item-list 5 --owner TheRealKoller --format json | jq '.items[] | select(.content.title | contains("ISSUE_TITLE"))'
```
