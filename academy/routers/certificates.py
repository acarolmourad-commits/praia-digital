from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from academy.core.database import get_db
from academy.core.models import Certificate, Enrollment, Course, User
from academy.core.security import get_current_user
from fpdf import FPDF
import os
from datetime import datetime
import uuid

router = APIRouter(prefix="/certificates", tags=["certificates"])

class CertificatePDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(0, 180, 216)
        self.cell(0, 12, "Praia Digital Academy", align="C", ln=True)
        self.set_font("Helvetica", "", 12)
        self.set_text_color(60, 60, 60)
        self.cell(0, 8, "Certificado de Conclusão", align="C", ln=True)
        self.ln(4)

    def footer(self):
        self.set_y(-30)
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Emitido em: {datetime.now().strftime('%d/%m/%Y')}", align="C")
        self.ln(6)
        self.cell(0, 8, "https://praia.digital/education", align="C")

@router.get("/me")
def list_my_certificates(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    certs = db.query(Certificate).filter(Certificate.user_id == user["id"]).all()
    return [
        {
            "id": c.id,
            "enrollment_id": c.enrollment_id,
            "course_id": c.course_id,
            "code": c.code,
            "pdf_url": c.pdf_url,
            "issued_at": c.issued_at,
        }
        for c in certs
    ]

@router.post("/generate/{enrollment_id}")
def generate_certificate(enrollment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id, Enrollment.user_id == user["id"]).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada.")
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")

    existing = db.query(Certificate).filter(Certificate.enrollment_id == enrollment_id).first()
    if existing:
        return {
            "message": "Certificado já emitido.",
            "file": existing.pdf_url,
            "code": existing.code,
        }

    pdf = CertificatePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, "Certificamos que", align="C", ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 12, f"{enrollment.user.name}", align="C", ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 10, f"concluiu o curso \"{course.title}\" com aproveitamento satisfatório.", align="C")
    pdf.ln(6)

    cert_code = f"{enrollment.id}-{course.id}-{uuid.uuid4().hex[:6]}"
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Código do certificado: {cert_code}", align="C", ln=True)

    filename = f"certificate_{enrollment.id}_{course.id}.pdf"
    output_path = os.path.join("academy", "static", "certificates", filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)

    certificate = Certificate(
        user_id=user["id"],
        course_id=course.id,
        enrollment_id=enrollment.id,
        code=cert_code,
        pdf_url=f"/academy/static/certificates/{filename}",
    )
    db.add(certificate)
    db.commit()
    db.refresh(certificate)

    return {
        "message": "Certificado gerado.",
        "file": certificate.pdf_url,
        "code": certificate.code,
    }
