import json
from pathlib import Path
from typing import Dict, Any
from bti.rag.fast_rag_index import FastRAGIndex

class RAGCorpusBuilder:
    def __init__(self):
        self.root = Path(__file__).resolve().parents[3]
        self.data_dir = self.root / "data"
        self.index = FastRAGIndex()

    def build_default_index(self) -> Dict[str, Any]:
        files = ["entity_registry.json", "wallet_registry.json", "oracle_registry.json", "policy_registry.json"]
        count = 0
        for name in files:
            path = self.data_dir / name
            if not path.exists():
                continue
            records = json.loads(path.read_text(encoding="utf-8"))
            for i, record in enumerate(records):
                doc_id = f"{name}:{i}"
                text = json.dumps(record, sort_keys=True)
                self.index.add_document(doc_id, text, {"source_file": name})
                count += 1
        return {"indexed_records": count, "status": self.index.status()}
