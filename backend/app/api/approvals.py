from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import get_db
from app.models import Approval, Action, AuditLog
from app.tools import execute_tool

router = APIRouter(prefix="/approvals", tags=["approvals"])

@router.get("")
def list_approvals(db: Session = Depends(get_db)):
    # Join with action to get details
    approvals = db.query(Approval).order_by(Approval.requested_at.desc()).all()
    results = []
    for a in approvals:
        action = db.query(Action).filter(Action.id == a.action_id).first()
        if action:
            results.append({
                "id": a.id,
                "action_id": a.action_id,
                "status": a.status,
                "requested_at": a.requested_at,
                "responded_at": a.responded_at,
                "responder": a.responder,
                "agent_id": action.agent_id,
                "tool_name": action.tool_name,
                "parameters": action.parameters,
            })
    return results

@router.post("/{approval_id}/approve")
def approve_action(approval_id: str, db: Session = Depends(get_db)):
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval or approval.status != "PENDING":
        raise HTTPException(status_code=400, detail="Invalid approval request")
        
    approval.status = "APPROVED"
    approval.responded_at = datetime.now(timezone.utc)
    approval.responder = "Human Admin"
    
    action = db.query(Action).filter(Action.id == approval.action_id).first()
    if action:
        action.status = "EXECUTED"
        try:
            result = execute_tool(action.tool_name, action.parameters)
            action.context["result"] = result
        except Exception as e:
            action.status = "FAILED"
            action.context["error"] = str(e)
            
        # Log approval
        audit = AuditLog(
            action_id=action.id,
            agent_id=action.agent_id,
            tool_name=action.tool_name,
            decision="HUMAN_APPROVED",
            details={"responder": "Human Admin", "result_status": action.status}
        )
        db.add(audit)
        
    db.commit()
    return {"status": "APPROVED", "action_result": action.context.get("result") if action else None}

@router.post("/{approval_id}/reject")
def reject_action(approval_id: str, db: Session = Depends(get_db)):
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval or approval.status != "PENDING":
        raise HTTPException(status_code=400, detail="Invalid approval request")
        
    approval.status = "REJECTED"
    approval.responded_at = datetime.now(timezone.utc)
    approval.responder = "Human Admin"
    
    action = db.query(Action).filter(Action.id == approval.action_id).first()
    if action:
        action.status = "REJECTED"
        
        audit = AuditLog(
            action_id=action.id,
            agent_id=action.agent_id,
            tool_name=action.tool_name,
            decision="HUMAN_REJECTED",
            details={"responder": "Human Admin"}
        )
        db.add(audit)
        
    db.commit()
    return {"status": "REJECTED"}
