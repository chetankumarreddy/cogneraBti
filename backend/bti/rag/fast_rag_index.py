import json
import math
from pathlib import Path
from typing import Any, Dict, List
from bti.rag.embeddings import LocalEmbeddingModel

class FastRAGIndex:
    def __init__(self, index_path: str = "model_vault/rag_index.json"):
        self.root = Path(__file__).resolve().parents[3]
        self.index_path = self.root / index_path
        self.embedder = LocalEmbeddingModel()
        self.documents: List[Dict[str, Any]] = []
        if self.index_path.exists():
            self.documents = json.loads(self.index_path.read_text(encoding="utf-8"))

    def _cosine(self, a: List[float], b: List[float]) -> float:
        return sum(x * y for x, y in zip(a, b)) / ((math.sqrt(sum(x*x for x in a)) or 1.0) * (math.sqrt(sum(y*y for y in b)) or 1.0))

    def add_document(self, doc_id: str, text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        item = {"doc_id": doc_id, "text": text, "metadata": metadata, "embedding": self.embedder.embed(text)}
        self.documents = [d for d in self.documents if d["doc_id"] != doc_id]
        self.documents.append(item)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(self.documents, indent=2), encoding="utf-8")
        return {"doc_id": doc_id, "indexed": True}

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        q = self.embedder.embed(query)
        scored = []
        for doc in self.documents:
            scored.append({"score": round(self._cosine(q, doc["embedding"]), 4), "doc_id": doc["doc_id"], "text": doc["text"], "metadata": doc["metadata"]})
        return sorted(scored, key=lambda x: x["score"], reverse=True)[:top_k]

    def status(self) -> Dict[str, Any]:
        return {"index_path": str(self.index_path), "document_count": len(self.documents), "embedding_model": "local_hash_embeddings"}
