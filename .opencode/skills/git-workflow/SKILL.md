---
name: git-workflow
description: Local Git operations including branch management, commits, and synchronization
---

# Git Workflow

Lokale Git-Operationen für Cookidoo-Unterprojekte.

## Quick Commands

### Status & Diff
```bash
git status
git diff              # Unstaged
git diff --staged     # Staged
git log --oneline -n 10
```

### Branches
```bash
# Erstellen & Wechseln
git checkout -b feature/ISSUE_NUMBER-desc
git checkout -b fix/ISSUE_NUMBER-desc

# Remote Branches
git fetch --all
git branch -r

# Löschen
git branch -d feature/xyz           # Lokal
git push origin --delete feature/xyz # Remote
```

### Commits
```bash
# Standard
git add .
git commit -m "feat: Add feature"

# Conventional Commits Types:
# feat, fix, docs, test, refactor, style, chore, ci

# Amend letzten Commit
git commit --amend -m "new message"
git add file && git commit --amend --no-edit
```

### Sync mit Remote
```bash
# Push
git push -u origin feature/xyz  # Erstmalig
git push                        # Nachfolgend
git push --force-with-lease     # Force (sicherer)

# Pull
git pull                # Fetch + Merge
git pull --rebase       # Fetch + Rebase
git fetch origin        # Nur fetchen

# Mit main synchronisieren
git checkout main && git pull
git checkout feature/xyz
git merge main          # oder: git rebase main
```

### Stash
```bash
git stash push -m "WIP: xyz"
git stash list
git stash pop           # Apply + delete
git stash apply stash@{0}
git stash drop stash@{0}
```

### Konflikte
```bash
# Nach Konflikt
git status              # Konflikt-Dateien anzeigen
# Manuell bearbeiten (<<<<<<< ======= >>>>>>>)
git add resolved-file.ts
git commit              # Bei merge
git rebase --continue   # Bei rebase

# Abbrechen
git merge --abort
git rebase --abort
```

## Workflows

### Feature entwickeln
```bash
git checkout main && git pull
git checkout -b feature/42-xyz
# ... entwickeln ...
git add . && git commit -m "feat: xyz"
git push -u origin feature/42-xyz
# PR erstellen (siehe github-workflow)
```

### Nach PR-Merge
```bash
git checkout main && git pull
git branch -d feature/42-xyz
git fetch --prune
```

### Hotfix
```bash
git checkout main && git pull
git checkout -b fix/urgent
git add . && git commit -m "fix: critical bug"
git push -u origin fix/urgent
```

## History

### Rebase (saubere History)
```bash
# Letzte N Commits bearbeiten
git rebase -i HEAD~3
# pick/reword/edit/squash/drop im Editor
```

### Log
```bash
git log --oneline --graph --all
git log --stat
git log main..feature/xyz
```

## Troubleshooting

### Änderungen verwerfen
```bash
git restore file.ts         # Unstaged
git restore --staged file.ts # Unstage
git reset --hard HEAD       # Alles (VORSICHT!)
git clean -fd               # Untracked files
```

### Commit rückgängig
```bash
git reset --soft HEAD~1     # Änderungen bleiben
git reset --hard HEAD~1     # Änderungen weg
git revert HEAD             # Neuer Revert-Commit (sicher)
```

### Falscher Branch
```bash
git log                     # Hash notieren
git checkout correct-branch
git cherry-pick HASH
git checkout wrong-branch
git reset --hard HEAD~1
```

### Reset zu Remote
```bash
git reset --hard origin/main
git clean -fd
```

## Best Practices

1. Kleine, logische Commits
2. Conventional Commits Format
3. Vor Push testen
4. Branch aktuell halten (merge/rebase von main)
5. `--force-with-lease` statt `--force`
6. Keine Secrets committen
7. Feature-Branches zeitnah mergen
