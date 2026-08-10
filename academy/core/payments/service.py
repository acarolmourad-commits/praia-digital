import os
import hmac
import hashlib
import logging
from typing import Optional
from sqlalchemy.orm import Session
from academy.core.models import Payment, PaymentStatus, Enrollment, EnrollmentStatus
from academy.core.payments.types import PaymentContext, PaymentGateway
from academy.core.email_service import send_enrollment_confirmation
from datetime import datetime, timedelta

logger = logging.getLogger("academy.payments")

# Public gateway enum for routing/config
payment_gateway_enum = PaymentGateway


def is_sandbox() -> bool:
    return os.getenv("PAYMENT_GATEWAY", "sandbox").lower() == "sandbox"


def _detect_gateway() -> PaymentGateway:
    raw = os.getenv("PAYMENT_GATEWAY", "sandbox").lower()
    mapping = {
        "sandbox": PaymentGateway.sandbox,
        "hotmart": PaymentGateway.hotmart,
        "mercadopago": PaymentGateway.mercadopago,
        "stripe": PaymentGateway.stripe,
    }
    return mapping.get(raw, PaymentGateway.sandbox)


def get_payment_provider() -> PaymentGateway:
    return _detect_gateway()


def create_payment(db: Session, context: PaymentContext) -> Payment:
    course_id = context.course_id
    if course_id is None and context.enrollment_id:
        enrollment = db.query(Enrollment).filter(Enrollment.id == context.enrollment_id).first()
        if enrollment:
            course_id = enrollment.course_id
    if course_id is None:
        course_id = 0
    payment = Payment(
        user_id=context.user_id,
        course_id=course_id,
        enrollment_id=context.enrollment_id,
        amount=context.amount,
        currency=context.currency,
        status=PaymentStatus.pending.value,
        gateway=context.gateway.value,
        gateway_payment_id=context.external_reference or None,
    )
    db.add(payment)
    db.flush()
    db.refresh(payment)
    logger.info(
        "payment_created gateway=%s payment_id=%s enrollment_id=%s amount=%s",
        context.gateway.value,
        payment.id,
        context.enrollment_id,
        context.amount,
    )
    return payment


def finalize_payment(
    db: Session,
    payment: Payment,
    new_status: str,
    *,
    gateway_payment_id: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> Payment:
    previous = payment.status
    payment.status = new_status
    payment.updated_at = datetime.utcnow()
    if gateway_payment_id:
        payment.gateway_payment_id = gateway_payment_id
    if new_status == PaymentStatus.paid.value:
        payment.paid_at = datetime.utcnow()
        _activate_enrollment(db, payment)
    elif new_status == PaymentStatus.refunded.value:
        _deactivate_enrollment(db, payment)
    db.commit()
    db.refresh(payment)
    logger.info(
        "payment_updated payment_id=%s %s -> %s gateway_payment_id=%s",
        payment.id,
        previous,
        new_status,
        payment.gateway_payment_id,
    )
    return payment


def _activate_enrollment(db: Session, payment: Payment) -> None:
    if not payment.enrollment_id:
        return
    enrollment = db.query(Enrollment).filter(Enrollment.id == payment.enrollment_id).first()
    if not enrollment:
        return
    if enrollment.status == EnrollmentStatus.active.value:
        return
    enrollment.status = EnrollmentStatus.active.value
    enrollment.access_until = datetime.utcnow() + timedelta(days=365)
    db.flush()
    logger.info("enrollment_activated enrollment_id=%s", enrollment.id)
    course = enrollment.course if hasattr(enrollment, "course") else None
    course_title = getattr(course, "title", "Curso")
    course_url = f"{os.getenv('BASE_URL', 'https://academy.praia.digital')}/education/courses/{enrollment.course_id}"
    user = enrollment.user if hasattr(enrollment, "user") else None
    user_email = getattr(user, "email", None)
    send_enrollment_confirmation(user_email, course_title, course_url)


def _deactivate_enrollment(db: Session, payment: Payment) -> None:
    if not payment.enrollment_id:
        return
    enrollment = db.query(Enrollment).filter(Enrollment.id == payment.enrollment_id).first()
    if not enrollment:
        return
    enrollment.status = EnrollmentStatus.refunded.value
    db.flush()
    logger.info("enrollment_refunded enrollment_id=%s", enrollment.id)
