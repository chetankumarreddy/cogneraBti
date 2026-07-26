import json
from pathlib import Path

class MLTrainer:
    def __init__(self):
        self.root = Path(__file__).resolve().parents[3]
        self.model_card = self.root / "model_vault" / "model_card.json"

    def train_local(self):
        self.model_card.parent.mkdir(exist_ok=True)
        payload = {
            "model": "local_isolation_fallback",
            "purpose": "Hackathon-safe contextual blockchain anomaly scoring",
            "features": ["amount", "hour", "is_weekend", "balance_percentage_moved", "velocity_24h", "first_time_receiver", "kyc_missing"],
            "status": "ready"
        }
        self.model_card.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return payload

if __name__ == "__main__":
    print(MLTrainer().train_local())
