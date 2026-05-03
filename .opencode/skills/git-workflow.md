# Git Workflow Skill

## Beschreibung
Dieser Skill unterstützt lokale Git-Operationen für die Cookidoo-Unterprojekte, einschließlich Branch-Management, Commits und Synchronisation.

## Kontext
Arbeitet mit den lokalen Git-Repositories der Unterprojekte:
- `./cookidoo-mcp/`
- `./cookidoo-assistant/`

## Workflow-Schritte

### 1. Repository-Status prüfen

#### Aktuellen Status anzeigen
```bash
git status
git branch -vv  # Zeigt auch Remote-Tracking
```

#### Änderungen anzeigen
```bash
git diff          # Unstaged Änderungen
git diff --staged # Staged Änderungen
git log --oneline -n 10  # Letzte 10 Commits
```

### 2. Branch-Management

#### Neuen Branch erstellen
```bash
# Feature-Branch
git checkout -b feature/ISSUE_NUMBER-beschreibung

# Fix-Branch
git checkout -b fix/ISSUE_NUMBER-beschreibung

# Docs-Branch
git checkout -b docs/update-readme
```

#### Branch wechseln
```bash
git checkout main
git checkout feature/xyz
```

#### Remote-Branches anzeigen
```bash
git branch -r
git fetch --all  # Alle Remote-Branches aktualisieren
```

#### Branch löschen
```bash
# Lokal (nur wenn gemerged)
git branch -d feature/xyz

# Lokal (erzwingen)
git branch -D feature/xyz

# Remote
git push origin --delete feature/xyz
```

### 3. Änderungen committen

#### Standard-Workflow
```bash
# 1. Änderungen reviewen
git status
git diff

# 2. Dateien stagen
git add file1.ts file2.ts
# oder alle Änderungen
git add .

# 3. Commit mit Conventional Commits
git commit -m "feat: Add new feature"
git commit -m "fix: Resolve bug #123"
git commit -m "docs: Update README"
git commit -m "test: Add unit tests"
git commit -m "refactor: Improve code structure"
git commit -m "chore: Update dependencies"
```

#### Commit-Message Format
```
<type>: <kurze Beschreibung>

[optionaler Body mit Details]

[optionale Footer, z.B. "Closes #123"]
```

**Types:**
- `feat:` - Neue Funktionalität
- `fix:` - Bugfix
- `docs:` - Dokumentation
- `test:` - Tests
- `refactor:` - Code-Refactoring
- `style:` - Code-Formatierung
- `chore:` - Maintenance, Dependencies
- `ci:` - CI/CD Änderungen

#### Letzten Commit ändern
```bash
# Commit-Message ändern
git commit --amend -m "neue message"

# Weitere Dateien zum letzten Commit hinzufügen
git add forgotten-file.ts
git commit --amend --no-edit
```

### 4. Mit Remote synchronisieren

#### Änderungen pushen
```bash
# Erstmaliges Push mit Tracking
git push -u origin feature/xyz

# Nachfolgende Pushes
git push

# Force push (VORSICHT!)
git push --force-with-lease  # Sicherer als --force
```

#### Änderungen holen
```bash
# Fetch + Merge
git pull

# Nur fetchen (ohne merge)
git fetch origin

# Rebase statt Merge beim Pull
git pull --rebase
```

#### Mit main/master synchronisieren
```bash
# Vor dem Start: main aktualisieren
git checkout main
git pull origin main

# Feature-Branch mit main aktualisieren
git checkout feature/xyz
git merge main
# oder mit Rebase für saubere History
git rebase main
```

### 5. Stash-Management

#### Änderungen temporär speichern
```bash
# Stash erstellen
git stash push -m "WIP: Feature XYZ"

# Stash anzeigen
git stash list

# Stash anwenden (behält Stash)
git stash apply stash@{0}

# Stash anwenden und löschen
git stash pop

# Stash löschen
git stash drop stash@{0}
```

### 6. Konflikte lösen

