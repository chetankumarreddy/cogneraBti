from typing import Dict, Any, List

class RiskCompass:
    def score(self, rules: List[Dict[str, Any]], ml: Dict[str, Any], graph: Dict[str, Any], confidence: float = 0.88) -> Dict[str, Any]:
        rule_score = min(sum(float(rule.get("weight", 10)) for rule in rules), 75)
        ml_score = float(ml.get("local_score", ml).get("anomaly_score", 0)) * 15 if isinstance(ml, dict) else 0
        graph_score = float(graph.get("graph_risk", 0))
        score = min(100, int(rule_score + ml_score + graph_score))
        level = "Critical" if score >= 85 else "High" if score >= 65 else "Medium" if score >= 35 else "Low"
        return {
            "risk_score": score,
            "risk_level": level,
            "confidence": confidence,
            "human_review_required": score >= 65 or confidence < 0.60,
            "risk_contributors": [r.get("rule_id") for r in rules] + graph.get("signals", [])
        }
