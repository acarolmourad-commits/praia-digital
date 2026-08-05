from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from academy.core.database import get_db
from academy.core.models import Course, Enrollment, Payment
from academy.core.config import (
    DATABASE_URL,
    SMTP_HOST,
    SMTP_USER,
    EMAIL_FROM,
    ALLOWED_ORIGINS,
    MERCADOPAGO_TOKEN,
    MERCADOPAGO_PUBLIC_KEY,
    BASE_URL,
    WHATSAPP_API_URL,
    WHATSAPP_TOKEN,
    WHATSAPP_PHONE_ID,
)
import os

router = APIRouter(tags=["monitoring"])

@router.get("/monitoring/status")
def monitoring_status(db: Session = Depends(get_db)):
    db_ok = False
    try:
        db.execute("SELECT 1")
        db_ok = True
    except Exception:
        db_ok = False

    courses = db.query(Course).count()
    enrollments = db.query(Enrollment).count()
    payments = db.query(Payment).count()

    integrations = {
        "smtp": bool(SMTP_HOST and SMTP_USER),
        "mercado_pago": bool(MERCADOPAGO_TOKEN and MERCADOPAGO_PUBLIC_KEY),
        "whatsapp": bool(WHATSAPP_API_URL and WHATSAPP_TOKEN and WHATSAPP_PHONE_ID),
        "base_url": BASE_URL,
        "allowed_origins": ALLOWED_ORIGINS,
    }

    checks = {
        "database": "ok" if db_ok else "error",
        "courses": courses,
        "enrollments": enrollments,
        "payments": payments,
        "integrations": integrations,
        "environment": os.getenv("APP_ENV", "development"),
    }

    status = "ok" if db_ok else "degraded"
    return {"status": status, "checks": checks}
