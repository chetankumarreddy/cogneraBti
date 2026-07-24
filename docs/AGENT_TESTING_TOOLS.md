# Cognira BTI Agent Testing Tools

## Purpose

The package now includes agent testing tools for validating Cognira BTI investigation agents, Narrative Forge outputs, RAG grounding and local ML scoring before hackathon or GKE deployment.

Google describes ADK as an open-source framework for building, debugging and deploying reliable agents at enterprise scale, and its documentation highlights tools, orchestration, evaluation and deployment patterns. This package therefore adds a local test harness, golden test cases, evaluation scripts and CI hooks to support those development practices. citeturn8search64turn8search65

Google also documents Agent Runtime deployment for ADK agents and Agents CLI workflows for scaffolding, evaluation, deployment and observability. The Cognira BTI package remains GKE-first, but the testing tools are structured to support optional Agent Runtime and Agents CLI workflows. citeturn8search66turn8search73

## Added folders

```text
backend/bti/agents/testing/
├── __init__.py
├── agent_test_harness.py
├── assertions.py
└── golden_runner.py

tests/
├── agent/
│   ├── test_agent_contract.py
│   ├── test_agent_golden.py
│   └── test_rag_ml_tools.py
├── fixtures/
│   └── agent_golden_cases.json
├── reports/
└── scripts/
    └── run_agent_tests.py

cloud/agents/testing/
├── agent_test_config.yaml
├── run_agent_tests.sh
└── run_agent_tests.bat
```

## Local test commands

```bash
export PYTHONPATH=backend:.
python -m pytest tests/agent -q
python tests/scripts/run_agent_tests.py
```

Or use:

```bash
./cloud/agents/testing/run_agent_tests.sh
```

Windows:

```bat
cloud\agents\testing\run_agent_tests.bat
```

## New API endpoints

```text
POST /agents/testing/run
GET  /agents/testing/report
```

## Test categories

- Agent contract tests
- Golden narrative tests
- Story Guardian tests
- Required phrase tests
- Anti-speculation tests
- Low-confidence human review tests
- Evidence reference tests
- RAG build/search tests
- ML router scoring tests

## CI/CD integration

The Cloud Build pipeline now includes an `agent-tests` step before building container images.
