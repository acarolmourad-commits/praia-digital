from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from academy.core.database import get_db
from academy.core.models import Course, Enrollment, EnrollmentStatus, Payment, PaymentStatus
from academy.core.security import get_current_user_optional
from academy.core.payments.service import get_payment_provider, is_sandbox, create_payment, PaymentContext, PaymentGateway
from academy.core.payments.webhooks import verify_webhook, handle_payment_event
import os
import logging

router = APIRouter(prefix="/academy", tags=["payments"])
optional_bearer = HTTPBearer(auto_error=False)
logger = logging.getLogger("academy.payments.router")

class CheckoutItem(BaseModel):
    course_id: int
    quantity: int = 1

class CheckoutPayload(BaseModel):
    items: List[CheckoutItem]
    buyer_name: Optional[str] = None
    buyer_email: Optional[str] = None
    buyer_document: Optional[str] = None

BASE_URL = os.getenv("BASE_URL", "https://academy.praia.digital")


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

    total = sum((c.price or 0) for c in courses)
    course_ids = [c.id for c in courses]
    user_id = user.get("id") if user else None

    # cria matrículas por curso
    enrollments = []
    for course_id in course_ids:
        enrollment = Enrollment(user_id=user_id, course_id=course_id, status=EnrollmentStatus.pending.value)
        db.add(enrollment)
        db.flush()
        enrollments.append(enrollment)

    gateway = get_payment_provider()
    context = PaymentContext(
        gateway=gateway,
        is_sandbox=is_sandbox(),
        enrollment_id=enrollments[0].id,
        amount=total,
        currency="BRL",
        buyer_email=payload.buyer_email or "",
        buyer_name=payload.buyer_name or "",
        external_reference=str(enrollments[0].id),
    )
    if user_id:
        context = PaymentContext(
            gateway=gateway,
            is_sandbox=is_sandbox(),
            enrollment_id=enrollments[0].id,
            amount=total,
            currency="BRL",
            buyer_email=payload.buyer_email or "",
            buyer_name=payload.buyer_name or "",
            external_reference=str(enrollments[0].id),
            user_id=user_id,
        )
    payment = create_payment(db, context)
    db.commit()

    if gateway == PaymentGateway.sandbox:
        return {
            "checkout_url": f"{BASE_URL}/education/checkout.html?order_id={enrollments[0].id}",
            "order_id": enrollments[0].id,
            "payment_id": payment.id,
            "total": total,
            "currency": "BRL",
            "status": "pending",
            "gateway": "sandbox",
            "message": "Pedido criado.",
        }

    if gateway == PaymentGateway.hotmart:
        token = os.getenv("HOTMART_TOKEN", "")
        api_url = os.getenv("HOTMART_API", "https://api.hotmart.com")
        if not token:
            raise HTTPException(status_code=500, detail="Hotmart não configurado")
        hotmart_payload = {
            "product_id": os.getenv("HOTMART_PRODUCT_ID", ""),
            "checkout_type": "lightbox",
            "currency": "BRL",
            "price": total,
            "name": payload.buyer_name or "Comprador",
            "email": payload.buyer_email or "",
            "document": payload.buyer_document or "",
            "external_reference": str(enrollments[0].id),
            "notification_url": f"{BASE_URL}/academy/payments/webhook",
            "return_url": f"{BASE_URL}/education/checkout.html?status=approved&order_id={enrollments[0].id}",
        }
        import requests
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        resp = requests.post(f"{api_url}/checkout", json=hotmart_payload, headers=headers, timeout=20)
        if resp.status_code != 201:
            raise HTTPException(status_code=502, detail=f"Erro ao criar checkout Hotmart: {resp.text}")
        data = resp.json()
        return {
            "checkout_url": data.get("checkout_url"),
            "order_id": enrollments[0].id,
            "payment_id": payment.id,
            "total": total,
            "currency": "BRL",
            "status": "pending",
            "gateway": "hotmart",
            "message": "Pedido criado.",
        }

    if gateway == PaymentGateway.mercadopago:
        token = os.getenv("MERCADOPAGO_TOKEN", "")
        api_url = os.getenv("MERCADOPAGO_API_URL", "https://api.mercadopago.com/v1")
        if not token:
            raise HTTPException(status_code=500, detail="Mercado Pago não configurado")
        mp_payload = {
            "items": [
                {
                    "title": "Matrícula Praia Digital Academy",
                    "quantity": 1,
                    "unit_price": total,
                    "currency_id": "BRL",
                }
            ],
            "payer": {
                "email": payload.buyer_email or "",
                "name": payload.buyer_name or "",
                "identification": {
                    "type": "CPF",
                    "number": payload.buyer_document or "",
                },
            },
            "back_urls": {
                "success": f"{BASE_URL}/education/checkout.html?status=approved&order_id={enrollments[0].id}",
                "failure": f"{BASE_URL}/education/checkout.html?status=rejected&order_id={enrollments[0].id}",
                "pending": f"{BASE_URL}/education/checkout.html?status=pending&order_id={enrollments[0].id}",
            },
            "auto_return": "approved",
            "notification_url": f"{BASE_URL}/payments/webhook",
            "external_reference": str(enrollments[0].id),
        }
        import requests
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        resp = requests.post(f"{api_url}/checkout/preferences", json=mp_payload, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        return {
            "checkout_url": data.get("init_point"),
            "order_id": enrollments[0].id,
            "payment_id": payment.id,
            "total": total,
            "currency": "BRL",
            "status": "pending",
            "gateway": "mercadopago",
            "message": "Pedido criado.",
        }

    raise HTTPException(status_code=500, detail=f"Gateway {gateway} não suportado no checkout ainda")


@router.get("/checkout/status")
def checkout_status(order_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    payment = db.query(Payment).filter(Payment.enrollment_id == enrollment.id).first()
    return {
        "order_id": order_id,
        "status": enrollment.status,
        "payment_status": payment.status if payment else "unknown",
    }


@router.get("/checkout/confirm")
def checkout_confirm(order_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    payment = db.query(Payment).filter(Payment.enrollment_id == enrollment.id).first()
    if payment and payment.status == PaymentStatus.paid.value:
        enrollment.status = EnrollmentStatus.active.value
        db.commit()
        return {
            "status": "active",
            "enrollment_id": enrollment.id,
            "course_id": enrollment.course_id,
            "message": "Pagamento confirmado. Acesso liberado.",
        }
    return {
        "status": enrollment.status,
        "enrollment_id": enrollment.id,
        "course_id": enrollment.course_id,
        "message": "Aguardando confirmação do pagamento.",
    }


@router.post("/payments/webhook")
async def payments_webhook(request: Request, db: Session = Depends(get_db)):
    body_bytes = await request.body()
    gateway = getattr(request.app.state, "payment_gateway", "sandbox") if hasattr(request, "app") else "sandbox"
    if not verify_webhook(request, body_bytes):
        raise HTTPException(status_code=403, detail="invalid webhook")
    try:
        payload = await request.json()
    except Exception:
        payload = {}
    result = handle_payment_event(db, gateway, payload)
    logger.info("webhook_received gateway=%s result=%s", gateway, result)
    return result
