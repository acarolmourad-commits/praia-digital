from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from academy.core.database import get_db
from academy.core.models import Cart, User, Course, EmailTemplate
from academy.core.email_service import send_email
from academy.core.security import get_current_user

router = APIRouter(prefix="/automation", tags=["automation"])

@router.post("/cart-recovery")
def cart_recovery(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    carts = db.query(Cart).filter(Cart.user_id == user["id"]).all()
    if not carts:
        return {"message": "Sem carrinhos para recuperar."}
    # Simple recovery: notify user with items in cart
    items = []
    for cart in carts:
        course = db.query(Course).filter(Course.id == cart.course_id).first()
        if course:
            items.append(course.title)
    # In production, send email with recovery link
    return {"message": f"Recuperação de carrinho enviada para {len(items)} item(ns).", "items": items}
