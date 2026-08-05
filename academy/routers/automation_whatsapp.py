from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from academy.core.database import get_db
from academy.core.models import User, Enrollment, Course
from academy.core.security import get_current_user

router = APIRouter(prefix="/automation", tags=["automation"])

@router.post("/whatsapp-notify/{enrollment_id}")
def whatsapp_notify(enrollment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment or enrollment.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada.")
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    message = (
        f"Olá, {user['name']}! Seja bem-vindo ao curso *{course.title}*, da Praia Digital Academy. "
        f"Acesse sua área do aluno para começar agora: https://praia.digital/education/aluno/index.html"
    )
    return {"message": "Notificação WhatsApp preparada.", "text": message}
