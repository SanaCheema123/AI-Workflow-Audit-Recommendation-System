from datetime import datetime
from pydantic import BaseModel, Field

class AuditCreate(BaseModel):
    project_name: str = Field(min_length=1, max_length=200)
    description: str = ""

class FindingOut(BaseModel):
    id: int
    workflow_name: str
    category: str
    severity: str
    title: str
    detail: str
    evidence: str
    impact: str

    class Config:
        from_attributes = True

class RecommendationOut(BaseModel):
    id: int
    priority: str
    category: str
    title: str
    action: str
    rationale: str
    expected_impact: str

    class Config:
        from_attributes = True

class WorkflowOut(BaseModel):
    id: int
    name: str
    node_count: int
    trigger_count: int
    ai_node_count: int
    integration_count: int
    connection_count: int

    class Config:
        from_attributes = True

class AuditOut(BaseModel):
    id: int
    project_name: str
    description: str
    status: str
    overall_score: int | None
    risk_level: str | None
    production_readiness: str | None
    created_at: datetime
    workflows: list[WorkflowOut] = []
    findings: list[FindingOut] = []
    recommendations: list[RecommendationOut] = []

    class Config:
        from_attributes = True
