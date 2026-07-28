#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="ltc-hack2026-team36"
REGION="europe-west2"
GEMINI_KEY="AQ.Ab8RN6Iwq-kOM8ttsfggK95rcVJ0P2iQV5AKc8s36LvMgHDAkg"
REPO_URL="https://github.com/chetankumarreddy/cogneraBti.git"

echo "=== 1. Git Commit & Push (ignoring venv/git/vs files) ==="
git config --global user.name "Chetan Kumar Reddy"
git config --global user.email "chetankumarreddy@users.noreply.github.com"
git init || true
git remote set-url origin "$REPO_URL" 2>/dev/null || git remote add origin "$REPO_URL"
git add .
git commit -m "feat: realign reboot-v1 ui features with cognerabti backend and mock fallbacks" || echo "No changes"
git branch -M main
git push -u origin main --force

echo "=== 2. Configuring GCP Project & APIs ==="
gcloud config set project "$PROJECT_ID"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com aiplatform.googleapis.com

echo "=== 3. Deploying Backend API to Cloud Run ==="
gcloud builds submit --tag "gcr.io/$PROJECT_ID/cognira-bti-api" backend/
gcloud run deploy cognira-bti-api \
    --image "gcr.io/$PROJECT_ID/cognira-bti-api" \
    --platform managed --region "$REGION" --allow-unauthenticated \
    --set-env-vars GCP_PROJECT_ID="$PROJECT_ID",GCP_REGION="$REGION",GEMINI_API_KEY="$GEMINI_KEY",PORT=8000

BACKEND_URL=$(gcloud run services describe cognira-bti-api --platform managed --region "$REGION" --format 'value(status.url)')
echo "Backend URL: $BACKEND_URL"

echo "=== 4. Deploying Frontend Web App to Cloud Run ==="
gcloud builds submit --tag "gcr.io/$PROJECT_ID/cognira-bti-web" frontend/
gcloud run deploy cognira-bti-web \
    --image "gcr.io/$PROJECT_ID/cognira-bti-web" \
    --platform managed --region "$REGION" --allow-unauthenticated \
    --set-env-vars VITE_API_URL="$BACKEND_URL"

FRONTEND_URL=$(gcloud run services describe cognira-bti-web --platform managed --region "$REGION" --format 'value(status.url)')

echo "================================================="
echo " 🎉 CLOUD RUN DEPLOYMENT SUCCESSFUL! "
echo " Public Frontend: $FRONTEND_URL"
echo " Public Backend:  $BACKEND_URL"
echo "================================================="
