#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/set_env.sh"
REGISTRY="$REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REPO"
gcloud auth configure-docker "$REGION-docker.pkg.dev" --quiet
docker build -f backend/Dockerfile -t "$REGISTRY/cognira-bti-api:$IMAGE_TAG" .
docker build -f frontend/Dockerfile -t "$REGISTRY/cognira-bti-web:$IMAGE_TAG" .
docker push "$REGISTRY/cognira-bti-api:$IMAGE_TAG"
docker push "$REGISTRY/cognira-bti-web:$IMAGE_TAG"
echo "BACKEND_IMAGE=$REGISTRY/cognira-bti-api:$IMAGE_TAG"
echo "FRONTEND_IMAGE=$REGISTRY/cognira-bti-web:$IMAGE_TAG"
