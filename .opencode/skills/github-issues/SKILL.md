---
name: github-issues
description: Create, edit, and manage GitHub Issues with gh CLI including permission handling
---

# GitHub Issues Management

Kompakter Workflow für GitHub Issues mit gh CLI.

**WICHTIG**: Bei fehlenden Berechtigungen User um Autorisierung bitten!

## ⚠️ PFLICHT-CHECKLISTE beim Issue-Erstellen

Jedes Issue MUSS diese Schritte durchlaufen:

- [ ] Issue mit `gh issue create` erstellen
- [ ] **ZWINGEND**: Issue zum Project Board hinzufügen mit `gh project item-add 5 --owner TheRealKoller --url "$ISSUE_URL"`
- [ ] Mindestens ein Service-Label setzen (`service:cookidoo-mcp`, `service:shared`, `service:assistant-mcp`, `service:api`)

**Empfohlen**: Nutze den kombinierten Command (siehe unten) um beide Schritte in einem durchzuführen!

## Repository-Kontext
- **Repo**: TheRealKoller/cookidoo-assistant
- **Project Board**: https://github.com/users/TheRealKoller/projects/5 (Project ID: 5)
- **Service Labels**: `service:cookidoo-mcp`, `service:shared`, `service:assistant-mcp`, `service:api`

## Issues erstellen

### ✅ EMPFOHLENE METHODE: Issue + Project Board in einem Command
```bash
ISSUE_URL=$(gh issue create \
  --repo TheRealKoller/cookidoo-assistant \
  --title "TITLE" \
  --body "DESCRIPTION" \
  --label "service:SERVICE" \
  --format json | jq -r '.url') && \
gh project item-add 5 --owner TheRealKoller --url "$ISSUE_URL"
```

**Wichtig**: Der `&&` Operator stellt sicher, dass das Issue nur zum Board hinzugefügt wird, wenn die Erstellung erfolgreich war.

### ⚠️ NUR in Ausnahmefällen: Issue ohne Project Board
```bash
# ACHTUNG: Issue wird NICHT im Project Board sichtbar sein!
# Danach MANUELL zum Board hinzufügen (siehe unten)
gh issue create \
  --repo TheRealKoller/cookidoo-assistant \
  --title "TITLE" \
  --body "DESCRIPTION" \
  --label "service:SERVICE"
```

### Interaktiv
```bash
gh issue create --repo TheRealKoller/cookidoo-assistant --web
```

## Issues anzeigen

```bash
# Alle offenen Issues
gh issue list --repo TheRealKoller/cookidoo-assistant

# Nach Service filtern
gh issue list --repo TheRealKoller/cookidoo-assistant --label "service:cookidoo-mcp"

# Nach Status filtern
gh issue list --repo TheRealKoller/cookidoo-assistant --state open
gh issue list --repo TheRealKoller/cookidoo-assistant --state closed

# Eigene Issues
gh issue list --repo TheRealKoller/cookidoo-assistant --assignee @me

# Details anzeigen
gh issue view ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant
```

## Issues bearbeiten

### Titel ändern
```bash
gh issue edit ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant --title "NEW_TITLE"
```

### Body ändern
```bash
gh issue edit ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant --body "NEW_DESCRIPTION"
```

### Labels verwalten
```bash
# Label hinzufügen
gh issue edit ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant --add-label "bug"

# Label entfernen
gh issue edit ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant --remove-label "bug"
```

### Assignee setzen
```bash
gh issue edit ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant --add-assignee @me
gh issue edit ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant --add-assignee USERNAME
```

### Milestone setzen
```bash
gh issue edit ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant --milestone "v1.0"
```

## Issues schließen/öffnen

```bash
# Schließen
gh issue close ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant

# Mit Kommentar
gh issue close ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant --comment "Fixed in PR #123"

# Wieder öffnen
gh issue reopen ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant
```

## Kommentare

