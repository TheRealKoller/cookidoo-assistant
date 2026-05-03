---
name: test-and-build
description: Testing, build processes, and CI/CD integration for all services
---

# Testing & Build

Testing, Build und CI/CD für alle Services.

## Quality Gates

### Vor Commit
```bash
npm run lint && npm run format:check && npm run type-check && npm test
```

### Vor Push
```bash
npm run lint && npm run type-check && npm test && npm run build
```

## Node.js/TypeScript Workflows

### Dependencies
```bash
npm install        # Standard
npm ci             # Clean install (CI)
```

### Testing
```bash
npm test                          # Alle
npm run test:coverage             # Mit Coverage
npm run test:watch                # Watch mode
npm test -- path/to/test.spec.ts  # Einzelne Datei

# Jest
npx jest --verbose
npx jest --coverage
npx jest --onlyFailures          # Nur failed
```

### Linting & Formatting
```bash
# ESLint
npm run lint
npm run lint:fix
npx eslint src/**/*.ts

# Prettier
npm run format:check
npm run format
npx prettier --write src/**/*.ts

# Combined
npm run lint && npm run format:check && npm test
```

### Type-Checking
```bash
npm run type-check
npx tsc --noEmit
npx tsc --noEmit --watch
```

### Build
```bash
npm run build                    # Production
npm run clean && npm run build   # Clean build
npm run type-check && npm run build

# Development
npm run dev
npm run watch
```

## Pre-Commit Script

```bash
#!/bin/bash
# pre-commit.sh
set -e

echo "🔍 Linting..."
npm run lint

echo "🎨 Formatting..."
npm run format:check

echo "📝 Type checking..."
npm run type-check

echo "🧪 Testing..."
npm test

echo "🏗️  Building..."
npm run build

echo "✅ All checks passed!"
```

## CI/CD Integration

### GitHub Actions (`.github/workflows/ci.yml`)
```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [18.x, 20.x]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Lint
      run: npm run lint
    
    - name: Type check
      run: npm run type-check
    
    - name: Test
      run: npm test
    
    - name: Build
      run: npm run build
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      if: matrix.node-version == '20.x'
```

### CI Status
```bash
gh run list --limit 5
gh run view
gh pr checks
gh workflow run ci.yml
```

## Package.json Scripts

### Scripts anzeigen
```bash
npm run
cat package.json | jq .scripts
```

### Standard Scripts
```json
{
  "scripts": {
    "dev": "Development server",
    "build": "Production build",
    "test": "Run tests",
    "test:watch": "Tests watch mode",
    "test:coverage": "Tests with coverage",
    "lint": "ESLint check",
    "lint:fix": "ESLint auto-fix",
    "format": "Prettier format",
    "format:check": "Prettier check",
    "type-check": "TypeScript checking",
    "clean": "Clean build artifacts"
  }
}
```

## Debugging

### Tests
```bash
# Node Inspector
node --inspect-brk node_modules/.bin/jest --runInBand
# Chrome: chrome://inspect

# Performance
npm test -- --logHeapUsage
```

### Build
```bash
npm run build -- --verbose
npx tsc --extendedDiagnostics
```

## Best Practices

1. **Tests vor Commits**: Immer Tests laufen lassen
2. **CI nicht ignorieren**: Fehlende Checks sofort fixen
3. **Coverage ≥ 80%**: Mindestabdeckung anstreben
4. **Kein `any`**: Ohne guten Grund vermeiden
5. **Linter befolgen**: Konsistenter Code-Stil
6. **Snapshots bewusst updaten**: `npm test -- -u`
7. **Flaky Tests fixen**: Instabile Tests = Tech Debt

## Troubleshooting

### Tests schlagen fehl
```bash
npm test -- --clearCache
npm test -- --verbose
npm test -- --testNamePattern="test name"
```

### Build-Fehler
```bash
rm -rf node_modules package-lock.json
npm install && npm run build
npx tsc --noEmit --pretty
```

### Linter-Fehler
```bash
npm run lint:fix
# eslint-disable-next-line rule-name  # Nur wenn nötig
```

### Dependencies
```bash
npm outdated
npm audit
npm audit fix
npm list --depth=1
```

## Quick Reference

### Vollständiger Check
```bash
npm install && \
npm run lint && \
npm run format:check && \
npm run type-check && \
npm test && \
npm run build
```

### Watch-Mode Development
```bash
# Terminal 1
npm run dev

# Terminal 2
npm run test:watch

# Terminal 3
npx tsc --watch
```

### CI lokal simulieren
```bash
act -j test  # Mit act (GitHub Actions local)
npm ci && npm run lint && npm test && npm run build
```
