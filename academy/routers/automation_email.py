from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from academy.core.database import get_db
from academy.core.models import Enrollment, Course, User, Lead
from academy.core.email_service import send_enrollment_confirmation, send_lead_magnet

router = APIRouter(tags=["automation-email"])

@router.post("/automation/email-confirmation/{enrollment_id}")
def email_confirmation(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    user = db.query(User).filter(User.id == enrollment.user_id).first()
    course_url = f"https://academy.praia.digital/education/aluno/curso.html?course_id={course.id}"
    resp = send_enrollment_confirmation(getattr(user, "email", None), course.title, course_url)
    if isinstance(resp, dict):
        return {"status": resp.get("status"), "detail": resp.get("reason") or "ok"}
    return {"status": bool(resp), "detail": "ok"}

@router.post("/automation/email-lead-magnet/{lead_id}")
def email_lead_magnet(lead_id: int, magnet_url: str, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    magnet_name = lead.magnet or "Guia"
    resp = send_lead_magnet(lead.email, lead.name, magnet_name, magnet_url)
    return {"status": resp.get("status"), "detail": resp.get("reason") or "ok"}
