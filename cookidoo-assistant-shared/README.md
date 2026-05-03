# cookidoo-assistant-shared

Gemeinsame Bibliothek für Business-Logic und Datenzugriff.

## Status

🚧 **In Development** - Awaiting tech stack decision

## Beschreibung

Diese Shared Library enthält:
- Database Connection Management
- Data Models und Repositories
- Business Logic Services
- Utility-Funktionen
- Type Definitions

Wird von `cookidoo-assistant-mcp` und `cookidoo-assistant-api` verwendet.

## Module

- **config/** - Konfigurationsmanagement
- **db/** - Datenbank-Connection und Migrations
- **models/** - Datenmodelle
- **repositories/** - Data Access Layer (CRUD)
- **services/** - Business Logic
  - UserService
  - HealthCalculatorService
  - RecipePreferenceService
  - WeekPlanService
- **utils/** - Hilfsfunktionen

## Installation

Als Teil des Monorepos:

```bash
cd /path/to/monorepo-root
npm install
```

## Verwendung

```typescript
// In cookidoo-assistant-mcp oder cookidoo-assistant-api
import { UserService, WeekPlanService } from 'cookidoo-assistant-shared';

const userService = new UserService();
const user = await userService.getUserProfile(userId);
```

## Entwicklung

```bash
# Tests ausführen
npm test

# Build
npm run build

# Type checking
npm run type-check
```

## Datenbank-Schema

Siehe [docs/database-schema.md](docs/database-schema.md) für Details zum Datenbankschema.

## Related Issues

- [#3 - Setup Shared Library](https://github.com/TheRealKoller/cookidoo-assistant/issues/3)
- [#4 - Database Schema](https://github.com/TheRealKoller/cookidoo-assistant/issues/4)
- [#5 - Data Access Layer](https://github.com/TheRealKoller/cookidoo-assistant/issues/5)
- [#6 - Business Logic Services](https://github.com/TheRealKoller/cookidoo-assistant/issues/6)

## Lizenz

MIT
