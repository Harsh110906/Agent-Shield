from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ActionProposal, ActionResponse
from app.agents.orchestrator import AgentOrchestrator

router = APIRouter(prefix="/actions", tags=["actions"])

@router.post("/evaluate")
def evaluate_action(proposal: ActionProposal, db: Session = Depends(get_db)):
    orchestrator = AgentOrchestrator(db)
    # The orchestrator handles evaluation and execution if ALLOWED
    # We call it evaluate_action to match the prompt's naming conceptually,
    # though it acts as a gateway run.
    return orchestrator.execute_action(proposal)
