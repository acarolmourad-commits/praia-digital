from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from academy.core.database import get_db
from academy.core.models import Course, Enrollment, EnrollmentStatus, Payment, PaymentStatus, Order, OrderStatus, OrderItem, Module, Lesson, Progress, LessonStatus, Cart
from academy.core.schemas import CartItemIn, OrderOut, PaymentOut, EnrollmentOut
from academy.core.security import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/academy", tags=["academy"])

@router.post("/cart/add")
def add_to_cart(item: CartItemIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    course = db.query(Course).filter(Course.id == item.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    existing = db.query(Enrollment).filter(Enrollment.user_id == user["id"], Enrollment.course_id == item.course_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Você já possui acesso a este curso.")
    cart_item = Cart(user_id=user["id"], course_id=item.course_id)
    db.add(cart_item)
    db.commit()
    return {"message": "Curso adicionado ao carrinho."}

@router.get("/cart", response_model=List[dict])
def get_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    cart_items = db.query(Cart).filter(Cart.user_id == user["id"]).all()
    result = []
    for item in cart_items:
        course = db.query(Course).filter(Course.id == item.course_id).first()
        if course:
            result.append({"cart_id": item.id, "course_id": course.id, "title": course.title, "price": course.price, "currency": course.currency})
    return result

@router.post("/cart/checkout")
def checkout_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    cart_items = db.query(Cart).filter(Cart.user_id == user["id"]).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Carrinho vazio.")
    # Create order
    order = Order(user_id=user["id"], status=OrderStatus.open, subtotal=0, discount=0, total=0, currency="BRL")
    db.add(order)
    db.commit()
    db.refresh(order)
    total = 0
    for item in cart_items:
        course = db.query(Course).filter(Course.id == item.course_id).first()
        if not course:
            continue
        price = course.price or 0
        total += price
        order_item = OrderItem(order_id=order.id, course_id=course.id, price=price)
        db.add(order_item)
    order.total = total
    order.subtotal = total
    db.commit()
    db.refresh(order)
    # clear cart
    db.query(Cart).filter(Cart.user_id == user["id"]).delete()
    db.commit()
    return {"order_id": order.id, "total": order.total, "currency": order.currency, "status": order.status}

@router.post("/payments")
def create_payment(payload: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    order_id = payload.get("order_id")
    gateway = payload.get("gateway")
    gateway_payment_id = payload.get("gateway_payment_id")
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user["id"]).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    if order.status == OrderStatus.paid:
        raise HTTPException(status_code=400, detail="Pedido já pago.")
    # Create payment record
    payment = Payment(
        user_id=user["id"],
        course_id=order.items[0].course_id if order.items else None,
        gateway=gateway,
        gateway_payment_id=gateway_payment_id,
        status=PaymentStatus.pending,
        amount=order.total,
        currency=order.currency,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    # Simulate gateway redirect URL
    return {"payment_id": payment.id, "order_id": order.id, "amount": payment.amount, "currency": payment.currency, "gateway": gateway, "status": payment.status}

@router.post("/payments/{payment_id}/webhook")
def payment_webhook(payment_id: int, payload: dict, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado.")
    status = payload.get("status")
    if status == "paid":
        payment.status = PaymentStatus.paid
        payment.paid_at = datetime.utcnow()
        # Update order
        order = db.query(Order).filter(Order.user_id == payment.user_id, Order.status == OrderStatus.open).first()
        if order:
            order.status = OrderStatus.paid
            order.updated_at = datetime.utcnow()
            # Create enrollments
            for item in order.items:
                enrollment = Enrollment(
                    user_id=payment.user_id,
                    course_id=item.course_id,
                    status=EnrollmentStatus.active,
                    access_until=datetime.utcnow() + timedelta(days=365),
                    source="checkout",
                )
                db.add(enrollment)
                db.flush()  # assign id before creating progress
                # Create progress entries for all lessons
                course = db.query(Course).filter(Course.id == item.course_id).first()
                if course:
                    for module in course.modules:
                        for lesson in module.lessons:
                            progress = Progress(
                                enrollment_id=enrollment.id,
                                lesson_id=lesson.id,
                                status=LessonStatus.not_started,
                            )
                            db.add(progress)
        db.commit()
        return {"message": "Pagamento confirmado e acesso liberado."}
    elif status == "failed":
        payment.status = PaymentStatus.failed
        db.commit()
        return {"message": "Pagamento falhou."}
    elif status == "refunded":
        payment.status = PaymentStatus.refunded
        db.commit()
        return {"message": "Pagamento reembolsado."}
    raise HTTPException(status_code=400, detail="Status inválido.")
