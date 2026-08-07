from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from academy.core.database import get_db
from academy.core.models import Lead, LeadEvent
from academy.core.schemas import LeadIn, LeadOut, LeadEventOut
from academy.core.middleware import sanitize_text

router = APIRouter(tags=["leads"])

@router.post("/leads", response_model=LeadOut)
def create_lead(payload: LeadIn, db: Session = Depends(get_db)):
    lead = Lead(
        name=sanitize_text(payload.name),
        email=sanitize_text(payload.email),
        phone=sanitize_text(payload.phone),
        city=sanitize_text(payload.city),
        source=sanitize_text(payload.source),
        magnet=sanitize_text(payload.magnet),
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    event = LeadEvent(lead_id=lead.id, event="created", payload=payload.model_dump_json())
    db.add(event)
    db.commit()
    return lead

@router.get("/leads/{lead_id}", response_model=LeadOut)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    return lead

@router.post("/leads/{lead_id}/events", response_model=LeadEventOut)
def add_lead_event(lead_id: int, event: str, payload: Optional[str] = None, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    ev = LeadEvent(lead_id=lead.id, event=event, payload=payload)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev
