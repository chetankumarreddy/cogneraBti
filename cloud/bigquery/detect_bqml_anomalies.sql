SELECT *
FROM ML.DETECT_ANOMALIES(
  MODEL `PROJECT_ID.DATASET.txn_anomaly_kmeans`,
  STRUCT(0.80 AS contamination),
  (SELECT * FROM `PROJECT_ID.DATASET.transactions_scoring`)
);
