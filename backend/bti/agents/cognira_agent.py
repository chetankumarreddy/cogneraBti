from typing import Dict, Any
from app import storage
from bti.middleware.pipeline_gateway import PipelineGateway
from bti.llm.narrative_forge import NarrativeForge
from bti.rag.retriever import EvidenceRetriever
from bti.ml.model_router import MLModelRouter

class CogniraBTIAgent:
    """Local ADK-style agent facade for transaction intelligence workflows."""
    def __init__(self):
        self.pipeline = PipelineGateway()
        self.narrative = NarrativeForge()
        self.retriever = EvidenceRetriever()
        self.ml = MLModelRouter()

    def analyse_transaction(self, txn_id: str, persona: str = "compliance_officer") -> Dict[str, Any]:
        evidence = self.pipeline.analyse("transaction_id", txn_id, persona)
        return evidence

    def generate_narrative(self, txn_id: str, persona: str = "fca_examiner") -> Dict[str, Any]:
        # Re-analyse to avoid stale evidence when rules, scoring or test fixtures change.
        evidence = self.pipeline.analyse("transaction_id", txn_id, persona)
        return self.narrative.generate(evidence, persona)

    def retrieve_context(self, query: str) -> Dict[str, Any]:
        return {"query": query, "matches": self.retriever.index.search(query)}

    def explain_model(self, txn_id: str) -> Dict[str, Any]:
        txn = storage.find("transaction_id", txn_id)
        if not txn:
            return {"error": "Transaction not found"}
        return self.ml.score(txn)
