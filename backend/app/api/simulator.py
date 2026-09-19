from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.schemas import ActionProposal
from app.simulator.engine import SimulatorEngine

router = APIRouter(prefix="/simulate", tags=["simulate"])

@router.post("")
def run_simulation(proposals: List[ActionProposal], db: Session = Depends(get_db)):
    engine = SimulatorEngine(db)
    return engine.simulate_sequence(proposals)
