# GitHub Actions Workflows

## CI Workflow

**File**: `.github/workflows/ci.yml`  
**Triggers**: Push to `main`, PRs to `main`

### Jobs

1. **lint** - ESLint + Prettier checks
2. **type-check** - TypeScript compilation
3. **test** - Unit tests (Node 18, 20) + coverage
4. **test-python** - Python tests + coverage
5. **build** - Build all services
6. **docker** - Build Docker images

### Coverage

Uploads to Codecov:
- Node: unit tests
- Python: cookidoo-mcp tests

## Release Workflow

**File**: `.github/workflows/release.yml`  
**Triggers**: Tag push (`v*`)

### Steps

1. Build and test all services
2. Extract version from tag
3. Login to GitHub Container Registry (GHCR)
4. Build and push Docker image with tags:
   - `latest`
   - `vX.Y.Z`
   - `vX.Y`
   - `vX`
5. Generate changelog from commits
6. Create GitHub release

### Images

Pushed to: `ghcr.io/therealkoller/cookidoo-assistant/cookidoo-mcp`

## E2E Workflow

**File**: `.github/workflows/e2e.yml`  
**Triggers**: Daily (2 AM), manual, PRs affecting services

### Steps

1. Install Node + Python deps
2. Create test `.env` file
3. Start services via `docker-compose`
4. Wait for health checks
5. Run E2E tests
6. Cleanup

### Environment

- `MCP_SERVER_URL=http://localhost:3000`
- Test credentials in `.env`

## Usage

### Run CI locally

```bash
npm run lint
npm run type-check
npm run test:coverage
npm run build
```

### Create release

```bash
git tag v1.0.0
git push origin v1.0.0
```

### Run E2E manually

```bash
gh workflow run e2e.yml
```

## Secrets

Required in repo settings:

- `CODECOV_TOKEN` - Coverage upload (from codecov.io)
- `GITHUB_TOKEN` - Auto-provided for releases/GHCR

See [COVERAGE.md](COVERAGE.md) and [DOCKER.md](DOCKER.md) for details.
