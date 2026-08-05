from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from academy.core.database import get_db
from academy.core.models import UpsellRule, CrossSellRule, Course, Coupon
from academy.core.schemas import RecommendationOut
from academy.core.security import get_current_user

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/upsell/{course_id}", response_model=List[RecommendationOut])
def get_upsell(course_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    rules = db.query(UpsellRule).filter(UpsellRule.trigger_course_id == course_id, UpsellRule.active == True).order_by(UpsellRule.priority.desc()).all()
    result = []
    for rule in rules:
        course = db.query(Course).filter(Course.id == rule.target_course_id).first()
        if course:
            result.append(RecommendationOut(course_id=course.id, title=course.title, slug=course.slug, price=course.price, discount_percent=rule.discount_percent, reason="upsell"))
    return result

@router.get("/cross-sell/{course_id}", response_model=List[RecommendationOut])
def get_cross_sell(course_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    rules = db.query(CrossSellRule).filter(CrossSellRule.trigger_course_id == course_id, CrossSellRule.active == True).order_by(CrossSellRule.priority.desc()).all()
    result = []
    for rule in rules:
        course = db.query(Course).filter(Course.id == rule.target_course_id).first()
        if course:
            result.append(RecommendationOut(course_id=course.id, title=course.title, slug=course.slug, price=course.price, discount_percent=rule.discount_percent, reason="cross-sell"))
    return result
