# Coverage reporting setup

## Required secrets

Add to GitHub repo settings → Secrets and variables → Actions:

- `CODECOV_TOKEN`: Get from https://codecov.io after connecting repo

## Coverage files

CI uploads coverage from:
- Node tests: `coverage/coverage-final.json`
- Python tests: `coverage.xml`

## View reports

- codecov.io/gh/TheRealKoller/cookidoo-assistant
- Coverage badge auto-updates in README
