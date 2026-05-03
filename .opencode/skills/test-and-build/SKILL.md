---
name: test-and-build
description: Testing, build processes, and CI/CD integration for all services
---

# Testing & Build Skill

## Beschreibung
Dieser Skill unterstützt Testing, Build-Prozesse und CI/CD-Integration für die Cookidoo-Unterprojekte.

## Kontext
Arbeitet mit den Unterprojekten:
- `./cookidoo-mcp/` - MCP Server (vermutlich TypeScript/Node.js)
- `./cookidoo-assistant/` - Assistant (Tech-Stack projektspezifisch)

## Allgemeine Prinzipien

### Vor jedem Commit
1. Tests ausführen
2. Linter prüfen
3. Type-Checking durchführen
4. Build erfolgreich durchführen

### Vor jedem Push
1. Alle Tests erfolgreich
2. Keine Linter-Fehler
3. Keine Type-Errors
4. Build läuft durch

## Standard Node.js/TypeScript Workflows

### 1. Dependencies installieren

```bash
# Im Unterprojekt-Verzeichnis
npm install

# oder mit yarn
yarn install

# Clean install (empfohlen für CI)
npm ci
```

### 2. Testing

#### Unit Tests
```bash
# Alle Tests ausführen
npm test

# Tests mit Coverage
npm run test:coverage

# Tests im Watch-Mode
npm run test:watch

# Einzelne Test-Datei
npm test -- path/to/test.spec.ts

# Jest spezifisch
npx jest
npx jest --verbose
npx jest --coverage
```

#### Integration Tests
```bash
# Falls separates Script vorhanden
npm run test:integration

# E2E Tests
npm run test:e2e
```

#### Test-Debugging
```bash
# Mit Node Inspector
node --inspect-brk node_modules/.bin/jest --runInBand

# Nur fehlgeschlagene Tests
npm test -- --onlyFailures
```

### 3. Linting & Formatting

#### ESLint
```bash
# Linting prüfen
npm run lint

# Auto-Fix
npm run lint:fix

# Spezifische Dateien
npx eslint src/**/*.ts

# Mit Type-Information
npx eslint --ext .ts,.tsx src/
```

#### Prettier
```bash
# Format prüfen
npm run format:check

# Auto-Format
npm run format
npm run format:fix

# Einzelne Dateien
npx prettier --write src/**/*.ts
```

#### Combined Check
```bash
# Empfohlener Pre-Commit Check
npm run lint && npm run format:check && npm test
```

### 4. Type-Checking

#### TypeScript
```bash
# Type-Check
npm run type-check
npx tsc --noEmit

# Mit Watch-Mode
npx tsc --noEmit --watch

# Specific tsconfig
npx tsc --project tsconfig.build.json --noEmit
```

### 5. Build

#### Production Build
```bash
# Standard Build
npm run build

# Clean Build
npm run clean && npm run build

# Build mit Type-Check
npm run type-check && npm run build
```

#### Development Build
```bash
# Watch-Mode
npm run dev
npm run watch

# Mit Hot-Reload
npm run dev:hot
```

### 6. Quality Gates (Vor Commit/Push)

#### Vollständiger Pre-Commit Check
```bash
#!/bin/bash
# pre-commit.sh

set -e  # Bei Fehler abbrechen

echo "🔍 Running linter..."
npm run lint

echo "🎨 Checking formatting..."
npm run format:check

echo "📝 Type checking..."
npm run type-check

echo "🧪 Running tests..."
npm test

echo "🏗️  Building..."
npm run build

echo "✅ All checks passed!"
```

#### Schneller Pre-Commit (nur geänderte Dateien)
```bash
# Mit lint-staged (wenn konfiguriert)
npx lint-staged

# Oder manual
git diff --cached --name-only --diff-filter=ACMR | grep '\.ts$' | xargs npm run lint
```

## CI/CD Integration

### GitHub Actions Workflow-Beispiel

Erstelle `.github/workflows/ci.yml` in den Unterprojekten:

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

### CI-Status prüfen

```bash
# GitHub Actions Status
gh run list --limit 5
gh run view

# Für spezifischen PR
gh pr checks

# Workflow manuell triggern
gh workflow run ci.yml
```

## Projekt-spezifische Scripts

### Package.json Scripts anzeigen
```bash
# Alle verfügbaren Scripts
npm run

# Oder direkt in package.json schauen
cat package.json | jq .scripts
```

### Häufige Script-Namen
```json
{
  "scripts": {
    "dev": "Development server starten",
    "build": "Production build",
    "test": "Tests ausführen",
    "test:watch": "Tests im Watch-Mode",
    "test:coverage": "Tests mit Coverage",
    "lint": "ESLint prüfen",
    "lint:fix": "ESLint mit Auto-Fix",
    "format": "Prettier format",
    "format:check": "Prettier check",
    "type-check": "TypeScript type checking",
    "clean": "Build-Artefakte löschen",
    "prepare": "Husky hooks installieren"
  }
}
```

## Debugging

### Debug Tests
```bash
# Node Inspector für Jest
node --inspect-brk node_modules/.bin/jest --runInBand

# Dann in Chrome: chrome://inspect
```

### Debug Build
```bash
# Verbose Build Output
npm run build -- --verbose

# TypeScript mit Trace
npx tsc --extendedDiagnostics
```

### Performance-Analyse
```bash
# Jest Performance
npm test -- --logHeapUsage

# Build Performance
npx tsc --diagnostics
```

## Best Practices

1. **Tests vor Commits**: Führe immer Tests vor dem Commit aus
2. **CI nicht ignorieren**: Fixe fehlende CI-Checks sofort
3. **Coverage im Auge behalten**: Mindestens 80% Coverage anstreben
4. **Type-Safety**: Keine `any` ohne guten Grund
5. **Linter-Rules befolgen**: Konsistenter Code-Stil
6. **Snapshots aktualisieren**: Nur wenn gewollt (`npm test -- -u`)
7. **Flaky Tests fixen**: Instabile Tests sind technische Schulden

## Troubleshooting

### Tests schlagen fehl
```bash
# Cache löschen
npm test -- --clearCache

# Verbose Output
npm test -- --verbose

# Einzelnen Test debuggen
npm test -- --testNamePattern="test name"
```

### Build-Fehler
```bash
# Clean Build
rm -rf node_modules package-lock.json
npm install
npm run build

# TypeScript Errors anzeigen
npx tsc --noEmit --pretty
```

### Linter-Fehler
```bash
# Auto-Fix versuchen
npm run lint:fix

# Spezifische Regel deaktivieren (nur wenn nötig)
# eslint-disable-next-line rule-name
```

### Dependencies-Probleme
```bash
# Outdated packages prüfen
npm outdated

# Audit für Security-Issues
npm audit
npm audit fix

# Dependencies-Baum anzeigen
npm list --depth=1
```

## Quick Reference

### Vollständiger Check vor Push
```bash
npm install && \
npm run lint && \
npm run format:check && \
npm run type-check && \
npm test && \
npm run build
```

### Watch-Mode für Development
```bash
# In separaten Terminals
npm run dev        # Terminal 1: Dev Server
npm run test:watch # Terminal 2: Tests
npx tsc --watch    # Terminal 3: Type Checking
```

### CI lokal simulieren
```bash
# Mit act (GitHub Actions lokal)
act -j test

# Oder manual
npm ci && npm run lint && npm test && npm run build
```
