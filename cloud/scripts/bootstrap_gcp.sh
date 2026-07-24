#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/set_env.sh"
gcloud config set project "$PROJECT_ID"
gcloud services enable container.googleapis.com artifactregistry.googleapis.com compute.googleapis.com secretmanager.googleapis.com cloudkms.googleapis.com logging.googleapis.com monitoring.googleapis.com iam.googleapis.com
terraform -chdir=cloud/terraform init
terraform -chdir=cloud/terraform apply \
  -var="project_id=$PROJECT_ID" \
  -var="region=$REGION" \
  -var="zone=$ZONE" \
  -var="cluster_name=$CLUSTER_NAME" \
  -var="artifact_repo=$ARTIFACT_REPO" \
  -var="gcul_endpoint=$GCUL_ENDPOINT" \
  -var="gcul_chain_id=$GCUL_CHAIN_ID"
gcloud container clusters get-credentials "$CLUSTER_NAME" --region "$REGION" --project "$PROJECT_ID"
