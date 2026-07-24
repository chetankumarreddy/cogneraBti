#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(pwd)/backend:$(pwd)"
python - <<'PY'
from bti.agents.eval_runner import AgentEvalRunner
print(AgentEvalRunner().run())
PY
