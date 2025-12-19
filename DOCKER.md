# Docker & Deployment 🔧

You can run the app locally in Docker or with docker-compose.

Quick start (Docker):

```bash
# build
docker build -t skills-integrate-mcp-with-copilot:latest .
# run
docker run -p 8000:8000 skills-integrate-mcp-with-copilot:latest
```

Quick start (docker-compose):

```bash
# build & start
docker-compose up --build
# then open http://localhost:8000
```

Build & publish to GitHub Container Registry (example):

```bash
# Build and push (set DOCKER_REGISTRY and DOCKER_REPOSITORY env vars or use defaults)
DOCKER_REGISTRY=ghcr.io DOCKER_REPOSITORY=${{ github.repository }} TAG=v1 ./scripts/deploy.sh --push
```

We also included a GitHub Actions workflow at `.github/workflows/release.yml` which builds and publishes `ghcr.io/${{ github.repository }}:latest` when changes are pushed to `main`.
