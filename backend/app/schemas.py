from typing import Optional
from pydantic import BaseModel
from typing import Literal, List, Optional
class AnalyseRequest(BaseModel): search_type:Literal['transaction_id','transaction_hash','block_hash']='transaction_id'; value:str; persona:str='compliance_officer'; date_range:str='last_30_days'
class RuleUpdateRequest(BaseModel): rule_id:str; enabled:Optional[bool]=None; threshold:Optional[float]=None; weight:Optional[float]=None; updated_by:str='admin'; change_reason:str='demo'
class ExportRequest(BaseModel): txn_ids:List[str]; persona:str='fca_examiner'; format:str='pdf'
class ChatRequest(BaseModel): txn_id:Optional[str]=None; case_id:Optional[str]=None; question:str; persona:str='compliance_officer'
class FeedbackRequest(BaseModel): txn_id:str; feedback:str; reviewer:str; comments:Optional[str]=None
