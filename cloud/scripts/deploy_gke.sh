#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/set_env.sh"
REGISTRY="$REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REPO"
BACKEND_IMAGE="$REGISTRY/cognira-bti-api:$IMAGE_TAG"
FRONTEND_IMAGE="$REGISTRY/cognira-bti-web:$IMAGE_TAG"
WORKLOAD_GSA="cognira-bti-workload@$PROJECT_ID.iam.gserviceaccount.com"
ETH_RPC_URL_EFFECTIVE="$ETH_RPC_URL"
if [ -z "$ETH_RPC_URL_EFFECTIVE" ]; then
  ETH_RPC_URL_EFFECTIVE="$(terraform -chdir=cloud/terraform output -raw ethereum_rpc_internal_url 2>/dev/null || true)"
fi
TMP_DIR="/tmp/cognira-bti-k8s"
rm -rf "$TMP_DIR" && mkdir -p "$TMP_DIR"
cp -R cloud/k8s/base/* "$TMP_DIR/"
find "$TMP_DIR" -type f -name '*.yaml' -print0 | xargs -0 sed -i \
  -e "s#PROJECT_ID_PLACEHOLDER#$PROJECT_ID#g" \
  -e "s#REGION_PLACEHOLDER#$REGION#g" \
  -e "s#ZONE_PLACEHOLDER#$ZONE#g" \
  -e "s#GCUL_ENDPOINT_PLACEHOLDER#$GCUL_ENDPOINT#g" \
  -e "s#ETHEREUM_RPC_URL_PLACEHOLDER#$ETH_RPC_URL_EFFECTIVE#g" \
  -e "s#BACKEND_IMAGE_PLACEHOLDER#$BACKEND_IMAGE#g" \
  -e "s#FRONTEND_IMAGE_PLACEHOLDER#$FRONTEND_IMAGE#g" \
  -e "s#COGNIRA_WORKLOAD_GSA_PLACEHOLDER#$WORKLOAD_GSA#g"
kubectl apply -k "$TMP_DIR"
gcloud iam service-accounts add-iam-policy-binding "$WORKLOAD_GSA" \
  --project "$PROJECT_ID" \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:$PROJECT_ID.svc.id.goog[cognira-bti/cognira-bti-ksa]" || true
kubectl -n cognira-bti rollout status deploy/cognira-bti-api
kubectl -n cognira-bti rollout status deploy/cognira-bti-web
kubectl -n cognira-bti get svc cognira-bti-web
