# Cognira BTI LLM, RAG, Local ML and BigQuery ML Architecture

## Narrative Forge

Narrative Forge is implemented under:

```text
backend/bti/llm/
├── gemini_agent.py
├── local_llm.py
├── narrative_forge.py
├── prompt_chain.py
└── story_guardian.py
```

It supports Gemini mode, local template fallback, persona prompt chaining and Story Guardian validation.

## Gemini Narrative Agent

The Gemini adapter is in:

```text
backend/bti/llm/gemini_agent.py
prompts/gemini_narrative_agent_prompt.json
control_room/llm_runtime.yaml
```

Runtime endpoint:

```text
GET /llm/narrative-agent/status
POST /llm/narrative-agent/generate/{txn_id}?persona=fca_examiner
```

Gemini Enterprise Agent Platform is intended for enterprise-grade agents grounded in enterprise data, and Google documents RAG Engine and Vector Search as relevant agent platform capabilities for grounding and retrieval. citeturn7search39turn7search41

## RAG Index

RAG is implemented under:

```text
backend/bti/rag/
├── embeddings.py
├── fast_rag_index.py
├── rag_corpus.py
└── retriever.py
```

Runtime endpoints:

```text
POST /rag/index/build
GET /rag/index/status
GET /rag/search?q=Albion Energy off-hours withdrawal
```

The hackathon RAG index uses deterministic local hash embeddings so it works offline. It can later evolve to Vertex Vector Search or BigQuery vector search.

## Local ML

Local ML is implemented under:

```text
backend/bti/ml/
├── signal_forge.py
├── local_isolation.py
└── model_router.py
```

Runtime endpoint:

```text
GET /ml/runtime/status
```

## BigQuery ML

BigQuery ML support is implemented under:

```text
backend/bti/ml/bigquery_ml.py
cloud/bigquery/create_bqml_anomaly_model.sql
cloud/bigquery/detect_bqml_anomalies.sql
control_room/ml_runtime.yaml
```

Runtime endpoints:

```text
GET /ml/bigquery/sql/create-model
GET /ml/bigquery/sql/detect-anomalies
```

BigQuery ML lets teams create and train models in BigQuery using SQL, and Google documents `CREATE MODEL`, `ML.EVALUATE`, and `ML.PREDICT` style workflows for BigQuery ML. citeturn7search45turn7search46
