from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Agent(Base):
    __tablename__ = "agents"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, default="ACTIVE")
    description = Column(String)
    risk_level = Column(String, default="LOW")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Tool(Base):
    __tablename__ = "tools"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, unique=True)
    category = Column(String)
    description = Column(String)
    risk_base_score = Column(Integer, default=0)

class AgentTool(Base):
    __tablename__ = "agent_tools"
    agent_id = Column(String, ForeignKey("agents.id"), primary_key=True)
    tool_id = Column(String, ForeignKey("tools.id"), primary_key=True)
    permission = Column(String, nullable=False) # allowed, approval, blocked

class Policy(Base):
    __tablename__ = "policies"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    category = Column(String)
    description = Column(String)
    enabled = Column(Boolean, default=True)
    rules = Column(JSON, nullable=False)

class Action(Base):
    __tablename__ = "actions"
    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, ForeignKey("agents.id"))
    tool_name = Column(String, nullable=False)
    parameters = Column(JSON)
    context = Column(JSON)
    status = Column(String, default="PENDING") # PENDING, EXECUTED, BLOCKED, REJECTED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ActionEvaluation(Base):
    __tablename__ = "action_evaluations"
    id = Column(String, primary_key=True, default=generate_uuid)
    action_id = Column(String, ForeignKey("actions.id"))
    risk_score = Column(Integer, default=0)
    risk_level = Column(String, default="LOW") # LOW, MEDIUM, HIGH, CRITICAL
    decision = Column(String, nullable=False) # ALLOW, REQUIRE_APPROVAL, BLOCK
    reasons = Column(JSON)
    policy_results = Column(JSON)
    security_findings = Column(JSON)

class Approval(Base):
    __tablename__ = "approvals"
    id = Column(String, primary_key=True, default=generate_uuid)
    action_id = Column(String, ForeignKey("actions.id"))
    status = Column(String, default="PENDING") # PENDING, APPROVED, REJECTED, EXPIRED
    requested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    responded_at = Column(DateTime, nullable=True)
    responder = Column(String, nullable=True)
    notes = Column(String, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True, default=generate_uuid)
    action_id = Column(String, ForeignKey("actions.id"), nullable=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=True)
    tool_name = Column(String, nullable=True)
    decision = Column(String, nullable=True)
    risk_score = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    details = Column(JSON)

class SecurityEvent(Base):
    __tablename__ = "security_events"
    id = Column(String, primary_key=True, default=generate_uuid)
    action_id = Column(String, ForeignKey("actions.id"), nullable=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=True)
    severity = Column(String, nullable=False) # INFO, WARNING, CRITICAL
    event_type = Column(String, nullable=False) # PROMPT_INJECTION, SENSITIVE_DATA, POLICY_VIOLATION, etc
    description = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