#### Bei Merge-Konflikten
```bash
# 1. Status prüfen
git status

# 2. Konflikt-Dateien manuell bearbeiten
# Suche nach Conflict Markers: <<<<<<<, =======, >>>>>>>

# 3. Nach dem Lösen
git add resolved-file.ts
git commit  # Bei merge
git rebase --continue  # Bei rebase

# Abbrechen
git merge --abort  # Bei merge
git rebase --abort  # Bei rebase
```

### 7. History-Management

#### Interaktives Rebase (für saubere History)
```bash
# Letzte N Commits bearbeiten
git rebase -i HEAD~3

# Aktionen im Editor:
# pick   = Commit behalten
# reword = Commit-Message ändern
# edit   = Commit bearbeiten
# squash = Mit vorherigem Commit zusammenführen
# drop   = Commit entfernen
```

#### Commit-History anzeigen
```bash
# Kompakte Ansicht
git log --oneline --graph --all

# Mit Änderungsstatistik
git log --stat

# Nur eigene Commits
git log --author="$(git config user.name)"

# Commits zwischen Branches
git log main..feature/xyz
```

### 8. Remote-Repository Management

#### Remote-Status prüfen
```bash
git remote -v
git remote show origin
```

#### Remote-URL ändern
```bash
git remote set-url origin https://github.com/TheRealKoller/cookidoo-mcp.git
```

## Best Practices

1. **Häufig committen**: Kleine, logische Commits sind besser als große
2. **Aussagekräftige Messages**: Folge Conventional Commits
3. **Vor Push testen**: Stelle sicher, dass der Code funktioniert
4. **Branch aktuell halten**: Merge/Rebase regelmäßig von main
5. **Force Push vermeiden**: Nutze `--force-with-lease` wenn nötig
6. **Keine Secrets committen**: Prüfe vor dem Commit
7. **Feature-Branches kurz halten**: Merge zeitnah

## Typische Workflows

### Feature entwickeln
```bash
# 1. Main aktualisieren
git checkout main
git pull

# 2. Feature-Branch erstellen
git checkout -b feature/42-neue-funktion

# 3. Entwickeln und committen
git add .
git commit -m "feat: Implement neue Funktion"

# 4. Pushen
git push -u origin feature/42-neue-funktion

# 5. PR erstellen (siehe github-workflow.md)
```

### Hotfix
```bash
# 1. Von main starten
git checkout main
git pull

# 2. Fix-Branch erstellen
git checkout -b fix/urgent-bug

# 3. Fix implementieren
git add .
git commit -m "fix: Resolve critical bug"

# 4. Sofort pushen und PR erstellen
git push -u origin fix/urgent-bug
```

### Nach PR-Merge aufräumen
```bash
# 1. Zu main wechseln
git checkout main

# 2. Aktualisieren
git pull

# 3. Lokalen Feature-Branch löschen
git branch -d feature/42-neue-funktion

# 4. Prüfen ob Remote-Branch gelöscht wurde
git fetch --prune
```

## Troubleshooting

### Änderungen verwerfen
```bash
# Unstaged Änderungen verwerfen
git restore file.ts
git restore .  # Alle Dateien

# Staged Änderungen unstagen
git restore --staged file.ts

# Alle Änderungen verwerfen (VORSICHTIG!)
git reset --hard HEAD
```

### Commit rückgängig machen
```bash
# Letzten Commit rückgängig (Änderungen bleiben)
git reset --soft HEAD~1

# Letzten Commit rückgängig (Änderungen verwerfen)
git reset --hard HEAD~1

# Commit mit neuem Commit rückgängig machen (sicher für gepushte Commits)
git revert HEAD
```

### Falscher Branch
```bash
# Commits auf anderen Branch verschieben
git log  # Commit-Hash notieren
git checkout richtiger-branch
git cherry-pick COMMIT_HASH
git checkout falscher-branch
git reset --hard HEAD~1  # Commit entfernen
```

### Repository-Status zurücksetzen
```bash
# Alle lokalen Änderungen verwerfen
git reset --hard origin/main

# Untracked Files entfernen
git clean -fd
```
