#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(pwd)/backend:$(pwd)"
python -m pytest tests/agent -q
python tests/scripts/run_agent_tests.py
