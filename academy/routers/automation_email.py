from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from academy.core.database import get_db
from academy.core.models import Enrollment, Course, User
from academy.core.email_service import send_enrollment_confirmation

router = APIRouter(tags=["automation-email"])

@router.post("/automation/email-confirmation/{enrollment_id}")
def email_confirmation(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    user = db.query(User).filter(User.id == enrollment.user_id).first()
    course_url = f"https://academy.praia.digital/education/aluno/curso.html?course_id={course.id}"
    resp = send_enrollment_confirmation(getattr(user, "email", None), course.name, course_url)
    return {"status": resp.get("status"), "detail": resp.get("reason") or "ok"}
