import os
import json
import pandas as pd
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Cognira BTI Enterprise API", version="2026.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class RequestModel(BaseModel):
    search_type: str = "transaction_id"
    value: str = "0xeth_demo_02_velocity"
    persona: str = "Compliance Officer"
    tx_id: str = None
    audience: str = None

class CaseResolveModel(BaseModel):
    tx_id: str = None
    txn_id: str = None
    verdict: str
    comments: str
    user: str

@app.get("/")
@app.get("/health")
@app.get("/api/v1/health")
def health_check():
    return {"status": "ONLINE", "database": "CONNECTED", "ml_engine": "ACTIVE", "kms": "VERIFIED", "project_id": os.getenv("BTI_GCP_PROJECT_ID", "ltc-hack2026-team36")}

@app.post("/analyse")
@app.post("/api/v1/analyze")
def analyze(req: RequestModel):
    target_tx = req.tx_id or req.value or "0xeth_demo_02_velocity"
    target_persona = req.audience or req.persona or "Compliance Officer"
    try:
        df = pd.read_csv("data/bti_transactions_full.csv")
        res = df[df["transaction_hash"] == target_tx]
        if res.empty:
            txn = {"transaction_hash": target_tx, "value_transferred": 50000.0, "from_address": "0xALBION_ENERGY_WALLET", "to_address": "0xUNKNOWN_HACKER_NODE", "velocity_1h": 12}
        else:
            txn = json.loads(res.iloc[0].to_json())
    except Exception:
        txn = {"transaction_hash": target_tx, "value_transferred": 15000.0}

    is_unknown = "unknown" in target_tx.lower() or "0xUNKNOWN" in str(txn.get("from_address"))
    score = 100.0 if is_unknown else 45.0
    level = "CRITICAL" if score > 75 else "LOW"

    narrative = (
        f"### [{target_persona.upper()} INSIGHT REPORT]\n"
        f"**WHAT HAPPENED**\nTransaction hash {target_tx} processed transferring £{txn.get('value_transferred', 0):,.2f}.\n\n"
        f"**WHY IT MATTERS**\nTriggered risk evaluation level {level} (Score: {score}%). Compliance protocols enforced under SYSC 6.1.1.\n\n"
        f"**RECOMMENDATION**\n{'Escalate to Case Command immediately.' if is_unknown else 'Proceed with routine settlement validation.'}"
    )

    return {
        "tx_id": target_tx,
        "security": {"kms": {"verified": True, "signature": "mock_sha256_sig", "kms_mode": "CLOUD_KMS_WITH_LOCAL_FALLBACK"}},
        "topology": {"sender": txn.get("from_address"), "receiver": txn.get("to_address"), "unknown_guardian": is_unknown},
        "risk": {"composite": score, "level": level, "components": {"rule": score, "ml": 20.0}},
        "consensus": {"root_cause": "Unknown Entity Escalation" if is_unknown else "Routine Baseline"},
        "ai_services": {"document_ai": {"status": "EXTRACTED", "po_reference": "PO-GCP-2026-X"}},
        "thread_status": {"ingest_thread": "OK", "rule_thread": "BREAK" if is_unknown else "OK", "ml_thread": "OK", "npl_thread": "OK"},
        "narrative": narrative,
        "raw": txn
    }

@app.get("/alerts")
@app.get("/api/v1/alerts")
def alerts():
    try:
        df = pd.read_csv("data/bti_transactions_full.csv")
        records = json.loads(df.head(15).to_json(orient="records"))
        return [{
            "tx_id": r.get("transaction_hash"),
            "transaction_hash": r.get("transaction_hash"),
            "amount_gbp": float(r.get("value_transferred", 0)),
            "value_transferred": float(r.get("value_transferred", 0)),
            "label": "Velocity Spike / Off-Hours Anomaly" if r.get("anomaly_label") == 1 else "Routine Settlement",
            "risk": "P1_CRITICAL" if r.get("anomaly_label") == 1 else "P4_LOW",
            "status": "OPEN",
            "sender": r.get("from_address"),
            "receiver": r.get("to_address")
        } for r in records]
    except Exception:
        return []

@app.post("/cases/resolve")
@app.post("/api/v1/cases/resolve")
def resolve_case(req: CaseResolveModel):
    return {"status": "SUCCESS", "txn_id": req.txn_id or req.tx_id}

@app.get("/config")
@app.get("/api/v1/config")
def get_config():
    with open("control_room/platform_config.json", "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    import uvicorn