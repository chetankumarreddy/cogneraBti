import os
from typing import Any, Dict

class LocalLLMAdapter:
    def __init__(self):
        self.mode = os.getenv("BTI_LOCAL_LLM_MODE", "template")
        self.ollama_endpoint = os.getenv("BTI_OLLAMA_ENDPOINT", "http://localhost:11434")
        self.ollama_model = os.getenv("BTI_OLLAMA_MODEL", "llama3.1")

    def status(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "ollama_endpoint": self.ollama_endpoint,
            "ollama_model": self.ollama_model,
            "fallback": "deterministic_template"
        }

    def generate_template(self, evidence: Dict[str, Any], persona: str) -> str:
        tx = evidence.get("transaction", {})
        risk = evidence.get("risk", {})
        rules = ", ".join([r.get("rule_id", "") for r in evidence.get("rules", [])]) or "No material rules triggered"
        confidence = risk.get("confidence", 0.0)
        low_conf = " I don’t know. Human review required." if confidence < 0.60 else ""
        review_required = bool(risk.get("human_review_required"))
        review_suffix = " Human review required." if review_required else ""
        return "\n".join([
            f"What happened: {tx.get('entity', 'Unknown entity')} executed {tx.get('function')} on {tx.get('contract_name')} for {tx.get('amount')} {tx.get('currency')}.",
            f"Why it matters: Risk is {risk.get('risk_level')} with rules triggered: {rules}.",
            f"How it happened: Source wallet {tx.get('from_wallet')} interacted with destination wallet {tx.get('to_wallet')} on {tx.get('chain')}.",
            f"Confidence: {confidence}.{low_conf}",
            "Impact: Potential compliance, audit, financial crime and FCA evidence relevance.",
            "Recommendation: Validate client instruction, KYC state, oracle provenance and retain evidence lineage." + review_suffix
        ])
