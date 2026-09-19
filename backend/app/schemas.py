from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class ToolSchema(BaseModel):
    id: str
    name: str
    category: str
    description: str
    risk_base_score: int
    class Config:
        from_attributes = True

class AgentToolSchema(BaseModel):
    tool_id: str
    permission: str
    tool: Optional[ToolSchema] = None
    class Config:
        from_attributes = True

class AgentSchema(BaseModel):
    id: str
    name: str
    type: str
    status: str
    description: str
    risk_level: str
    created_at: datetime
    class Config:
        from_attributes = True

class PolicySchema(BaseModel):
    id: str
    name: str
    category: str
    description: str
    enabled: bool
    rules: Dict[str, Any]
    class Config:
        from_attributes = True

class ActionProposal(BaseModel):
    agent_id: str
    tool_name: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)

class ActionEvaluationSchema(BaseModel):
    risk_score: int
    risk_level: str
    decision: str
    reasons: List[str]
    policy_results: List[Dict[str, Any]]
    security_findings: List[Dict[str, Any]]

class ActionResponse(BaseModel):
    action_id: str
    evaluation: ActionEvaluationSchema
    status: str
    result: Optional[Dict[str, Any]] = None # If executed
