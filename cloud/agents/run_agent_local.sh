#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(pwd)/backend:$(pwd)"
python - <<'PY'
from bti.agents.cognira_agent import CogniraBTIAgent
agent = CogniraBTIAgent()
print(agent.generate_narrative('TXN-000421', 'fca_examiner'))
PY
