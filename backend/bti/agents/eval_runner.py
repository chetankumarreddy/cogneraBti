from typing import Dict, Any, List
from bti.agents.cognira_agent import CogniraBTIAgent

DEFAULT_EVALS = [
    {"txn_id": "TXN-000421", "persona": "fca_examiner", "must_contain": ["Human review", "Risk", "Confidence"]},
    {"txn_id": "TXN-000423", "persona": "compliance_officer", "must_contain": ["KYC", "Recommendation"]}
]

class AgentEvalRunner:
    def __init__(self):
        self.agent = CogniraBTIAgent()

    def run(self, cases: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
        cases = cases or DEFAULT_EVALS
        results = []
        for case in cases:
            narrative = self.agent.generate_narrative(case["txn_id"], case.get("persona", "compliance_officer"))
            text = narrative.get("text", "")
            checks = {term: term.lower() in text.lower() for term in case.get("must_contain", [])}
            results.append({"case": case, "passed": all(checks.values()), "checks": checks})
        return {"total": len(results), "passed": sum(1 for r in results if r["passed"]), "results": results}
