from typing import Dict, Any, List

class TriadReferee:
    def decide(self, rules: List[Dict[str, Any]], ml: Dict[str, Any], graph: Dict[str, Any]) -> Dict[str, Any]:
        votes = {
            "rules": bool(rules),
            "ml": bool(ml.get("local_score", ml).get("is_anomaly", False)) if isinstance(ml, dict) else False,
            "graph": bool(graph.get("signals"))
        }
        vote_count = sum(1 for value in votes.values() if value)
        return {"votes": votes, "consensus": vote_count >= 2, "decision_basis": f"{vote_count}/3 intelligence engines signalled risk"}
