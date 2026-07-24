#!/usr/bin/env bash
set -euo pipefail
export PROJECT_ID="${PROJECT_ID:-your-gcp-project-id}"
export REGION="${REGION:-europe-west2}"
export ZONE="${ZONE:-europe-west2-a}"
export CLUSTER_NAME="${CLUSTER_NAME:-cognira-bti-gke}"
export ARTIFACT_REPO="${ARTIFACT_REPO:-cognira-bti}"
export IMAGE_TAG="${IMAGE_TAG:-hackathon}"
export GCUL_ENDPOINT="${GCUL_ENDPOINT:-https://gcul.example.internal/rpc}"
export GCUL_CHAIN_ID="${GCUL_CHAIN_ID:-gcul-hackathon}"
export ETH_RPC_URL="${ETH_RPC_URL:-}"
