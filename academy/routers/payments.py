from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from academy.core.database import get_db
from academy.core.models import Course, Enrollment, EnrollmentStatus, Payment, PaymentStatus
import os, requests

router = APIRouter()

class CheckoutItem(BaseModel):
    course_id: int
    quantity: int = 1

class CheckoutPayload(BaseModel):
    items: List[CheckoutItem]
    buyer_name: Optional[str] = None
    buyer_email: Optional[str] = None
    buyer_document: Optional[str] = None

MERCADOPAGO_API = os.getenv("MERCADOPAGO_API_URL", "https://api.mercadopago.com/v1")
MERCADOPAGO_TOKEN = os.getenv("MERCADOPAGO_TOKEN", "")
MERCADOPAGO_PUBLIC_KEY = os.getenv("MERCADOPAGO_PUBLIC_KEY", "")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

def _build_payment_payload(enrollment_id: int, total: int, payer: dict):
    return {
        "items": [
            {
                "title": "Matrícula Praia Digital Academy",
                "quantity": 1,
                "unit_price": total,
                "currency_id": "BRL",
            }
        ],
        "payer": {
            "email": payer.get("email", "comprador@example.com"),
            "first_name": payer.get("name", "Comprador"),
            "identification": {"type": "CPF", "number": payer.get("document", "00000000000")},
        },
        "back_urls": {
            "success": f"{BASE_URL}/education/checkout.html?status=approved&enrollment_id={enrollment_id}",
            "failure": f"{BASE_URL}/education/checkout.html?status=rejected&enrollment_id={enrollment_id}",
            "pending": f"{BASE_URL}/education/checkout.html?status=pending&enrollment_id={enrollment_id}",
        },
        "auto_return": "approved",
        "notification_url": f"{BASE_URL}/payments/mercadopago/webhook",
        "external_reference": str(enrollment_id),
    }

@router.post("/checkout")
def public_checkout(payload: CheckoutPayload, db: Session = Depends(get_db)):
    courses = db.query(Course).filter(Course.id.in_([i.course_id for i in payload.items])).all()
    if not courses:
        raise HTTPException(status_code=404, detail="Cursos não encontrados")

    total = sum(c.price for c in courses)
    enrollment = Enrollment(student_id=None, status=EnrollmentStatus.pending.value)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    payment = Payment(enrollment_id=enrollment.id, amount=total, status=PaymentStatus.pending.value, method="public_checkout")
    db.add(payment)
    db.commit()
    db.refresh(payment)

    if MERCADOPAGO_TOKEN:
        try:
            headers = {"Authorization": f"Bearer {MERCADOPAGO_TOKEN}", "Content-Type": "application/json"}
            mp_payload = _build_payment_payload(enrollment.id, total, {"name": payload.buyer_name or "", "email": payload.buyer_email or "", "document": payload.buyer_document or ""})
            resp = requests.post(f"{MERCADOPAGO_API}/checkout/preferences", json=mp_payload, headers=headers, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            return {"checkout_url": data.get("init_point"), "order_id": enrollment.id, "payment_id": payment.id, "total": total, "currency": "BRL", "status": "pending", "message": "Pedido criado."}
        except requests.RequestException:
            pass

    return {"checkout_url": f"/education/checkout.html?order_id={enrollment.id}", "order_id": enrollment.id, "payment_id": payment.id, "total": total, "currency": "BRL", "status": "pending", "message": "Pedido criado."}

@router.get("/checkout/status")
def checkout_status(order_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).join(Enrollment).filter(Enrollment.id == order_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
    return {"order_id": order_id, "status": enrollment.status if enrollment else "unknown", "payment_status": payment.status if payment else "unknown"}

@router.post("/mercadopago/webhook")
def mercadopago_webhook(payload: dict, db: Session = Depends(get_db)):
    if payload.get("type") != "payment":
        return {"ok": True}
    data = payload.get("data", {})
    status = data.get("status")
    external_ref = str(data.get("external_reference", ""))
    if not external_ref:
        return {"ok": True}
    try:
        enrollment_id = int(external_ref)
    except ValueError:
        return {"ok": True}

    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        return {"ok": True}
    payment = db.query(Payment).filter(Payment.enrollment_id == enrollment.id).first()
    if not payment:
        return {"ok": True}

    if status == "approved":
        enrollment.status = EnrollmentStatus.active.value
        payment.status = PaymentStatus.approved.value
    elif status == "rejected":
        enrollment.status = EnrollmentStatus.cancelled.value
        payment.status = PaymentStatus.rejected.value
    elif status == "pending":
        enrollment.status = EnrollmentStatus.pending.value
        payment.status = PaymentStatus.pending.value
    db.commit()
    return {"ok": True}
