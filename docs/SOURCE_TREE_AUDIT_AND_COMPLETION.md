# Cognira BTI Source Tree Audit and Completion

## Required source tree coverage

The package has been checked against the requested source tree and the missing components have been added.

```text
Cognira_BTI_Hackathon/
├── frontend/
├── backend/
├── middleware/
├── data/
├── model_vault/
├── control_room/
├── docs/
├── evidence/
├── scripts/
├── forge_models.py
├── requirements.txt
├── requirements-api-optional.txt
└── README.md
```

## Backend module coverage

```text
backend/bti/core/
├── chainprint.py
├── rule_alchemist.py
├── relationship_atlas.py
├── risk_compass.py
└── triad_referee.py

backend/bti/ml/
├── signal_forge.py
├── ml_trainer.py
├── ml_inference.py
├── local_isolation.py
├── bigquery_ml.py
└── model_router.py

backend/bti/rag/
├── rag_corpus.py
├── fast_rag_index.py
├── embeddings.py
└── retriever.py

backend/bti/llm/
├── npl_engine.py
├── prompt_chain.py
├── story_guardian.py
├── gemini_agent.py
├── local_llm.py
└── narrative_forge.py

backend/bti/security/
└── money_flow_graph.py

backend/bti/audit/
└── fca_exporter.py

backend/bti/middleware/
└── pipeline_gateway.py

backend/bti/agents/
├── agent_manifest.py
├── agent_runtime_client.py
├── cognira_agent.py
├── eval_runner.py
└── tool_registry.py
```

## Added agent development tools

```text
cloud/agents/
├── README.md
├── agent_manifest.yaml
├── agents_cli_setup.sh
├── deploy_agent_runtime.sh
├── run_agent_eval.sh
├── run_agent_local.sh
├── cognira_bti_agent/
│   ├── agent.py
│   └── agent_engine_app.py
└── evals/
    └── eval_cases.json
```

## Added API endpoints

```text
GET  /agents/manifest
GET  /agents/runtime/status
POST /agents/analyse/{txn_id}
POST /agents/evaluate
GET  /llm/narrative-agent/status
POST /llm/narrative-agent/generate/{txn_id}
POST /rag/index/build
GET  /rag/index/status
GET  /rag/search
GET  /ml/runtime/status
GET  /ml/bigquery/sql/create-model
GET  /ml/bigquery/sql/detect-anomalies
GET  /cloud/runtime
```
