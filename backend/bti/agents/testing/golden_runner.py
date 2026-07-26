import json
from pathlib import Path
from typing import Dict, Any, List
from bti.agents.testing.agent_test_harness import AgentTestHarness

class GoldenTestRunner:
    def __init__(self, cases_path: str = "tests/fixtures/agent_golden_cases.json"):
        self.root = Path(__file__).resolve().parents[4]
        self.cases_path = self.root / cases_path
        self.harness = AgentTestHarness()

    def load_cases(self) -> List[Dict[str, Any]]:
        return json.loads(self.cases_path.read_text(encoding="utf-8"))

    def run(self) -> Dict[str, Any]:
        results = [self.harness.run_case(case) for case in self.load_cases()]
        summary = {
            "total": len(results),
            "passed": sum(1 for item in results if item["passed"]),
            "failed": sum(1 for item in results if not item["passed"]),
            "results": results
        }
        out_dir = self.root / "tests" / "reports"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "agent_test_report.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        return summary
