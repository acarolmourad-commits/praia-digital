from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from academy.core.database import get_db
from academy.core.models import Enrollment, Course, User, Payment
from academy.core.whatsapp_service import send_text, send_template, send_media
from academy.core.config import (
    WHATSAPP_API_URL,
    WHATSAPP_TOKEN,
    WHATSAPP_PHONE_ID,
    WHATSAPP_TO_NUMBER,
)
import os

router = APIRouter(tags=["automation-whatsapp"])

def _enrollment_context(enrollment_id: int, db: Session):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    user = db.query(User).filter(User.id == enrollment.user_id).first()
    return enrollment, course, user

def _is_configured():
    return bool(WHATSAPP_API_URL and WHATSAPP_TOKEN and WHATSAPP_PHONE_ID)

# Templates por evento
MESSAGES = {
    "post_purchase": "🎉 Parabéns pela sua matrícula na Praia Digital Academy! Acesse o conteúdo em: {course_url}. Dúvidas? Responda esta mensagem.",
    "payment_confirmed": "✅ Pagamento confirmado! Seu acesso ao curso foi liberado. Acesse agora: {course_url}",
    "certificate_ready": "📜 Seu certificado está disponível! Baixe em: {certificate_url}",
    "welcome": "👋 Bem-vindo à Praia Digital Academy! Seu curso já está disponível. Acesse: {course_url}",
    "upsell": "🚀 Que tal avançar para o próximo nível? Conheça cursos complementares: {upsell_url}",
}

@router.post("/automation/whatsapp-notify/{enrollment_id}")
def notify_enrollment(enrollment_id: int, event: str = "post_purchase", db: Session = Depends(get_db)):
    enrollment, course, user = _enrollment_context(enrollment_id, db)

    if not _is_configured():
        return {"status": "skipped", "reason": "not configured"}

    to_number = WHATSAPP_TO_NUMBER or getattr(user, "phone", "")
    if not to_number:
        return {"status": "skipped", "reason": "missing destination number"}

    template_key = event
    message = MESSAGES.get(template_key, MESSAGES["post_purchase"])
    course_url = f"https://academy.praia.digital/education/aluno/curso.html?course_id={course.id}"
    certificate_url = f"https://academy.praia.digital/academy/certificates/{enrollment.id}.pdf"
    upsell_url = "https://academy.praia.digital/education/cursos/index.html"

    text = message.format(
        course_url=course_url,
        certificate_url=certificate_url,
        upsell_url=upsell_url,
    )

    resp = send_text(to_number, text)
    return {"status": "sent", "to": to_number, "event": event, "response": resp}

@router.post("/automation/whatsapp-payment-confirmed/{enrollment_id}")
def notify_payment_confirmed(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment, course, user = _enrollment_context(enrollment_id, db)
    return notify_enrollment(enrollment_id, event="payment_confirmed", db=db)

@router.post("/automation/whatsapp-certificate/{enrollment_id}")
def notify_certificate(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment, course, user = _enrollment_context(enrollment_id, db)
    return notify_enrollment(enrollment_id, event="certificate_ready", db=db)

@router.post("/automation/whatsapp-upsell/{user_id}")
def notify_upsell(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not _is_configured():
        return {"status": "skipped", "reason": "not configured"}

    to_number = WHATSAPP_TO_NUMBER or getattr(user, "phone", "")
    if not to_number:
        return {"status": "skipped", "reason": "missing destination number"}

    text = MESSAGES["upsell"].format(
        upsell_url="https://academy.praia.digital/education/cursos/index.html"
    )
    resp = send_text(to_number, text)
    return {"status": "sent", "to": to_number, "event": "upsell", "response": resp}
