from typing import Dict, Any

class MoneyFlowGraph:
    def analyse(self, graph: Dict[str, Any]) -> Dict[str, Any]:
        edges = graph.get("edges", [])
        nodes = graph.get("nodes", [])
        return {
            "counterparty_count": len(nodes),
            "movement_count": len(edges),
            "layering_detected": len(edges) >= 3,
            "circular_movement_detected": bool(graph.get("cycles")),
            "signals": graph.get("signals", [])
        }
