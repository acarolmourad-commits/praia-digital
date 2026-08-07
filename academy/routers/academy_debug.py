from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging
from academy.core.database import get_db
from academy.core.models import Cart, Course
from academy.core.security import get_current_user

logger = logging.getLogger("academy")

router = APIRouter(prefix="/academy", tags=["academy"])

@router.post("/cart/add")
def add_to_cart(item: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    course = db.query(Course).filter(Course.id == item["course_id"]).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    from academy.core.models import Enrollment
    existing = db.query(Enrollment).filter(Enrollment.user_id == user["id"], Enrollment.course_id == item["course_id"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="Você já possui acesso a este curso.")
    cart_item = Cart(user_id=user["id"], course_id=item["course_id"])
    db.add(cart_item)
    db.commit()
    logger.info("cart_added", extra={"user_id": cart_item.user_id, "course_id": cart_item.course_id})
    return {"message": "Curso adicionado ao carrinho."}

@router.get("/cart", response_model=List[dict])
def get_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    cart_items = db.query(Cart).filter(Cart.user_id == user["id"]).all()
    logger.info("cart_listed", extra={"count": len(cart_items), "items": [(c.user_id, c.course_id) for c in cart_items]})
    result = []
    for item in cart_items:
        course = db.query(Course).filter(Course.id == item.course_id).first()
        if course:
            result.append({"cart_id": item.id, "course_id": course.id, "title": course.title, "price": course.price, "currency": course.currency})
    return result
