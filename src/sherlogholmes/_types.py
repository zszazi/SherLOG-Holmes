from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel


class FailureJob(BaseModel):
    jobid: str
    ip: str

class FailureJobs(BaseModel):
    ids: List[FailureJob]
    
    
class LogsFailure(BaseModel):
    job_id: str
    logs: str

class LogsFailureList(BaseModel):
    fails: List[LogsFailure]

class AggregatorEntry(BaseModel):
    ip_address: str
    issue: str
    log_snippet: str
    origin: Literal["application", "network"]

class AggregatorList(BaseModel):
    failures: List[AggregatorEntry]

class SherLOGState(BaseModel):
    log_analysis: Optional[str] = None
    started_at: Optional[datetime] = None
    impact: Optional[str] = None
    severity_score: Optional[str] = None
    rca: Optional[str] = None
    war_room: Optional[str] = None
    cust_comm: Optional[str] = None

#alert response crew 
class ImpactScore(BaseModel):
    impact_score: int
    severity: str 
    justification_for_severity: str

class PagerDuty(BaseModel):
    notification: str 
    data: ImpactScore

#war_room_crews 
class BackendIssueReport(BaseModel):
    api_failures: List[str]
    database_issues: List[str]
    recommendations: List[str]

class NetworkIssueReport(BaseModel):
    latency_issues: List[str]
    firewall_blocks: List[str]
    recommendations: List[str]

class ArchitecturalReviewReport(BaseModel):
    weak_points: List[str]
    resilience_improvements: List[str]
    scaling_recommendations: List[str]

class BusinessImpactReport(BaseModel):
    affected_customers: List[str]
    estimated_financial_loss: float
    priority_fixes: List[str]

class WarRoomActionPlan(BaseModel):
    immediate_actions: List[str]
    short_term_goals: List[str]
    long_term_strategy: List[str]

#Customer Communication crew 

class CustomerEmail(BaseModel):
    subject: str
    body: str

class FAQDocument(BaseModel):
    questions: List[str]
    answers: List[str]
