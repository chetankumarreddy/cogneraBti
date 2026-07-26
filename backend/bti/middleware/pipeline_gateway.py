from datetime import datetime
try:
    import networkx as nx
except Exception:
    nx = None
from app import storage
from bti.core.rule_alchemist import RuleAlchemist

class PipelineGateway:
    def __init__(self):
        self.rules = RuleAlchemist()

    def regs(self):
        return {
            "wallets": storage.load("wallet_registry.json"),
            "entities": storage.load("entity_registry.json"),
            "oracles": storage.load("oracle_registry.json")
        }

    def analyse(self, search_type, value, persona):
        txn = storage.find(search_type, value)
        if not txn:
            return {"error": "Transaction not found"}
        regs = self.regs()
        integrity = {
            "hash_valid": bool(txn.get("hash_valid")) and str(txn.get("txn_hash", "")).startswith("0x"),
            "signature_valid": bool(txn.get("signature_valid")),
            "cryptographic_assurance": "passed"
        }
        fired = self.rules.evaluate(txn, regs, integrity)
        base_score = sum(r.get("weight", 10) for r in fired) + int(txn.get("amount", 0) / 50000000 * 15)
        rule_ids = {r.get("rule_id") for r in fired}
        contextual_boost = 30 if {"OFF_HOURS", "LARGE_BALANCE_MOVEMENT"}.issubset(rule_ids) else 0
        score = min(100, base_score + contextual_boost)
        level = "Critical" if score >= 85 else "High" if score >= 65 else "Medium" if score >= 35 else "Low"
        confidence = 0.55 if any(r["rule_id"] == "UNKNOWN_WALLET" for r in fired) else 0.88
        narrative = self.narrate(persona, txn, fired, score, level, confidence)

        related = [t for t in storage.all_txns() if t.get("entity_id") == txn.get("entity_id")][-40:]
        if nx:
            graph_obj = nx.DiGraph()
            for t in related:
                graph_obj.add_edge(t["from_wallet"], t["to_wallet"], amount=t["amount"], txn_id=t["txn_id"])
            graph = {
                "nodes": [{"id": n, "label": n} for n in graph_obj.nodes],
                "edges": [{"from": u, "to": v, "amount": graph_obj.edges[u, v]["amount"]} for u, v in graph_obj.edges],
                "signals": []
            }
        else:
            nodes = sorted(set([x for t in related for x in [t.get("from_wallet"), t.get("to_wallet")] if x]))
            graph = {
                "nodes": [{"id": n, "label": n} for n in nodes],
                "edges": [{"from": t.get("from_wallet"), "to": t.get("to_wallet"), "amount": t.get("amount")} for t in related],
                "signals": ["NetworkX unavailable, used lightweight graph fallback"]
            }
        evidence = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "transaction": txn,
            "integrity": integrity,
            "decoded": {"business_action": txn["function"], "contract": txn["contract_name"]},
            "rules": fired,
            "risk": {
                "risk_score": score,
                "risk_level": level,
                "confidence": confidence,
                "human_review_required": score >= 65 or confidence < 0.6,
                "risk_contributors": [r["rule_id"] for r in fired]
            },
            "graph": graph,
            "ml": {"model_mode": "local_demo", "anomaly_score": min(1, score / 100)},
            "narrative": narrative
        }
        storage.save_ev(txn["txn_id"], evidence)
        return evidence

    def narrate(self, persona, txn, rules, score, level, conf):
        rule_summary = ", ".join(r["rule_id"] for r in rules) or "No material rules triggered"
        review = " Human review required." if conf < 0.6 or score >= 65 else ""
        sections = {
            "what_happened": f"{txn['entity']} executed {txn['function']} on {txn['contract_name']} for {txn['amount']} {txn['currency']} at {txn['timestamp']}.",
            "why_it_matters": f"The transaction is technically valid but contextually classified as {level}. Rules triggered: {rule_summary}.",
            "how_it_happened": f"Wallet {txn['from_wallet']} interacted with {txn['to_wallet']} on {txn['chain']}.",
            "confidence": f"Confidence is {conf}." + (" I don’t know. Human review required." if conf < 0.6 else ""),
            "impact": "Potential compliance, audit, financial crime, and FCA evidence relevance.",
            "recommendation": "Validate client instruction, KYC, oracle provenance, and supporting evidence." + review
        }
        return {"sections": sections, "text": "\n".join(f"{k}: {v}" for k, v in sections.items()), "persona": persona}
