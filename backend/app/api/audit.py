from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AuditLog, SecurityEvent

router = APIRouter(tags=["audit"])

@router.get("/audit-logs")
def get_audit_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()

@router.get("/security-events")
def get_security_events(db: Session = Depends(get_db)):
    return db.query(SecurityEvent).order_by(SecurityEvent.timestamp.desc()).limit(100).all()
