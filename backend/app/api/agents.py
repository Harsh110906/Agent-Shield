from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.models import Agent, AgentTool, Tool
from app.schemas import AgentSchema, AgentToolSchema

router = APIRouter(prefix="/agents", tags=["agents"])

@router.get("", response_model=List[AgentSchema])
def list_agents(db: Session = Depends(get_db)):
    return db.query(Agent).all()

@router.get("/{agent_id}")
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    tools = db.query(AgentTool).filter(AgentTool.agent_id == agent_id).all()
    # Eager load tools
    tool_details = []
    for at in tools:
        t = db.query(Tool).filter(Tool.id == at.tool_id).first()
        if t:
            tool_details.append({
                "tool_id": t.id,
                "name": t.name,
                "category": t.category,
                "permission": at.permission,
                "risk_base_score": t.risk_base_score
            })
            
    return {
        "agent": agent,
        "tools": tool_details
    }
