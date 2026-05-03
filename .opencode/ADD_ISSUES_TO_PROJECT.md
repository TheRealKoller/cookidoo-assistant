# Issues zum Project Board hinzufügen

## Problem
Die 29 erstellten Issues wurden **nicht automatisch** zum zentralen Project Board hinzugefügt, weil die GitHub CLI nicht die erforderlichen Berechtigungen hatte.

## Lösung

### Schritt 1: GitHub CLI Berechtigungen erweitern

Führe folgenden Befehl aus:

```bash
gh auth refresh -s project
```

Du wirst durch einen interaktiven OAuth-Flow geleitet, um die `project` Berechtigung hinzuzufügen.

### Schritt 2: Issues zum Project Board hinzufügen

#### Option A: Automatisches Script (Empfohlen)

Führe das bereitgestellte Script aus:

```bash
cd /home/thekoller/projekte/cookidoo-assistant
./.opencode/add-issues-to-project.sh
```

Das Script fügt alle 29 Issues automatisch zum Project Board hinzu.

#### Option B: Manuell

Falls das Script nicht funktioniert, kannst du die Issues manuell hinzufügen:

```bash
# cookidoo-mcp Issues (1-11)
for i in {1..11}; do
  gh project item-add 5 --owner TheRealKoller --url "https://github.com/TheRealKoller/cookidoo-mcp/issues/$i"
done

# cookidoo-assistant Issues (1-18)
for i in {1..18}; do
  gh project item-add 5 --owner TheRealKoller --url "https://github.com/TheRealKoller/cookidoo-assistant/issues/$i"
done
```

### Schritt 3: Verifizieren

Öffne das Project Board und prüfe, ob alle Issues vorhanden sind:
https://github.com/users/TheRealKoller/projects/5

Du solltest **29 Issues** sehen:
- 11 von cookidoo-mcp
- 18 von cookidoo-assistant

## Was wurde geändert?

Ich habe die Instructions und Skills aktualisiert, damit dies in Zukunft nicht mehr passiert:

### 1. `.opencode/instructions.md`
- Klargestellt, dass Issues IMMER zum Project Board hinzugefügt werden müssen
- Project Board URL und ID dokumentiert
- Workflow aktualisiert

### 2. `.opencode/skills/github-workflow.md`
- Workflow für Issue-Erstellung erweitert
- Automatisches Hinzufügen zum Project Board eingebaut
- Best Practices aktualisiert
- Beispiel mit `jq` für direktes Hinzufügen nach Erstellung

### 3. `.opencode/add-issues-to-project.sh`
- Script zum nachträglichen Hinzufügen aller Issues
- Prüft automatisch auf erforderliche Berechtigungen
- Gibt klare Fehlermeldungen

## Zukünftige Issue-Erstellung

In Zukunft sollten Issues so erstellt werden:

```bash
# Issue erstellen und direkt zum Project Board hinzufügen
ISSUE_URL=$(gh issue create \
  --repo TheRealKoller/cookidoo-mcp \
  --title "TITLE" \
  --body "DESCRIPTION" \
  --format json | jq -r '.url')

gh project item-add 5 --owner TheRealKoller --url "$ISSUE_URL"
```

Oder als One-Liner:

```bash
gh issue create --repo TheRealKoller/cookidoo-mcp --title "TITLE" --body "DESCRIPTION" && \
gh project item-add 5 --owner TheRealKoller --url "$(gh issue list --repo TheRealKoller/cookidoo-mcp --limit 1 --json url --jq '.[0].url')"
```

## Warum ist das wichtig?

Das zentrale Project Board ist der **Single Source of Truth** für alle Tasks im Cookidoo-Projekt. Ohne Issues im Board:
- ❌ Keine zentrale Übersicht über alle Tasks
- ❌ Keine Priorisierung möglich
- ❌ Keine Sprint-Planung möglich
- ❌ Schwierig, Fortschritt zu tracken

Mit Issues im Board:
- ✅ Zentrale Übersicht über beide Repositories
- ✅ Einfache Priorisierung und Planung
- ✅ Klare Übersicht über offene, laufende und erledigte Tasks
- ✅ Bessere Zusammenarbeit möglich
