# Cookidoo Project - Konfiguration

## Verzeichnisstruktur

```
cookidoo-assistant/              # Root-Verzeichnis (aktuell)
├── .opencode/                   # Zentrale OpenCode-Konfiguration
│   ├── instructions.md          # Projekt-Übersicht und Standards
│   └── skills/                  # Workflow-Skills
│       ├── github-workflow.md   # GitHub Issues, PRs, Project Board
│       ├── git-workflow.md      # Git-Operationen
│       └── test-and-build.md    # Testing, Linting, Build
├── cookidoo-mcp/                # MCP Server Unterprojekt
│   ├── .git/                    # Git Repository
│   ├── src/
│   ├── package.json
│   └── ...
└── cookidoo-assistant/          # Assistant Unterprojekt
    ├── .git/                    # Git Repository
    ├── src/
    ├── package.json
    └── ...
```

## GitHub-Ressourcen

### Zentrale Ressourcen
- **Project Board**: https://github.com/users/TheRealKoller/projects/5
  - Zentrale Verwaltung aller Issues/Tickets
  - Issues sind mit den jeweiligen Repositories verknüpft

### Repositories

#### cookidoo-mcp
- **URL**: https://github.com/TheRealKoller/cookidoo-mcp
- **Beschreibung**: Model Context Protocol Server für Cookidoo
- **Lokaler Pfad**: `./cookidoo-mcp/`

#### cookidoo-assistant
- **URL**: https://github.com/TheRealKoller/cookidoo-assistant
- **Beschreibung**: Assistant-Anwendung für Cookidoo
- **Lokaler Pfad**: `./cookidoo-assistant/`

## Skills laden

Die Skills können über OpenCode geladen werden:

```bash
# Im OpenCode CLI
/load-skill github-workflow  # GitHub-Operationen
/load-skill git-workflow     # Git-Operationen
/load-skill test-and-build   # Testing & Build
```

Oder direkt referenzieren:
- Skills befinden sich in `.opencode/skills/`
- Instructions in `.opencode/instructions.md`

## Arbeiten mit Unterprojekten

### Kontext wechseln
```bash
# In cookidoo-mcp arbeiten
cd cookidoo-mcp

# In cookidoo-assistant arbeiten
cd cookidoo-assistant

# Zurück zum Root
cd ..
```

### Git-Status aller Projekte prüfen
```bash
# Im Root-Verzeichnis
for dir in cookidoo-*; do
  if [ -d "$dir/.git" ]; then
    echo "=== $dir ==="
    cd "$dir"
    git status -s
    git branch --show-current
    cd ..
    echo
  fi
done
```

## Setup für neue Unterprojekte

Falls ein neues Unterprojekt hinzugefügt wird:

1. **Repository klonen**:
   ```bash
   git clone https://github.com/TheRealKoller/PROJEKT-NAME.git
   ```

2. **Instructions aktualisieren**:
   - `.opencode/instructions.md` → Unterprojekt-Liste erweitern

3. **GitHub Project konfigurieren**:
   - Issues automatisch zum Project Board hinzufügen

## Empfohlene Tools

### GitHub CLI (gh)
```bash
# Installation prüfen
gh --version

# Authentifizierung
gh auth status
gh auth login  # Falls nicht authentifiziert
```

### Git
```bash
# Konfiguration prüfen
git config --list

# User konfigurieren (falls nötig)
git config --global user.name "Dein Name"
git config --global user.email "deine@email.com"
```

### Node.js & npm
```bash
# Versionen prüfen
node --version
npm --version

# Empfohlen: Node.js 18.x oder 20.x
```

## Workflow-Integration

### Typischer Entwicklungs-Workflow

1. **Issue erstellen und zum Project Board hinzufügen**
   - Skill: `github-workflow.md`
   
2. **Feature-Branch erstellen**
   - Skill: `git-workflow.md`

3. **Entwicklung mit Tests**
   - Skill: `test-and-build.md`

4. **Commits mit Conventional Commits**
   - Skill: `git-workflow.md`

5. **Pull Request erstellen**
   - Skill: `github-workflow.md`

6. **Nach Merge: Branch aufräumen**
   - Skill: `git-workflow.md`

## Best Practices

### Branch-Naming Convention
```
feature/ISSUE_NUMBER-kurze-beschreibung
fix/ISSUE_NUMBER-bug-beschreibung
docs/update-readme
refactor/improve-performance
```

### Commit-Message Convention
```
<type>: <description>

[optional body]

[optional footer, z.B. "Closes #123"]
```

**Types:**
- `feat:` - Neue Features
- `fix:` - Bugfixes
- `docs:` - Dokumentation
- `test:` - Tests
- `refactor:` - Refactoring
- `chore:` - Maintenance

### Pull Request Template

Empfohlene PR-Beschreibung:
```markdown
## Beschreibung
Kurze Zusammenfassung der Änderungen

## Änderungen
- Änderung 1
- Änderung 2

## Testing
- [ ] Unit Tests hinzugefügt
- [ ] Integration Tests durchgeführt
- [ ] Manuell getestet

## Checklist
- [ ] Tests laufen durch
- [ ] Linter ohne Fehler
- [ ] Documentation aktualisiert
- [ ] Breaking Changes dokumentiert

Closes #ISSUE_NUMBER
```

## Troubleshooting

### Skill nicht gefunden
Skills befinden sich in `.opencode/skills/`. Prüfe, ob die Datei existiert:
```bash
ls -la .opencode/skills/
```

### Git-Repository nicht erkannt
Stelle sicher, dass du im richtigen Unterprojekt-Verzeichnis bist:
```bash
pwd
git remote -v
```

### GitHub CLI Authentifizierung
```bash
gh auth status
gh auth login
```

### Node Modules fehlen
```bash
cd cookidoo-mcp
npm install
cd ../cookidoo-assistant
npm install
```

## Nächste Schritte

1. **Repositories klonen** (falls noch nicht geschehen):
   ```bash
   git clone https://github.com/TheRealKoller/cookidoo-mcp.git
   git clone https://github.com/TheRealKoller/cookidoo-assistant.git
   ```

2. **Dependencies installieren**:
   ```bash
   cd cookidoo-mcp && npm install && cd ..
   cd cookidoo-assistant && npm install && cd ..
   ```

3. **Erstes Issue erstellen** und Workflow testen:
   ```bash
   # Skill laden und Issue erstellen
   /load-skill github-workflow
   ```

4. **Development starten**:
   ```bash
   cd cookidoo-mcp
   npm run dev
   ```