```bash
# Kommentar hinzufügen
gh issue comment ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant --body "COMMENT"

# Kommentar bearbeiten
gh issue comment ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant --edit

# Interaktiv im Browser
gh issue comment ISSUE_NUMBER --repo TheRealKoller/cookidoo-assistant --web
```

## Project Board

### Issue zum Board hinzufügen
```bash
gh project item-add 5 \
  --owner TheRealKoller \
  --url https://github.com/TheRealKoller/cookidoo-assistant/issues/NUMBER
```

### Board Items anzeigen
```bash
gh project item-list 5 --owner TheRealKoller --format json
```

## Berechtigungs-Management

### Authentifizierung prüfen
```bash
gh auth status
```

### Bei fehlenden Berechtigungen

**Symptom**: Error "Not Found" oder "Forbidden"

**Lösung für User**:
```bash
# Schritt 1: Re-Authentifizierung mit erweiterten Scopes
gh auth login --scopes repo,project

# Schritt 2: Oder refresh mit project scope
gh auth refresh -s project

# Schritt 3: Status prüfen
gh auth status
```

**Wenn Project Board Zugriff fehlt**:
```bash
gh auth refresh -s project
```

**User-Anweisung Template**:
```
⚠️ Fehlende GitHub-Berechtigung!

Bitte führe folgenden Befehl aus:
  gh auth refresh -s project

Das gibt mir Zugriff auf dein Project Board.

Alternativ komplett neu authentifizieren:
  gh auth login --scopes repo,project

Nach der Authentifizierung versuche ich es erneut.
```

## Batch-Operationen

### Mehrere Issues erstellen
```bash
# Mit Loop
for title in "Issue 1" "Issue 2" "Issue 3"; do
  gh issue create \
    --repo TheRealKoller/cookidoo-assistant \
    --title "$title" \
    --label "service:shared"
done
```

### Labels zu mehreren Issues
```bash
# Alle offenen Issues mit Label versehen
gh issue list --repo TheRealKoller/cookidoo-assistant --state open --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --repo TheRealKoller/cookidoo-assistant --add-label "needs-review"
```

## Templates

```bash
# Bug Report
gh issue create --repo TheRealKoller/cookidoo-assistant \
  --title "[BUG] Title" \
  --body "Beschreibung + Schritte + Service" \
  --label "bug,service:SERVICE"

# Feature Request
gh issue create --repo TheRealKoller/cookidoo-assistant \
  --title "[FEATURE] Title" \
  --body "Beschreibung + Motivation + Service" \
  --label "enhancement,service:SERVICE"
```

## Troubleshooting

```bash
# gh nicht installiert
brew install gh  # macOS
sudo apt install gh  # Linux

# Auth fehlgeschlagen
gh auth login

# Issue nicht gefunden
gh issue list --repo TheRealKoller/cookidoo-assistant --search "TERM"

# Item-ID finden
gh project item-list 5 --owner TheRealKoller --format json | \
  jq '.items[] | select(.content.title | contains("TITLE"))'
```

## Best Practices

1. **Service-Label setzen**: Jedes Issue MUSS ein `service:*` Label haben
2. **Project Board**: Neue Issues IMMER zum Board hinzufügen
3. **Permissions prüfen**: Bei Fehlern zuerst `gh auth status` checken
4. **Klare Titel**: Format `[TYPE] Short description`
5. **Detaillierte Beschreibung**: Nutze Templates für Konsistenz

## Quick Commands

```bash
# Issue erstellen + zum Board
ISSUE_URL=$(gh issue create --repo TheRealKoller/cookidoo-assistant \
  --title "Title" --body "Description" --label "service:shared" \
  --format json | jq -r '.url') && \
gh project item-add 5 --owner TheRealKoller --url "$ISSUE_URL"

# Issue Status ändern
gh issue edit NUMBER --repo TheRealKoller/cookidoo-assistant --add-label "in-progress"

# Issue schließen mit Verweis
gh issue close NUMBER --repo TheRealKoller/cookidoo-assistant --comment "Closed by #PR_NUMBER"
```
