# Cognira BTI Hackathon Edition

This is the self-contained hackathon/demo edition of **Cognira BTI**.
It is designed to run reliably without cloud credentials while still exposing the full enterprise configuration model.

## One-command run

### macOS / Linux / Git Bash
```bash
./run_all.sh
```

### Windows
```bat
run_all.bat
```

### Python
```bash
python run_all.py
```

## URLs

```text
API Docs:  http://localhost:8000/docs
Frontend:  http://localhost:5173
Demo TXN:  TXN-000421
```

## Hackathon fallback-first design

The hackathon edition includes all configuration and fallback options:

- Ledger: `gcul -> mock_gcul -> ethereum_mock -> eosio_mock -> fabric_simulation`
- LLM: `gemini -> ollama -> transformers -> template -> mock`
- Graph: `neo4j -> networkx`
- Auth: `firebase -> mock`
- Storage: `firestore -> bigquery -> local_json`
- Enrichment: KYC, 2FA, PAM, AD, SIEM and syslog mock/local fallbacks

Configuration files:

```text
control_room/connectors.yaml
control_room/fallback_strategy.yaml
control_room/deployment_modes.yaml
control_room/rules.yaml
control_room/policies.yaml
.env.sample
```

## What this edition includes

- React-only frontend
- Python FastAPI backend
- Configurable Rule Alchemist
- Mock GCUL ledger
- NetworkX topology graph
- Template/mock narrative fallback
- Local evidence export
- FCA PDF and CSV export
- Case creation
- 520 synthetic blockchain transactions

## Recommended demo

Search for:

```text
TXN-000421
```

This demonstrates off-hours full-balance withdrawal, contextual risk scoring, graph visualisation, narrative generation and evidence readiness.


## Google Cloud GKE deployment

This hackathon edition now includes GKE, GCUL and Ethereum RPC node deployment alignment.

Cloud deployment assets:

```text
cloud/terraform/          GKE, Artifact Registry, Secret Manager, VPC and Ethereum RPC VM
cloud/k8s/base/           Kubernetes manifests for API, React UI, ConfigMap and Secret Manager CSI
cloud/scripts/            Bootstrap, secret creation, build, push, deploy and teardown scripts
cloud/cloudbuild/         Cloud Build container build pipeline
backend/app/cloud_runtime.py  Cloud runtime and secret mount status endpoint
```

Main command:

```bash
./cloud/scripts/full_gke_deploy.sh
```

Set cloud location and endpoints in:

```bash
cloud/scripts/set_env.sh
cloud/terraform/terraform.tfvars.example
.env.sample
```

Passwords must not be committed. Use:

```bash
./cloud/scripts/create_or_update_secrets.sh
```

Runtime check after deployment:

```bash
curl http://localhost:8000/cloud/runtime
```

## Agent development tools added

The package now includes Cognira BTI agent development tools for local agent testing, ADK-style agent source packaging, agent evaluation and optional Agent Runtime alignment.

```text
cloud/agents/
backend/bti/agents/
docs/SOURCE_TREE_AUDIT_AND_COMPLETION.md
```

Local agent test:

```bash
./cloud/agents/run_agent_local.sh
```

Agent evaluation:

```bash
./cloud/agents/run_agent_eval.sh
```

Agent API endpoints:

```text
GET  /agents/manifest
GET  /agents/runtime/status
POST /agents/analyse/{txn_id}
POST /agents/evaluate
```

## Agent testing tools

Agent testing tools are now included for local and CI validation.

```bash
./cloud/agents/testing/run_agent_tests.sh
```

Windows:

```bat
cloud\agents\testing\run_agent_tests.bat
```

API:

```text
POST /agents/testing/run
GET  /agents/testing/report
```

Documentation:

```text
docs/AGENT_TESTING_TOOLS.md
```
By relying on a lightweight local RuleEngine and BigQueryMLInference model for initial triage, the system minimizes carbon-intensive LLM API calls, only invoking the generative GeminiNPL engine for high-risk anomalies or explicit investigations. The platform leverages GCP Secret Manager and Workload Identity for zero-trust security, ensuring no hardcoded credentials exist.
