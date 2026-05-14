# Database Testing in CI

## Overview

The project includes comprehensive database migration and repository tests that require a PostgreSQL database. These tests run automatically in the CI pipeline using GitHub Actions service containers.

## CI Pipeline Setup

The CI pipeline includes a dedicated `test-database` job that:

1. **Starts PostgreSQL 15 service container**
   - Image: `postgres:15-alpine`
   - Database: `cookidoo_test`
   - Health checks ensure DB is ready before tests run

2. **Runs migration and repository tests**
   - All tests in `tests/migrations.test.ts`
   - Tests are enabled via `DATABASE_AVAILABLE=true` environment variable
   - Full coverage reporting for DB and repository code

3. **Reports coverage to Codecov**
   - Separate coverage report with `database` flag
   - Tracks coverage for `src/db/**` and `src/repositories/**`

## Local Testing

### Without Database (Default)

When running tests locally without a database:

```bash
npm test
```

- Migration tests are **skipped** (15 tests)
- DB/repository files are **excluded** from coverage
- Only utility tests run (28 tests)
- Coverage threshold: 70% (met by utilities at 98%)

### With Database (Full Tests)

To run all tests including database tests:

```bash
# 1. Start PostgreSQL
docker run -d \
  --name cookidoo-postgres-test \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=cookidoo_test \
  -p 5432:5432 \
  postgres:15-alpine

# 2. Run tests with DATABASE_AVAILABLE flag
DATABASE_AVAILABLE=true \
DB_HOST=localhost \
DB_PORT=5432 \
DB_NAME=cookidoo_test \
DB_USER=postgres \
DB_PASSWORD=postgres \
npm test

# 3. Cleanup
docker stop cookidoo-postgres-test
docker rm cookidoo-postgres-test
```

When `DATABASE_AVAILABLE=true`:
- Migration tests **run** (15 tests)
- DB/repository files are **included** in coverage
- All tests run (43 tests total)
- Coverage threshold: 70% for all code including DB

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_AVAILABLE` | `false` | Enable database tests |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `cookidoo_test` | Database name |
| `DB_USER` | `postgres` | Database user |
| `DB_PASSWORD` | `postgres` | Database password |

## CI Workflow Details

From `.github/workflows/ci.yml`:

```yaml
test-database:
  runs-on: ubuntu-latest
  services:
    postgres:
      image: postgres:15-alpine
      env:
        POSTGRES_PASSWORD: postgres
        POSTGRES_DB: cookidoo_test
      options: >-
        --health-cmd pg_isready
        --health-interval 10s
        --health-timeout 5s
        --health-retries 5
      ports:
        - 5432:5432
  env:
    DATABASE_AVAILABLE: true
    DB_HOST: localhost
    DB_PORT: 5432
    DB_NAME: cookidoo_test
    DB_USER: postgres
    DB_PASSWORD: postgres
```

## Test Coverage

### Without Database
- **Utility tests**: 28 tests, ~98% coverage
- **Migration tests**: 15 tests skipped
- **Coverage files**: `src/utils/**`

### With Database
- **Utility tests**: 28 tests, ~98% coverage
- **Migration tests**: 15 tests, coverage TBD
- **Coverage files**: All files including `src/db/**`, `src/repositories/**`

## Why This Approach?

1. **Fast local development**: Developers can run tests without database setup
2. **Complete CI validation**: All code is tested in CI with real database
3. **Separate coverage tracking**: DB tests have dedicated Codecov flag
4. **No mocking required**: Tests run against real PostgreSQL
5. **Health checks**: Ensures database is ready before tests run

## Troubleshooting

### Tests skipped in CI
Check that `DATABASE_AVAILABLE=true` is set in the CI job environment.

### Connection errors
Verify PostgreSQL service container is healthy:
- Check health check configuration
- Ensure ports are properly mapped (5432:5432)
- Verify credentials match environment variables

### Tests pass locally but fail in CI
Ensure local PostgreSQL version matches CI (postgres:15-alpine).
