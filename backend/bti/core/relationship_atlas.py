from typing import Dict, Any, List
try:
    import networkx as nx
except Exception:
    nx = None

class RelationshipAtlas:
    def build(self, txn: Dict[str, Any], transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        related = [t for t in transactions if t.get("entity_id") == txn.get("entity_id")][-80:]
        if nx:
            graph = nx.DiGraph()
            for item in related:
                graph.add_edge(item.get("from_wallet"), item.get("to_wallet"), amount=item.get("amount"), txn_id=item.get("txn_id"))
            cycles = list(nx.simple_cycles(graph))[:5]
            return {
                "nodes": [{"id": node, "label": node} for node in graph.nodes],
                "edges": [{"from": u, "to": v, "amount": graph.edges[u, v].get("amount")} for u, v in graph.edges],
                "cycles": cycles,
                "graph_risk": 10 if cycles else 0,
                "signals": ["Circular movement detected"] if cycles else []
            }
        nodes = sorted(set([x for item in related for x in [item.get("from_wallet"), item.get("to_wallet")] if x]))
        return {
            "nodes": [{"id": node, "label": node} for node in nodes],
            "edges": [{"from": item.get("from_wallet"), "to": item.get("to_wallet"), "amount": item.get("amount")} for item in related],
            "cycles": [],
            "graph_risk": 0,
            "signals": ["NetworkX unavailable, used lightweight graph fallback"]
        }
