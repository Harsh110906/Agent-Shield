from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Policy
from app.schemas import PolicySchema

router = APIRouter(prefix="/policies", tags=["policies"])

@router.get("", response_model=List[PolicySchema])
def list_policies(db: Session = Depends(get_db)):
    return db.query(Policy).all()

@router.post("")
def create_policy(policy: PolicySchema, db: Session = Depends(get_db)):
    db_policy = Policy(
        name=policy.name,
        category=policy.category,
        description=policy.description,
        enabled=policy.enabled,
        rules=policy.rules
    )
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy

@router.put("/{policy_id}")
def update_policy(policy_id: str, policy: dict, db: Session = Depends(get_db)):
    db_policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not db_policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    for key, value in policy.items():
        if hasattr(db_policy, key):
            setattr(db_policy, key, value)
            
    db.commit()
    db.refresh(db_policy)
    return db_policy
