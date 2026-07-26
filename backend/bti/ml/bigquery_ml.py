import os
from typing import Any, Dict

class BigQueryMLAdapter:
    def __init__(self):
        self.project_id = os.getenv("BTI_GCP_PROJECT_ID", "")
        self.dataset = os.getenv("BTI_BIGQUERY_DATASET", "cognira_bti")
        self.model_name = os.getenv("BTI_BQML_MODEL", "txn_anomaly_kmeans")
        self.enabled = os.getenv("BTI_ML_MODE", "local") in {"bigquery_ml", "bigquery_ml_with_local_fallback"}

    @property
    def model_fqn(self) -> str:
        return f"`{self.project_id}.{self.dataset}.{self.model_name}`"

    def create_model_sql(self) -> str:
        return f"""
CREATE OR REPLACE MODEL {self.model_fqn}
OPTIONS(model_type='kmeans', num_clusters=4, standardize_features=true) AS
SELECT
  CAST(amount AS FLOAT64) AS amount,
  CAST(balance_percentage_moved AS FLOAT64) AS balance_percentage_moved,
  CAST(velocity_24h AS FLOAT64) AS velocity_24h,
  CAST(first_time_receiver AS INT64) AS first_time_receiver,
  CAST(CASE WHEN kyc_status = 'missing' THEN 1 ELSE 0 END AS INT64) AS kyc_missing
FROM `{self.project_id}.{self.dataset}.transactions_train`;
""".strip()

    def detect_anomalies_sql(self, table_name: str = "transactions_scoring") -> str:
        return f"""
SELECT *
FROM ML.DETECT_ANOMALIES(
  MODEL {self.model_fqn},
  STRUCT(0.80 AS contamination),
  (SELECT * FROM `{self.project_id}.{self.dataset}.{table_name}`)
);
""".strip()

    def status(self) -> Dict[str, Any]:
        return {"enabled": self.enabled, "project_id_present": bool(self.project_id), "dataset": self.dataset, "model": self.model_name, "model_fqn": self.model_fqn}
