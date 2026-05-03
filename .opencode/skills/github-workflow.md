# GitHub Workflow Skill

## Beschreibung
Dieser Skill unterstützt das Management von GitHub Issues, Project Boards und Pull Requests für die Cookidoo-Unterprojekte.

## Kontext
- **Project Board**: https://github.com/users/TheRealKoller/projects/5
- **Repositories**:
  - cookidoo-mcp: https://github.com/TheRealKoller/cookidoo-mcp
  - cookidoo-assistant: https://github.com/TheRealKoller/cookidoo-assistant

## Workflow-Schritte

### 1. Issue-Management

#### Neues Issue erstellen
```bash
# Für cookidoo-mcp
gh issue create --repo TheRealKoller/cookidoo-mcp --title "TITLE" --body "DESCRIPTION"

# Für cookidoo-assistant
gh issue create --repo TheRealKoller/cookidoo-assistant --title "TITLE" --body "DESCRIPTION"
```

#### Issue zum Project Board hinzufügen (ZWINGEND ERFORDERLICH!)
```bash
# WICHTIG: JEDES neue Issue MUSS zum Project Board hinzugefügt werden!
# Issue-URL aus vorherigem Schritt verwenden
gh project item-add 5 --owner TheRealKoller --url https://github.com/TheRealKoller/REPO/issues/ISSUE_NUMBER

# Beispiel - direkt nach Issue-Erstellung:
ISSUE_URL=$(gh issue create --repo TheRealKoller/cookidoo-mcp --title "TITLE" --body "DESCRIPTION" --format json | jq -r '.url')
gh project item-add 5 --owner TheRealKoller --url "$ISSUE_URL"
```

**KRITISCH**: Ohne Hinzufügen zum Project Board sind Issues nicht im zentralen Board sichtbar!

#### Issues anzeigen
```bash
# Alle offenen Issues für ein Projekt
gh issue list --repo TheRealKoller/cookidoo-mcp --state open

# Project Board Items anzeigen
gh project item-list 5 --owner TheRealKoller --format json
```

### 2. Branch-Workflow mit Issue-Verknüpfung

#### Feature-Branch von Issue erstellen
```bash
# Aktuelles Unterprojekt-Verzeichnis muss aktiv sein!
# Branch-Name sollte Issue-Nummer enthalten
git checkout -b feature/ISSUE_NUMBER-beschreibung
```

#### Branch pushen und Tracking setzen
```bash
git push -u origin feature/ISSUE_NUMBER-beschreibung
```

### 3. Pull Request Management

#### PR erstellen und mit Issue verknüpfen
```bash
# Im entsprechenden Unterprojekt-Verzeichnis
gh pr create \
  --title "feat: Beschreibung" \
  --body "Closes #ISSUE_NUMBER

## Änderungen
- Änderung 1
- Änderung 2

## Testing
- [ ] Tests hinzugefügt
- [ ] Manuelle Tests durchgeführt" \
  --assignee @me
```

#### PR-Status prüfen
```bash
gh pr status
gh pr view PULL_NUMBER
```

#### PR-Checks ansehen
```bash
gh pr checks PULL_NUMBER
```

#### PR mergen
```bash
# Nach erfolgreicher Review
gh pr merge PULL_NUMBER --squash --delete-branch
```

### 4. Project Board Status aktualisieren

#### Issue-Status ändern
```bash
# Status-Optionen: "Todo", "In Progress", "Done"
gh project item-edit --id ITEM_ID --project-id 5 --owner TheRealKoller --field-id STATUS_FIELD_ID --text "In Progress"
```

## Best Practices

1. **Issue erstellen UND zum Project Board hinzufügen**: Jedes Issue MUSS zum zentralen Project Board (ID: 5) hinzugefügt werden
2. **Issue-Nummern in Branches**: Verwende Issue-Nummern im Branch-Namen für bessere Nachvollziehbarkeit
3. **PR mit Issue verknüpfen**: Nutze "Closes #ISSUE_NUMBER" im PR-Body
4. **Project Board aktuell halten**: Aktualisiere den Status im Project Board während der Arbeit
5. **Kontext prüfen**: Stelle sicher, dass du im richtigen Unterprojekt-Verzeichnis bist

## Häufige Aufgaben

### Issue → Branch → PR → Merge Workflow
```bash
# 1. Issue erstellen
ISSUE_URL=$(gh issue create --repo TheRealKoller/cookidoo-mcp \
  --title "Feature: XYZ" \
  --body "Beschreibung" \
  --format json | jq -r '.url')

# 2. Issue zum Project hinzufügen
gh project item-add 5 --owner TheRealKoller --url $ISSUE_URL

# 3. Branch erstellen (im Unterprojekt-Verzeichnis)
cd cookidoo-mcp
ISSUE_NUMBER=$(echo $ISSUE_URL | grep -oP '\d+$')
git checkout -b feature/$ISSUE_NUMBER-xyz
git push -u origin feature/$ISSUE_NUMBER-xyz

# 4. Nach Implementation: PR erstellen
gh pr create --title "feat: XYZ" --body "Closes #$ISSUE_NUMBER"

# 5. Nach erfolgreicher Review: Mergen
gh pr merge --squash --delete-branch
```

## Troubleshooting

### gh CLI nicht authentifiziert
```bash
gh auth login
```

### Falsches Repository
Prüfe, ob du im richtigen Unterprojekt-Verzeichnis bist:
```bash
pwd
git remote -v
```

### Project Board Item-ID herausfinden
```bash
gh project item-list 5 --owner TheRealKoller --format json | jq '.items[] | select(.content.title | contains("ISSUE_TITLE"))'
```
