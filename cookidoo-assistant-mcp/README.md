# cookidoo-assistant-mcp

MCP (Model Context Protocol) Server für User-Daten und Präferenzen.

## Status

🚧 **In Development** - Awaiting tech stack decision

## Beschreibung

Dieser MCP-Server verwaltet User-Daten für den AI-Agent:
- User-Profile (Größe, Gewicht, Alter, Geschlecht)
- Ernährungspräferenzen (omnivor, vegetarisch, vegan, etc.)
- Allergien und Unverträglichkeiten
- Gesundheitsdaten (Aktivitätslevel, Ziele, Kalorien, Makros)
- Rezept-Bewertungen (gemocht/nicht gemocht)
- Wochenpläne (erstellen, verwalten, archivieren)

## Technologie

- Port: 3001
- Database: PostgreSQL
- Dependencies: cookidoo-assistant-shared
- Protocol: MCP

## Installation

```bash
# Im Root des Monorepos
npm install

# Oder für dieses Projekt allein
cd cookidoo-assistant-mcp
npm install
```

## Konfiguration

```bash
cp .env.example .env
# Fülle DATABASE_URL, MCP_API_KEY, etc. aus
```

## Entwicklung

```bash
# Development Server starten
npm run dev

# Tests ausführen
npm test

# Mit Datenbank
docker-compose up postgres
npm run dev
```

## Docker

```bash
# Mit docker-compose (inkl. PostgreSQL)
docker-compose up cookidoo-assistant-mcp

# Oder einzelner Container
docker build -t cookidoo-assistant-mcp .
docker run -p 3001:3001 --env-file .env cookidoo-assistant-mcp
```

## MCP Tools (CRUD)

### User Profile
- `create_user_profile`
- `get_user_profile`
- `update_user_profile`
- `delete_user_profile`

### Dietary Preferences
- `create_dietary_preference`
- `get_dietary_preferences`
- `update_dietary_preference`
- `delete_dietary_preference`

### Allergies
- `create_allergy`
- `get_allergies`
- `update_allergy`
- `delete_allergy`

### Health Data
- `create_health_data`
- `get_health_data`
- `update_health_data`
- `delete_health_data`
- `calculate_nutrition_targets`

### Recipe Ratings
- `create_recipe_rating`
- `get_recipe_ratings`
- `get_recipe_rating`
- `update_recipe_rating`
- `delete_recipe_rating`
- `track_recipe_interaction`

### Week Plans
- `create_week_plan`
- `get_week_plan`
- `get_week_plan_history`
- `add_meal_to_plan`
- `remove_meal_from_plan`
- `select_meal_option`
- `complete_week_plan`
- `archive_old_plans`

Siehe [docs/mcp-tools.md](docs/mcp-tools.md) für Details.

## Related Issues

- [#7 - MCP Server Core](https://github.com/TheRealKoller/cookidoo-assistant/issues/7)
- [#8-13 - MCP Tools](https://github.com/TheRealKoller/cookidoo-assistant/issues/8)

## Lizenz

MIT
