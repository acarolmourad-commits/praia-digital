from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from academy.core.database import get_db
from academy.core.models import Course, Enrollment, EnrollmentStatus, Payment, PaymentStatus
from academy.core.security import get_current_user_optional
import os
import requests

router = APIRouter(prefix="/academy", tags=["payments"])

optional_bearer = HTTPBearer(auto_error=False)

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
BASE_URL = os.getenv("BASE_URL", "https://academy.praia.digital")


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
            "identification": {
                "type": "CPF",
                "number": payer.get("document", "00000000000"),
            },
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
def public_checkout(
    payload: CheckoutPayload,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_optional),
    credentials=Depends(optional_bearer),
):
    courses = db.query(Course).filter(Course.id.in_([i.course_id for i in payload.items])).all()
    if not courses:
        raise HTTPException(status_code=404, detail="Cursos não encontrados")

    total = sum(c.price for c in courses)
    course_ids = [c.id for c in courses]
    user_id = user.get("id") if user else None

    # cria matrículas por curso
    enrollments = []
    for course_id in course_ids:
        enrollment = Enrollment(user_id=user_id, course_id=course_id, status=EnrollmentStatus.pending.value)
        db.add(enrollment)
        db.flush()
        enrollments.append(enrollment)

    # cria pagamento associado ao primeiro item
    payment = Payment(user_id=user_id, course_id=course_ids[0], amount=total, status=PaymentStatus.pending.value, gateway="public_checkout")
    db.add(payment)
    db.commit()
    db.refresh(payment)

    if MERCADOPAGO_TOKEN:
        try:
            headers = {"Authorization": f"Bearer {MERCADOPAGO_TOKEN}", "Content-Type": "application/json"}
            mp_payload = _build_payment_payload(enrollments[0].id, total, {
                "name": payload.buyer_name or "",
                "email": payload.buyer_email or "",
                "document": payload.buyer_document or "",
            })
            resp = requests.post(f"{MERCADOPAGO_API}/checkout/preferences", json=mp_payload, headers=headers, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            return {
                "checkout_url": data.get("init_point"),
                "order_id": enrollments[0].id,
                "payment_id": payment.id,
                "total": total,
                "currency": "BRL",
                "status": "pending",
                "message": "Pedido criado.",
            }
        except requests.RequestException as e:
            raise HTTPException(status_code=502, detail=f"Erro ao criar preferência no Mercado Pago: {str(e)}")

    return {
        "checkout_url": f"{BASE_URL}/education/checkout.html?order_id={enrollments[0].id}",
        "order_id": enrollments[0].id,
        "payment_id": payment.id,
        "total": total,
        "currency": "BRL",
        "status": "pending",
        "message": "Pedido criado.",
    }


@router.get("/checkout/status")
def checkout_status(order_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).join(Enrollment).filter(Enrollment.id == order_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
    return {
        "order_id": order_id,
        "status": enrollment.status if enrollment else "unknown",
        "payment_status": payment.status if payment else "unknown",
    }


@router.post("/payments/{payment_id}/webhook")
def payment_webhook(payment_id: str, payload: dict, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == int(payment_id)).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    status = payload.get("status")
    if status == "paid":
        payment.status = PaymentStatus.paid.value
    elif status == "rejected":
        payment.status = PaymentStatus.failed.value
    elif status == "pending":
        payment.status = PaymentStatus.pending.value
    elif status == "refunded":
        payment.status = PaymentStatus.refunded.value
    elif status == "cancelled":
        payment.status = PaymentStatus.failed.value
    db.commit()
    return {"ok": True}


@router.get("/mercadopago/payment/{payment_id}")
def get_mercadopago_payment(payment_id: str):
    if not MERCADOPAGO_TOKEN:
        raise HTTPException(status_code=500, detail="Mercado Pago não configurado")
    headers = {"Authorization": f"Bearer {MERCADOPAGO_TOKEN}"}
    resp = requests.get(f"{MERCADOPAGO_API}/payments/{payment_id}", headers=headers, timeout=20)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Erro ao consultar pagamento")
    return resp.json()
