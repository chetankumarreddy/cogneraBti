from typing import Any, Dict, List
from bti.ml.signal_forge import engineer_features

class LocalIsolationModel:
    def score(self, txn: Dict[str, Any]) -> Dict[str, Any]:
        f = engineer_features(txn)
        score = 0.0
        score += min(f["amount"] / 50000000, 1.0) * 0.35
        score += min(f["balance_percentage_moved"] / 100, 1.0) * 0.30
        score += f["is_weekend"] * 0.10
        score += min(f["velocity_24h"] / 15, 1.0) * 0.15
        score += f["first_time_receiver"] * 0.05
        score += f["kyc_missing"] * 0.05
        score = round(min(score, 1.0), 4)
        return {"model": "local_isolation_fallback", "anomaly_score": score, "is_anomaly": score >= 0.55, "features": f}
