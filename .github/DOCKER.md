# Docker Registry Authentication

## GitHub Container Registry (GHCR)

Already configured in release.yml using:
- Registry: `ghcr.io`
- User: `${{ github.actor }}`
- Token: `${{ secrets.GITHUB_TOKEN }}` (auto-provided)

Images pushed to: `ghcr.io/therealkoller/cookidoo-assistant/cookidoo-mcp`

## Docker Hub (optional)

To push to Docker Hub instead:

1. Add secrets to repo:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`

2. Update release.yml login:
```yaml
- uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

3. Update IMAGE_PREFIX in release.yml env

## Permissions

Release workflow needs:
- `contents: write` - create releases
- `packages: write` - push to GHCR

Already set in release.yml:28-30
