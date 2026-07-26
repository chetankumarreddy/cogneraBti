import yaml
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parents[3]
class RuleAlchemist:
 def __init__(self): self.path=ROOT/'control_room'/'rules.yaml'; self.rules=yaml.safe_load(self.path.read_text())['rules']
 def list_rules(self): return self.rules
 def update_rule(self, rule_id, payload):
  self.rules.setdefault(rule_id, {'description':rule_id,'enabled':True,'severity':'medium','weight':10})
  for k in ['enabled','threshold','weight']:
   if payload.get(k) is not None: self.rules[rule_id][k]=payload[k]
  self.path.write_text(yaml.safe_dump({'rules':self.rules}, sort_keys=False)); return self.rules[rule_id]
 def add(self,out,rid,e):
  r=self.rules.get(rid,{})
  if r.get('enabled',True): out.append({'rule_id':rid,'description':r.get('description',rid),'severity':r.get('severity','medium'),'weight':r.get('weight',10),'evidence':e})
 def evaluate(self,txn,regs,integrity):
  out=[]; wm={w['wallet_address']:w for w in regs['wallets']}
  if not integrity['hash_valid']: self.add(out,'HASH_MISMATCH','Hash validation failed')
  if not integrity['signature_valid']: self.add(out,'SIGNATURE_INVALID','Signature invalid')
  if txn.get('to_wallet') not in wm or not wm.get(txn.get('to_wallet'),{}).get('known',False): self.add(out,'UNKNOWN_WALLET','Destination wallet could not be verified')
  ts=datetime.fromisoformat(txn['timestamp'].replace('Z','+00:00'))
  if ts.weekday()>=5 or ts.hour<8 or ts.hour>=18: self.add(out,'OFF_HOURS','Transaction executed outside expected hours')
  if txn.get('amount',0)>=self.rules['HIGH_VALUE'].get('threshold',50000000) or 49800000<=txn.get('amount',0)<50000000: self.add(out,'HIGH_VALUE','High or near-threshold value')
  if txn.get('balance_percentage_moved',0)>=self.rules['LARGE_BALANCE_MOVEMENT'].get('percentage_threshold',80): self.add(out,'LARGE_BALANCE_MOVEMENT','Large percentage of wallet balance moved')
  if txn.get('kyc_status')=='missing': self.add(out,'KYC_MISSING','KYC is missing')
  if txn.get('first_time_receiver'): self.add(out,'FIRST_TIME_RECEIVER','First interaction with receiver')
  if txn.get('velocity_24h',0)>10: self.add(out,'VELOCITY_SPIKE','Transaction velocity exceeds baseline')
  if txn.get('oracle_address') and txn.get('oracle_address') not in [o['oracle_address'] for o in regs['oracles'] if o.get('status')=='approved']: self.add(out,'UNKNOWN_WALLET','Oracle is not approved')
  return out
