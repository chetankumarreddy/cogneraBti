#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/set_env.sh"
read -rsp "Enter GCUL password/token: " GCUL_PASSWORD; echo
read -rsp "Enter Ethereum RPC password/token if required, otherwise press Enter: " ETH_PASSWORD; echo
read -rsp "Enter Cognira BTI admin password: " ADMIN_PASSWORD; echo
create_secret() {
  local name="$1" value="$2"
  gcloud secrets describe "$name" --project "$PROJECT_ID" >/dev/null 2>&1 || gcloud secrets create "$name" --replication-policy="automatic" --project "$PROJECT_ID"
  printf "%s" "$value" | gcloud secrets versions add "$name" --data-file=- --project "$PROJECT_ID"
}
create_secret cognira-bti-gcul-password "$GCUL_PASSWORD"
create_secret cognira-bti-ethereum-rpc-password "$ETH_PASSWORD"
create_secret cognira-bti-admin-password "$ADMIN_PASSWORD"
echo "Secrets stored in Google Secret Manager. No password was written to Git files."
