import logging
from datetime import datetime
from sqlalchemy.orm import Session
from academy.core.models import (
    User,
    Course,
    Enrollment,
    EnrollmentStatus,
    Payment,
    PaymentStatus,
    Order,
    OrderItem,
)
from academy.core.payments.service import create_payment, get_payment_provider, is_sandbox, PaymentContext, PaymentGateway
from academy.core.payments.webhooks import handle_payment_event
from academy.core.email_service import send_enrollment_confirmation

logger = logging.getLogger("academy.conversion")


def register_interest(db: Session, *, name: str, email: str, phone: str | None, course_id: int, source: str = "checkout") -> dict:
    """Registra interesse inicial e cria ou retorna usuário/aluno."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(name=name, email=email, phone=phone, role="student", status="active")
        db.add(user)
        db.flush()
        db.refresh(user)

    enrollment = (
        db.query(Enrollment)
        .filter(Enrollment.user_id == user.id, Enrollment.course_id == course_id)
        .first()
    )
    if not enrollment:
        enrollment = Enrollment(user_id=user.id, course_id=course_id, status=EnrollmentStatus.pending.value, source=source)
        db.add(enrollment)
        db.flush()
        db.refresh(enrollment)

    return {
        "user_id": user.id,
        "enrollment_id": enrollment.id,
        "course_id": course_id,
        "status": enrollment.status,
    }


def create_order_for_course(db: Session, *, user_id: int, course_id: int, amount: int, currency: str = "BRL", buyer_name: str = "", buyer_email: str = "", buyer_document: str | None = None) -> dict:
    """Cria pedido + matrícula pendente + pagamento pendente e retorna payload para checkout."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise ValueError("Curso não encontrado")

    enrollment = (
        db.query(Enrollment)
        .filter(Enrollment.user_id == user_id, Enrollment.course_id == course_id)
        .first()
    )
    if not enrollment:
        enrollment = Enrollment(user_id=user_id, course_id=course_id, status=EnrollmentStatus.pending.value)
        db.add(enrollment)
        db.flush()
        db.refresh(enrollment)

    order = Order(user_id=user_id, status="open", subtotal=amount, discount=0, total=amount, currency=currency)
    db.add(order)
    db.flush()
    db.refresh(order)

    order_item = OrderItem(order_id=order.id, course_id=course_id, price=amount)
    db.add(order_item)

    gateway = get_payment_provider()
    context = PaymentContext(
        gateway=gateway,
        is_sandbox=is_sandbox(),
        enrollment_id=enrollment.id,
        amount=amount,
        currency=currency,
        buyer_email=buyer_email,
        buyer_name=buyer_name,
        external_reference=str(enrollment.id),
        user_id=user_id,
        course_id=course_id,
    )
    payment = create_payment(db, context)
    db.commit()
    db.refresh(payment)
    db.refresh(enrollment)

    return {
        "order_id": order.id,
        "enrollment_id": enrollment.id,
        "payment_id": payment.id,
        "course_id": course_id,
        "slug": course.slug,
        "title": course.title,
        "amount": amount,
        "currency": currency,
        "status": enrollment.status,
        "gateway": gateway.value,
    }


def confirm_payment_from_gateway(db: Session, *, gateway: str, payload: dict) -> dict:
    """Confirma pagamento via webhook/gateway e ativa matrícula se pago."""
    result = handle_payment_event(db, gateway, payload)
    return result
