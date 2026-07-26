import os
from typing import Any, Dict
from bti.ml.local_isolation import LocalIsolationModel
from bti.ml.bigquery_ml import BigQueryMLAdapter

class MLModelRouter:
    def __init__(self):
        self.mode = os.getenv("BTI_ML_MODE", "local")
        self.local = LocalIsolationModel()
        self.bqml = BigQueryMLAdapter()

    def status(self) -> Dict[str, Any]:
        return {"mode": self.mode, "local": "enabled", "bigquery_ml": self.bqml.status(), "fallback": "local_isolation_fallback"}

    def score(self, txn: Dict[str, Any]) -> Dict[str, Any]:
        # For hackathon runtime, score locally even when BigQuery ML is configured.
        # BigQuery ML SQL is generated for cloud training/scoring workflows.
        local_score = self.local.score(txn)
        return {"runtime": "local" if self.mode != "bigquery_ml" else "local_fallback", "local_score": local_score, "bigquery_ml": self.bqml.status()}
