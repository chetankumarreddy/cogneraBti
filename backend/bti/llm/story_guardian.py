from typing import Dict, List

class StoryGuardian:
    def validate(self, text: str, confidence: float, evidence_refs: List[str]) -> Dict[str, object]:
        issues = []
        lower = text.lower()
        if confidence < 0.60 and "human review required" not in lower:
            issues.append("Low-confidence narrative missing mandatory human review statement")
        if "probably" in lower or "assume" in lower:
            issues.append("Speculative wording detected")
        if not evidence_refs:
            issues.append("Narrative has no evidence references")
        return {"passed": not issues, "issues": issues, "evidence_refs": evidence_refs}
