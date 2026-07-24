CREATE OR REPLACE MODEL `PROJECT_ID.DATASET.txn_anomaly_kmeans`
OPTIONS(model_type='kmeans', num_clusters=4, standardize_features=true) AS
SELECT
  CAST(amount AS FLOAT64) AS amount,
  CAST(balance_percentage_moved AS FLOAT64) AS balance_percentage_moved,
  CAST(velocity_24h AS FLOAT64) AS velocity_24h,
  CAST(first_time_receiver AS INT64) AS first_time_receiver,
  CAST(CASE WHEN kyc_status = 'missing' THEN 1 ELSE 0 END AS INT64) AS kyc_missing
FROM `PROJECT_ID.DATASET.transactions_train`;
