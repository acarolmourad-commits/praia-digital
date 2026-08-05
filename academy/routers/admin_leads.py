from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from academy.core.database import get_db
from academy.core.models import Lead, LeadEvent
from academy.core.schemas import LeadOut, LeadEventOut
from academy.core.security import admin_required

router = APIRouter(tags=["admin-leads"])

@router.get("/admin/leads", response_model=List[LeadOut])
def list_leads(
    db: Session = Depends(get_db),
    admin=Depends(admin_required),
    city: Optional[str] = None,
    magnet: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
):
    query = db.query(Lead)
    if city:
        query = query.filter(Lead.city == city)
    if magnet:
        query = query.filter(Lead.magnet == magnet)
    if status:
        query = query.filter(Lead.status == status)
    leads = query.order_by(Lead.created_at.desc()).offset(offset).limit(limit).all()
    return leads

@router.get("/admin/leads/{lead_id}/events", response_model=List[LeadEventOut])
def list_lead_events(lead_id: int, db: Session = Depends(get_db), admin=Depends(admin_required)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    return db.query(LeadEvent).filter(LeadEvent.lead_id == lead_id).order_by(LeadEvent.created_at.desc()).all()

@router.patch("/admin/leads/{lead_id}/status")
def update_lead_status(lead_id: int, status: str, db: Session = Depends(get_db), admin=Depends(admin_required)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    lead.status = status
    db.commit()
    db.refresh(lead)
    return {"status": "ok", "lead_id": lead.id, "new_status": lead.status}
