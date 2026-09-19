from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Agent, Action, Approval, ActionEvaluation, SecurityEvent

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("")
def get_metrics(db: Session = Depends(get_db)):
    active_agents = db.query(Agent).filter(Agent.status == "ACTIVE").count()
    total_actions = db.query(Action).count()
    
    approvals = db.query(Approval).filter(Approval.status == "PENDING").count()
    blocked = db.query(ActionEvaluation).filter(ActionEvaluation.decision == "BLOCK").count()
    
    avg_risk = db.query(func.avg(ActionEvaluation.risk_score)).scalar() or 0
    
    # recent activity
    recent_actions = db.query(Action).order_by(Action.created_at.desc()).limit(10).all()
    activity_feed = []
    for a in recent_actions:
        agent = db.query(Agent).filter(Agent.id == a.agent_id).first()
        eval = db.query(ActionEvaluation).filter(ActionEvaluation.action_id == a.id).first()
        activity_feed.append({
            "action_id": a.id,
            "agent_name": agent.name if agent else "Unknown",
            "tool_name": a.tool_name,
            "status": a.status,
            "decision": eval.decision if eval else "UNKNOWN",
            "risk_score": eval.risk_score if eval else 0,
            "created_at": a.created_at
        })
        
    security_events = db.query(SecurityEvent).order_by(SecurityEvent.timestamp.desc()).limit(5).all()

    return {
        "active_agents": active_agents,
        "actions_today": total_actions, # simplified for hackathon
        "pending_approvals": approvals,
        "blocked_actions": blocked,
        "average_risk": int(avg_risk),
        "activity_feed": activity_feed,
        "security_events": security_events
    }
