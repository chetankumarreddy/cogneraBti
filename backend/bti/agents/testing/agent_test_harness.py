from typing import Dict, Any
from bti.agents.cognira_agent import CogniraBTIAgent
from bti.agents.testing.assertions import AgentAssertions

class AgentTestHarness:
    def __init__(self):
        self.agent = CogniraBTIAgent()
        self.assertions = AgentAssertions()

    def run_case(self, case: Dict[str, Any]) -> Dict[str, Any]:
        txn_id = case["txn_id"]
        persona = case.get("persona", "compliance_officer")
        narrative = self.agent.generate_narrative(txn_id, persona)
        text = narrative.get("text", "")
        confidence = 0.0
        prompt_conf = narrative.get("prompt_payload", {}).get("evidence_summary", {}).get("confidence")
        if prompt_conf is not None:
            confidence = float(prompt_conf)
        checks = {
            "required_terms": self.assertions.contains_required_terms(text, case.get("must_contain", [])),
            "no_speculation": self.assertions.no_unsupported_speculation(text),
            "human_review_low_confidence": self.assertions.requires_human_review_when_low_confidence(text, confidence),
            "evidence_reference": self.assertions.has_evidence_reference(narrative)
        }
        return {
            "case_id": case.get("case_id", txn_id),
            "txn_id": txn_id,
            "persona": persona,
            "passed": all(item["passed"] for item in checks.values()),
            "checks": checks,
            "narrative_provider": narrative.get("llm_provider"),
            "narrative_preview": text[:700]
        }
