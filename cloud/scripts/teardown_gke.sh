#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/set_env.sh"
kubectl delete namespace cognira-bti --ignore-not-found=true || true
terraform -chdir=cloud/terraform destroy \
  -var="project_id=$PROJECT_ID" \
  -var="region=$REGION" \
  -var="zone=$ZONE" \
  -var="cluster_name=$CLUSTER_NAME" \
  -var="artifact_repo=$ARTIFACT_REPO" \
  -var="gcul_endpoint=$GCUL_ENDPOINT" \
  -var="gcul_chain_id=$GCUL_CHAIN_ID"
