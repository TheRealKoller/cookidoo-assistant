# Running Migration Tests

## Prerequisites

The migration tests require a PostgreSQL database. You can use Docker for easy setup:

```bash
# Start PostgreSQL with Docker
docker run -d \
  --name cookidoo-postgres-test \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=cookidoo_test \
  -p 5432:5432 \
  postgres:15-alpine

# Or use docker-compose (if available in project root)
docker-compose up -d postgres
```

## Environment Variables

Create a `.env` file in `cookidoo-assistant-shared/` directory:

```env
# Test Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cookidoo_test
DB_USER=postgres
DB_PASSWORD=postgres
DB_SSL=false
```

## Running Tests

```bash
# Run all tests
npm test

# Run only migration tests
npm test tests/migrations.test.ts

# Run with coverage
npm test:coverage
```

## Test Database Reset

To reset the test database between test runs:

```bash
# Drop and recreate database
docker exec cookidoo-postgres-test psql -U postgres -c "DROP DATABASE IF EXISTS cookidoo_test;"
docker exec cookidoo-postgres-test psql -U postgres -c "CREATE DATABASE cookidoo_test;"
```

## CI/CD

The CI pipeline will:
1. Start a PostgreSQL container
2. Run migrations
3. Execute all tests
4. Check test coverage

Tests are required to pass before merge.
