#!/usr/bin/env bash
set -euo pipefail
python -m pip install --upgrade google-adk google-agents-cli || true
echo "Agents CLI / ADK setup attempted. If your environment blocks install, use the local agent facade under backend/bti/agents."
