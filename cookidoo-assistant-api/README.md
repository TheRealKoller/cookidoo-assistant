# cookidoo-assistant-api

REST API für die zukünftige UI-Integration.

## Status

🚧 **In Development** - Lower priority, for future UI

## Beschreibung

REST API Server für die spätere Web/Mobile-UI:
- User-Management
- Profil-Verwaltung
- Ernährungspräferenzen
- Allergien
- Gesundheitsdaten
- Rezept-Bewertungen
- Wochenplan-Management

## Technologie

- Port: 3002
- Database: PostgreSQL
- Dependencies: cookidoo-assistant-shared
- API: REST (JSON)
- Documentation: OpenAPI 3.0

## Installation

```bash
# Im Root des Monorepos
npm install

# Oder für dieses Projekt allein
cd cookidoo-assistant-api
npm install
```

## Konfiguration

```bash
cp .env.example .env
# Fülle DATABASE_URL, API_KEY, etc. aus
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
docker-compose up cookidoo-assistant-api

# Oder einzelner Container
docker build -t cookidoo-assistant-api .
docker run -p 3002:3002 --env-file .env cookidoo-assistant-api
```

## API Endpoints

### User Profile
- `POST /api/v1/profiles` - Create profile
- `GET /api/v1/profiles/:userId` - Get profile
- `PUT /api/v1/profiles/:userId` - Update profile
- `DELETE /api/v1/profiles/:userId` - Delete profile

### Dietary Preferences
- `POST /api/v1/dietary` - Create preferences
- `GET /api/v1/dietary/:userId` - Get preferences
- `PUT /api/v1/dietary/:userId` - Update preferences
- `DELETE /api/v1/dietary/:userId` - Delete preferences

### Allergies
- `POST /api/v1/allergies` - Create allergy
- `GET /api/v1/allergies/:userId` - Get all allergies
- `PUT /api/v1/allergies/:allergyId` - Update allergy
- `DELETE /api/v1/allergies/:allergyId` - Delete allergy

### Health Data
- `POST /api/v1/health` - Create health data
- `GET /api/v1/health/:userId` - Get health data
- `PUT /api/v1/health/:userId` - Update health data
- `DELETE /api/v1/health/:userId` - Delete health data
- `POST /api/v1/health/:userId/calculate` - Calculate nutrition targets

### Recipe Ratings
- `POST /api/v1/ratings` - Create rating
- `GET /api/v1/ratings/:userId` - Get all ratings
- `GET /api/v1/ratings/:userId/:recipeId` - Get specific rating
- `PUT /api/v1/ratings/:userId/:recipeId` - Update rating
- `DELETE /api/v1/ratings/:userId/:recipeId` - Delete rating
- `POST /api/v1/ratings/:userId/:recipeId/track` - Track interaction

### Week Plans
- `POST /api/v1/week-plans` - Create week plan
- `GET /api/v1/week-plans/:planId` - Get specific plan
- `GET /api/v1/week-plans/user/:userId` - Get user's active plan
- `GET /api/v1/week-plans/user/:userId/history` - Get plan history
- `POST /api/v1/week-plans/:planId/meals` - Add meal
- `DELETE /api/v1/week-plans/meals/:mealId` - Remove meal
- `PUT /api/v1/week-plans/meals/:mealId/select` - Select meal option
- `PUT /api/v1/week-plans/:planId/complete` - Complete plan
- `POST /api/v1/week-plans/user/:userId/archive` - Archive old plans

## API Documentation

Swagger/OpenAPI documentation available at:
- Development: http://localhost:3002/api-docs
- See [docs/api-spec.yaml](docs/api-spec.yaml)

## Related Issues

- [#14 - REST API Server](https://github.com/TheRealKoller/cookidoo-assistant/issues/14)
- [#15 - REST API Endpoints](https://github.com/TheRealKoller/cookidoo-assistant/issues/15)

## Lizenz

MIT
