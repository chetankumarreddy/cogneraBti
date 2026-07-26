from datetime import datetime
from typing import Dict, Any

def engineer_features(txn: Dict[str, Any]) -> Dict[str, float]:
    ts = datetime.fromisoformat(txn["timestamp"].replace("Z", "+00:00"))
    return {
        "amount": float(txn.get("amount", 0)),
        "hour": float(ts.hour),
        "is_weekend": 1.0 if ts.weekday() >= 5 else 0.0,
        "balance_percentage_moved": float(txn.get("balance_percentage_moved", 0)),
        "velocity_24h": float(txn.get("velocity_24h", 0)),
        "first_time_receiver": 1.0 if txn.get("first_time_receiver") else 0.0,
        "kyc_missing": 1.0 if txn.get("kyc_status") == "missing" else 0.0,
    }
