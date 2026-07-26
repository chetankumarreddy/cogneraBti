import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime
from app.schemas import *
from app.cloud_runtime import cloud_runtime_status
from app import storage
from bti.middleware.pipeline_gateway import PipelineGateway
from bti.core.rule_alchemist import RuleAlchemist
from bti.audit.fca_exporter import FCAExporter

from bti.llm.narrative_forge import NarrativeForge
from bti.rag.rag_corpus import RAGCorpusBuilder
from bti.rag.retriever import EvidenceRetriever
from bti.ml.model_router import MLModelRouter

from bti.agents import CogniraBTIAgent, AgentEvalRunner, COGNIRA_AGENT_MANIFEST
from bti.agents.agent_runtime_client import AgentRuntimeClient
from bti.agents.testing.golden_runner import GoldenTestRunner
app=FastAPI(title='Cognira BTI API',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])
pipe=PipelineGateway(); rules=RuleAlchemist(); exp=FCAExporter()
narrative_forge = NarrativeForge()
rag_builder = RAGCorpusBuilder()
rag_retriever = EvidenceRetriever()
ml_router = MLModelRouter()
cognira_agent = CogniraBTIAgent()
agent_runtime_client = AgentRuntimeClient()
@app.get('/health')
def health(): return {'status':'ok','platform':'Cognira BTI'}
@app.post('/analyse')
def analyse(req:AnalyseRequest):
 r=pipe.analyse(req.search_type,req.value,req.persona)
 if r.get('error'): raise HTTPException(404,r)
 return r
@app.get('/alerts')
def alerts(limit:int=50): return [{'txn_id':t['txn_id'],'entity':t['entity'],'amount':t['amount'],'timestamp':t['timestamp'],'risk':{'risk_level':'Review'},'rules':['candidate']} for t in storage.all_txns()[-limit:]]
@app.post('/chat')
def chat(req:ChatRequest):
 ev=storage.get_ev(req.txn_id) if req.txn_id else None
 if not ev: raise HTTPException(404,'Evidence not found')
 return {'answer':f"Risk is {ev['risk']['risk_level']} due to {', '.join(r['rule_id'] for r in ev['rules']) or 'no material rules'}. Confidence {ev['risk']['confidence']}", 'evidence_refs':[ev['transaction']['txn_id']]}
@app.post('/feedback')
def feedback(req:FeedbackRequest): return {'status':'captured','feedback':req.model_dump(),'created_at':datetime.utcnow().isoformat()+'Z'}
@app.get('/retrain-status')
def retrain(): return {'ready':True,'next_action':'Governance approval before retraining'}
@app.get('/model-stability')
def stability(): return {'model':'IsolationForest-demo','status':'stable','drift_status':'monitoring'}
@app.get('/rules')
def get_rules(): return rules.list_rules()
@app.post('/rules/update')
def update(req:RuleUpdateRequest): return rules.update_rule(req.rule_id,req.model_dump())
@app.get('/evidence/{txn_id}')
def evidence(txn_id:str):
 ev=storage.get_ev(txn_id)
 if not ev: raise HTTPException(404,'Run /analyse first')
 return ev
@app.post('/cases/{txn_id}')
def create_case(txn_id:str):
 cases=storage.list_cases(); case={'case_id':f'CASE-{len(cases)+1:05d}','txn_id':txn_id,'status':'Open','created_at':datetime.utcnow().isoformat()+'Z'}; cases.append(case); storage.save_cases(cases); return case
@app.get('/cases')
def cases(): return storage.list_cases()
@app.post('/export/fca/pdf')
def pdf(req:ExportRequest): return FileResponse(exp.export_pdf([storage.get_ev(x) for x in req.txn_ids if storage.get_ev(x)]),filename='cognira_bti_fca_export.pdf')
@app.post('/export/fca/csv')
def csv(req:ExportRequest): return FileResponse(exp.export_csv([storage.get_ev(x) for x in req.txn_ids if storage.get_ev(x)]),filename='cognira_bti_fca_export.csv')


@app.get('/cloud/runtime')
def cloud_runtime():
    return cloud_runtime_status()


@app.get('/llm/narrative-agent/status')
def narrative_agent_status():
    return narrative_forge.runtime_status()

@app.post('/llm/narrative-agent/generate/{txn_id}')
def narrative_agent_generate(txn_id: str, persona: str = 'compliance_officer'):
    ev = storage.get_ev(txn_id)
    if not ev:
        ev = pipe.analyse('transaction_id', txn_id, persona)
    return narrative_forge.generate(ev, persona)

@app.post('/rag/index/build')
def rag_index_build():
    return rag_builder.build_default_index()

@app.get('/rag/index/status')
def rag_index_status():
    return rag_retriever.index.status()

@app.get('/rag/search')
def rag_search(q: str, top_k: int = 5):
    return {'query': q, 'matches': rag_retriever.index.search(q, top_k)}

@app.get('/ml/runtime/status')
def ml_runtime_status():
    return ml_router.status()

@app.get('/ml/bigquery/sql/create-model')
def bqml_create_model_sql():
    return {'sql': ml_router.bqml.create_model_sql()}

@app.get('/ml/bigquery/sql/detect-anomalies')
def bqml_detect_anomalies_sql(table_name: str = 'transactions_scoring'):
    return {'sql': ml_router.bqml.detect_anomalies_sql(table_name)}


@app.get('/agents/manifest')
def agents_manifest():
    return COGNIRA_AGENT_MANIFEST

@app.get('/agents/runtime/status')
def agents_runtime_status():
    return agent_runtime_client.status()

@app.post('/agents/analyse/{txn_id}')
def agents_analyse(txn_id: str, persona: str = 'compliance_officer'):
    return cognira_agent.analyse_transaction(txn_id, persona)

@app.post('/agents/evaluate')
def agents_evaluate():
    return AgentEvalRunner().run()


@app.post('/agents/testing/run')
def agents_testing_run():
    return GoldenTestRunner().run()

@app.get('/agents/testing/report')
def agents_testing_report():
    report = Path(__file__).resolve().parents[2] / 'tests' / 'reports' / 'agent_test_report.json'
    if not report.exists():
        return {'status': 'not-run', 'message': 'Run POST /agents/testing/run first'}
    return json.loads(report.read_text(encoding='utf-8'))
