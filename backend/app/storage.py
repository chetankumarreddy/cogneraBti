import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'data'; EVID=ROOT/'evidence'; EVID.mkdir(exist_ok=True)
def load(name): return json.loads((DATA/name).read_text())
def all_txns(): return load('transactions_train.json')+load('transactions_test.json')
def find(search_type,value):
    key={'transaction_id':'txn_id','transaction_hash':'txn_hash','block_hash':'block_hash'}.get(search_type,'txn_id')
    return next((r for r in all_txns() if str(r.get(key,'')).lower()==value.lower()),None)
def save_ev(txn_id,ev): (EVID/f'{txn_id}.json').write_text(json.dumps(ev,indent=2,default=str))
def get_ev(txn_id):
    p=EVID/f'{txn_id}.json'; return json.loads(p.read_text()) if p.exists() else None
def list_cases():
    p=EVID/'cases.json'; return json.loads(p.read_text()) if p.exists() else []
def save_cases(cases): (EVID/'cases.json').write_text(json.dumps(cases,indent=2))
