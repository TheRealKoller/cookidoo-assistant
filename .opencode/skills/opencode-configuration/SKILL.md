---
name: opencode-configuration
description: Create and manage OpenCode Skills, Agents, and MCP Servers
---

# OpenCode Configuration

Kompakter Referenz-Guide für Skills, Agents und MCP-Server.

**WICHTIG**: Alle Skills und Agents MÜSSEN kompakt gestaltet werden:
- Minimale Token-Nutzung
- Wenig Kontext-Verbrauch
- Direkt zu Code-Beispielen
- Keine redundanten Erklärungen

## Skills

### Design-Prinzipien
- **Kompakt**: Max. 200-300 Zeilen
- **Fokussiert**: Nur essenzielle Informationen
- **Code-First**: Beispiele statt Prosa
- **Keine Redundanz**: Jede Info nur einmal

### Erstellen
```bash
mkdir -p .opencode/skills/<name>
cat > .opencode/skills/<name>/SKILL.md << 'EOF'
---
name: skill-name          # PFLICHT: ^[a-z0-9]+(-[a-z0-9]+)*$ (1-64 chars)
description: Short desc   # PFLICHT: 1-1024 chars
---
# Kurzer Titel

## Wann nutzen
1-2 Sätze

## Wichtigste Commands
```bash
command1
command2
```

## Best Practices
- Punkt 1
- Punkt 2
EOF
```

### Berechtigungen
```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "internal-*": "deny"
    }
  }
}
```

## Agents

### Design-Prinzipien
- **Kurze Prompts**: 50-100 Wörter maximum
- **Klare Rolle**: 1-2 Sätze was der Agent tut
- **Fokussierte Tools**: Nur nötige Tools aktivieren
- **Keine langen Anweisungen**: Stichpunkte statt Prosa

### CLI
```bash
opencode agent create  # Interaktiver Wizard
```

### Markdown (.opencode/agents/<name>.md)
```markdown
---
description: Kurze, klare Beschreibung (max 100 chars)
mode: primary|subagent|all
temperature: 0.1                    # 0.1=fokussiert, 0.8=kreativ
tools:
  write: false
  edit: false
permission:
  edit: deny
  bash:
    "*": ask
    "git status": allow
---
# Rolle
Du bist X. Fokus auf Y.

## Aufgaben
- Task 1
- Task 2

## Vermeide
- Thing 1
- Thing 2
```

### JSON (opencode.json)
```json
{
  "agent": {
    "agent-name": {
      "description": "...",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "{file:./prompts/agent.txt}",
      "temperature": 0.1,
      "steps": 10,
      "tools": {
        "skill": false,
        "mcp_*": false
      },
      "permission": {
        "edit": "ask|allow|deny",
        "bash": { "*": "ask" },
        "task": { "*": "deny", "allowed-*": "allow" }
      }
    }
  }
}
```

### Temperature Guide
- 0.0-0.2: Analyse, Code-Review
- 0.3-0.5: Standard-Entwicklung
- 0.6-1.0: Kreativ, Brainstorming

### Built-in Agents
- **primary**: `build` (full access), `plan` (read-only)
- **subagent**: `general` (multi-step), `explore` (codebase search)

## MCP Server

### Lokal
```json
{
  "mcp": {
    "server-name": {
      "type": "local",
      "command": ["npx", "-y", "package-name"],
      "enabled": true,
      "environment": {
        "KEY": "{env:ENV_VAR}"
      },
      "timeout": 5000
    }
  }
}
```

### Remote
```json
{
  "mcp": {
    "server-name": {
      "type": "remote",
      "url": "https://server.com",
      "enabled": true,
      "headers": {
        "Authorization": "Bearer {env:API_KEY}"
      }
    }
  }
}
```

### OAuth
```json
{
  "mcp": {
    "server": {
      "type": "remote",
      "url": "https://server.com",
      "oauth": {}  // Auto-discovery
    }
  }
}
```

```bash
opencode mcp auth server    # Authentifizieren
opencode mcp list           # Status anzeigen
opencode mcp logout server  # Logout
```

### Tools verwalten
```json
{
  "tools": {
    "servername_*": false  // Global aus
  },
  "agent": {
    "agent-name": {
      "tools": {
        "servername_*": true  // Pro Agent aktivieren
      }
    }
  }
}
```

## Quick Reference

### Häufige Patterns
```json
{
  "$schema": "https://opencode.ai/config.json",
  
  // Global alles deaktivieren
  "tools": {
    "mcp_*": false
  },
  
  // Pro Agent aktivieren
  "agent": {
    "searcher": {
      "description": "Uses search tools",
      "mode": "subagent",
      "tools": { "mcp_search_*": true }
    }
  },
  
  // Berechtigungen
  "permission": {
    "skill": { "*": "allow", "internal-*": "deny" },
    "edit": "ask",
    "bash": { "*": "ask", "git status": "allow" }
  }
}
```

### Glob Patterns
- `*` = 0+ chars: `mcp_*` → `mcp_foo`, `mcp_bar`
- `?` = 1 char
- Letzte Regel gewinnt

### Troubleshooting
```bash
# Skill lädt nicht
ls .opencode/skills/*/SKILL.md     # Datei prüfen
# → name muss zum Verzeichnis passen
# → description erforderlich

# MCP verbindet nicht
opencode mcp debug server
# → timeout erhöhen
# → OAuth neu: opencode mcp auth server
```

## Best Practices

### Token-Effizienz (KRITISCH!)
1. **Skills**: Max. 200-300 Zeilen, Code-First, keine Prosa
2. **Agents**: Prompts max. 50-100 Wörter, Stichpunkte
3. **MCP-Tools**: Global deaktivieren, selektiv aktivieren
4. **Berechtigungen**: Nur nötige Tools/Skills aktivieren

### Sicherheit
1. **Env-Variablen**: `{env:VAR}` für Secrets
2. **Permissions**: `ask` für kritisch, `deny` für verboten
3. **Temperature**: 0.1 für Code, 0.7+ für Docs
