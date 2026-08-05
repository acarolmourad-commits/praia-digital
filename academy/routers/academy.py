from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from academy.core.database import get_db
from academy.core.models import Enrollment, Lesson, Module, Cart, Course
from academy.core.schemas import EnrollmentOut, ProgressOut, CartItemIn
from academy.core.security import get_current_user

router = APIRouter(prefix="/academy", tags=["academy"])

@router.get("/me/enrollments", response_model=List[EnrollmentOut])
def my_enrollments(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    return db.query(Enrollment).filter(Enrollment.user_id == user["id"]).all()

@router.get("/me/enrollments/{enrollment_id}/progress", response_model=List[ProgressOut])
def enrollment_progress(enrollment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment or enrollment.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada.")
    return enrollment.progresses

@router.post("/me/progress/{lesson_id}/complete")
def complete_lesson(lesson_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Aula não encontrada.")
    module = db.query(Module).filter(Module.id == lesson.module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado.")
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user["id"],
        Enrollment.course_id == module.course_id,
    ).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada.")
    from academy.core.models import Progress, LessonStatus
    from datetime import datetime
    progress = db.query(Progress).filter(Progress.enrollment_id == enrollment.id, Progress.lesson_id == lesson_id).first()
    if not progress:
        progress = Progress(enrollment_id=enrollment.id, lesson_id=lesson_id, status=LessonStatus.completed, completed_at=datetime.utcnow())
        db.add(progress)
    else:
        progress.status = LessonStatus.completed
        progress.completed_at = datetime.utcnow()
    db.commit()
    return {"message": "Aula marcada como concluída."}

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
    db.refresh(cart_item)
    return {"message": "Curso adicionado ao carrinho.", "cart_id": cart_item.id}

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
