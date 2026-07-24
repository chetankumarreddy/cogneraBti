#!/usr/bin/env bash
set -euo pipefail
./cloud/scripts/bootstrap_gcp.sh
./cloud/scripts/create_or_update_secrets.sh
./cloud/scripts/build_and_push.sh
./cloud/scripts/deploy_gke.sh
