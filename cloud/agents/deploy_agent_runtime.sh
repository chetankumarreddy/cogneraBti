#!/usr/bin/env bash
set -euo pipefail
source ./cloud/scripts/set_env.sh
cat <<MSG
This package is GKE-first for the hackathon. Optional Agent Runtime deployment can be enabled with Google ADK / Agents CLI.
Suggested flow:
  1. ./cloud/agents/agents_cli_setup.sh
  2. export GOOGLE_CLOUD_PROJECT=$PROJECT_ID
  3. export GOOGLE_CLOUD_LOCATION=$REGION
  4. Package cloud/agents/cognira_bti_agent as your ADK agent source.
MSG
