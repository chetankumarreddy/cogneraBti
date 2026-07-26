from typing import Any, Dict
from bti.rag.fast_rag_index import FastRAGIndex

class EvidenceRetriever:
    def __init__(self):
        self.index = FastRAGIndex()

    def enrich(self, transaction: Dict[str, Any], top_k: int = 5) -> Dict[str, Any]:
        query = " ".join(str(transaction.get(k, "")) for k in ["entity", "from_wallet", "to_wallet", "function", "oracle_address", "event_type"])
        return {"query": query, "matches": self.index.search(query, top_k=top_k), "index_status": self.index.status()}
