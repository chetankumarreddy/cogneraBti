from typing import Dict, Any
from bti.ml.model_router import MLModelRouter

class MLInference:
    def __init__(self):
        self.router = MLModelRouter()

    def score(self, txn: Dict[str, Any]) -> Dict[str, Any]:
        return self.router.score(txn)
