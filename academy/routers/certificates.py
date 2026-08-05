from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from academy.core.database import get_db
from academy.core.models import Certificate, Enrollment, Course
from fpdf import FPDF
import os
from datetime import datetime

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

@router.post("/generate/{enrollment_id}")
def generate_certificate(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada.")
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")

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

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Código do certificado: {enrollment.id}-{course.id}", align="C", ln=True)

    filename = f"certificate_{enrollment.id}_{course.id}.pdf"
    output_path = os.path.join("academy", "static", "certificates", filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)

    return {"message": "Certificado gerado.", "file": f"/academy/static/certificates/{filename}"}

@router.get("/me")
def list_my_certificates(db: Session = Depends(get_db)):
    return []
