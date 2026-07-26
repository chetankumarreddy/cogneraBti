from dataclasses import dataclass
from typing import Any, Dict, List

PERSONA_PROMPTS = {
    "compliance_officer": "Use UK compliance language. Focus on controls, risk, action and human review.",
    "relationship_manager": "Use client-safe business language. Avoid technical jargon and do not infer client intent.",
    "external_auditor": "Use formal audit evidence language. Focus on controls, evidence lineage and exceptions.",
    "fca_examiner": "Use concise FCA-oriented regulatory language. Focus on governance, control observations and limitations."
}

SYSTEM_GUARDRAILS = [
    "Never assume unknown entities.",
    "Use supplied evidence only.",
    "Do not infer intent.",
    "When confidence is insufficient, state: I don’t know. Human review required.",
    "Preserve evidence lineage and control mapping."
]

@dataclass
class PromptChain:
    persona: str
    evidence: Dict[str, Any]

    def build(self) -> Dict[str, Any]:
        rules = [r.get("rule_id") for r in self.evidence.get("rules", [])]
        risk = self.evidence.get("risk", {})
        tx = self.evidence.get("transaction", {})
        return {
            "system": "You are Cognira BTI, an enterprise Blockchain Transaction Intelligence narrative engine.",
            "guardrails": SYSTEM_GUARDRAILS,
            "persona": self.persona,
            "persona_instruction": PERSONA_PROMPTS.get(self.persona, PERSONA_PROMPTS["compliance_officer"]),
            "required_sections": ["What happened", "Why it matters", "How it happened", "Confidence", "Impact", "Recommendation"],
            "evidence_summary": {
                "txn_id": tx.get("txn_id"),
                "entity": tx.get("entity"),
                "chain": tx.get("chain"),
                "function": tx.get("function"),
                "amount": tx.get("amount"),
                "timestamp": tx.get("timestamp"),
                "rules": rules,
                "risk_level": risk.get("risk_level"),
                "confidence": risk.get("confidence"),
                "human_review_required": risk.get("human_review_required")
            }
        }
