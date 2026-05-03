# cookidoo-mcp

MCP (Model Context Protocol) Server für Cookidoo-Integration.

## Status

🚧 **In Development** - Awaiting tech stack decision (Issue #2)

## Beschreibung

Dieser MCP-Server stellt Tools bereit, um mit der Cookidoo-API zu interagieren:
- Rezepte suchen (Freitext, Zutaten, Filter)
- Rezept-Details abrufen
- Nährwertinformationen abrufen
- Zutaten durchsuchen
- Rezepte zum Wochenplan hinzufügen

## Voraussetzungen

- Gültiges Cookidoo-Abo
- Node.js >= 18 oder Python >= 3.11 (abhängig von Tech-Stack-Entscheidung)
- Docker (für Container-Deployment)

## Installation

```bash
# Im Root des Monorepos
npm install

# Oder für dieses Projekt allein
cd cookidoo-mcp
npm install
```

## Konfiguration

Kopiere `.env.example` zu `.env` und fülle die Werte aus:

```bash
cp .env.example .env
```

## Entwicklung

```bash
# Development Server starten
npm run dev

# Tests ausführen
npm test

# Build
npm run build
```

## Docker

```bash
# Image bauen
docker build -t cookidoo-mcp .

# Container starten
docker run -p 3000:3000 --env-file .env cookidoo-mcp
```

## MCP Tools

Siehe [docs/tools.md](docs/tools.md) für eine vollständige Liste der verfügbaren MCP-Tools.

## Related Issues

- [#2 - Evaluate Cookidoo API Libraries](https://github.com/TheRealKoller/cookidoo-mcp/issues/2)
- [#3 - Docker Configuration](https://github.com/TheRealKoller/cookidoo-mcp/issues/3)
- [#4 - MCP Server Core](https://github.com/TheRealKoller/cookidoo-mcp/issues/4)

## Lizenz

MIT
