#!/usr/bin/env bash
set -euo pipefail

# Simple deploy helper that builds, tags, and optionally pushes the image.
# Usage:
#   DOCKER_REGISTRY=ghcr.io DOCKER_REPOSITORY=owner/skills-integrate-mcp-with-copilot TAG=v1 ./scripts/deploy.sh --push

REGISTRY="${DOCKER_REGISTRY:-ghcr.io}"
REPOSITORY="${DOCKER_REPOSITORY:-$GITHUB_REPOSITORY}"
TAG="${TAG:-latest}"
PUSH=false

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --push) PUSH=true ; shift ;;
    -t|--tag) TAG="$2" ; shift 2 ;;
    -r|--registry) REGISTRY="$2" ; shift 2 ;;
    -h|--help) echo "Usage: $0 [--push] [-t TAG] [-r REGISTRY]" ; exit 0 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

IMAGE="$REGISTRY/$REPOSITORY:$TAG"

echo "Building image $IMAGE..."
docker build -t "$IMAGE" .

if [ "$PUSH" = true ]; then
  echo "Pushing $IMAGE..."
  docker push "$IMAGE"
else
  echo "Built $IMAGE locally. Use --push to push to a registry."
fi
