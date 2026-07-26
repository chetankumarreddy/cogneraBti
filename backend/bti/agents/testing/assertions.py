from typing import Dict, Any, List

class AgentAssertions:
    @staticmethod
    def contains_required_terms(text: str, terms: List[str]) -> Dict[str, Any]:
        checks = {term: term.lower() in text.lower() for term in terms}
        return {"passed": all(checks.values()), "checks": checks}

    @staticmethod
    def no_unsupported_speculation(text: str) -> Dict[str, Any]:
        blocked = ["probably", "assume", "assumed", "must have intended", "appears to intend"]
        findings = [term for term in blocked if term in text.lower()]
        return {"passed": not findings, "findings": findings}

    @staticmethod
    def requires_human_review_when_low_confidence(text: str, confidence: float) -> Dict[str, Any]:
        if confidence >= 0.60:
            return {"passed": True, "reason": "confidence above threshold"}
        passed = "human review required" in text.lower()
        return {"passed": passed, "reason": "mandatory human review phrase for low confidence"}

    @staticmethod
    def has_evidence_reference(payload: Dict[str, Any]) -> Dict[str, Any]:
        txn_id = payload.get("transaction", {}).get("txn_id") or payload.get("prompt_payload", {}).get("evidence_summary", {}).get("txn_id")
        return {"passed": bool(txn_id), "txn_id": txn_id}
