# cookidoo-assistant-shared

Shared library for business logic and data access.

## Status

✅ **Setup Complete** - Ready for use by MCP and API services

## Description

This shared library provides:
- Database Connection Management (PostgreSQL)
- Data Models and Repositories
- Business Logic Services (placeholder for Issue #6)
- Error Handling Utilities
- Logging Utilities
- Validation Helpers with Zod
- Type Definitions

Used by `cookidoo-assistant-mcp` and `cookidoo-assistant-api`.

## Package Structure

```
cookidoo-assistant-shared/
├── src/
│   ├── db/              # Database connection & migration management
│   │   ├── connection.ts
│   │   └── migrations.ts
│   ├── models/          # Data models/entities
│   │   ├── base.ts
│   │   └── entities.ts
│   ├── repositories/    # Data access layer with CRUD operations
│   │   ├── base.repository.ts
│   │   └── entities.repository.ts
│   ├── services/        # Business logic (to be implemented in #6)
│   │   └── index.ts
│   ├── utils/           # Utility functions
│   │   ├── errors.ts
│   │   ├── logger.ts
│   │   └── validation.ts
│   └── index.ts         # Public API exports
├── tests/               # Unit tests
└── dist/                # Build output
```

## Installation

As part of the monorepo:

```bash
cd /path/to/monorepo-root
npm install
```

## Usage

### Database Connection

```typescript
import { db, DatabaseConfig } from 'cookidoo-assistant-shared/db';

const config: DatabaseConfig = {
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME || 'cookidoo_assistant',
  username: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres',
};

await db.connect(config);
```

### Using Repositories

```typescript
import {
  userProfileRepository,
  weekPlanRepository,
} from 'cookidoo-assistant-shared/repositories';

// Create a user profile
const profile = await userProfileRepository.create({
  userId: 'user123',
  name: 'John Doe',
  email: 'john@example.com',
});

// Find by user ID
const userProfile = await userProfileRepository.findByUserId('user123');

// Get active week plan
const activePlan = await weekPlanRepository.findActiveByUserId('user123');
```

### Using Models and Types

```typescript
import {
  UserProfile,
  DietaryPreference,
  WeekPlan,
  CreateEntity,
  UpdateEntity,
} from 'cookidoo-assistant-shared/models';

type CreateUserProfile = CreateEntity<UserProfile>;
type UpdateUserProfile = UpdateEntity<UserProfile>;
```

### Error Handling

```typescript
import {
  AppError,
  ValidationError,
  NotFoundError,
  DatabaseError,
} from 'cookidoo-assistant-shared/utils';

try {
  const user = await userProfileRepository.findByIdOrFail(123);
} catch (error) {
  if (error instanceof NotFoundError) {
    console.log('User not found');
  }
}
```

### Logging

```typescript
import { logger } from 'cookidoo-assistant-shared/utils';

logger.info('User created', { userId: '123' });
logger.error('Database error', error, { operation: 'create' });
logger.debug('Debug info', { details: {...} });
```

### Validation

```typescript
import { validate, commonSchemas } from 'cookidoo-assistant-shared/utils';
import { z } from 'zod';

const userSchema = z.object({
  name: commonSchemas.nonEmptyString,
  email: commonSchemas.email,
  age: commonSchemas.positiveInt,
});

const validatedData = validate(userSchema, inputData);
```

## Development

```bash
# Install dependencies
npm install

# Run tests
npm test

# Run tests with coverage
npm test:coverage

# Build
npm run build

# Watch mode for development
npm run dev

# Type checking
npm run type-check

# Linting
npm run lint
npm run lint:fix

# Formatting
npm run format
npm run format:check
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cookidoo_assistant
DB_USER=postgres
DB_PASSWORD=postgres
DB_SSL=false

# Logging
LOG_LEVEL=info
```

## Available Entities

- **UserProfile** - User account and preferences
- **DietaryPreference** - User dietary choices (vegetarian, vegan, etc.)
- **Allergy** - User allergies with severity levels
- **HealthData** - Health metrics (weight, blood pressure, etc.)
- **RecipeRating** - User ratings and reviews for recipes
- **WeekPlan** - Weekly meal planning
- **WeekPlanMeal** - Individual meals in a week plan

## Database Schema

Database schema and migrations will be implemented in Issue #4.

## Testing

All utilities have comprehensive unit tests:
- Error handling (`tests/utils/errors.test.ts`)
- Logging (`tests/utils/logger.test.ts`)
- Validation (`tests/utils/validation.test.ts`)

Current test coverage: 28 passing tests across 3 test suites.

## Related Issues

- [#3 - Setup Shared Library](https://github.com/TheRealKoller/cookidoo-assistant/issues/3) ✅
- [#4 - Database Schema](https://github.com/TheRealKoller/cookidoo-assistant/issues/4) 🚧
- [#5 - Data Access Layer](https://github.com/TheRealKoller/cookidoo-assistant/issues/5) 🚧
- [#6 - Business Logic Services](https://github.com/TheRealKoller/cookidoo-assistant/issues/6) 🚧

## License

MIT
