from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from academy.core.database import get_db
from academy.core.models import User, Course, Enrollment, Payment, Order, OrderStatus, Certificate
from academy.core.schemas import UserOut, CourseOut, EnrollmentOut, PaymentOut, OrderOut
from academy.core.security import get_current_user, admin_required
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), admin=Depends(admin_required)):
    return db.query(User).all()

@router.get("/courses", response_model=List[CourseOut])
def list_courses_admin(db: Session = Depends(get_db), admin=Depends(admin_required)):
    return db.query(Course).all()

@router.get("/orders", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db), admin=Depends(admin_required)):
    return db.query(Order).all()

@router.get("/enrollments", response_model=List[EnrollmentOut])
def list_enrollments(db: Session = Depends(get_db), admin=Depends(admin_required)):
    return db.query(Enrollment).all()

@router.get("/certificates", response_model=List[dict])
def list_certificates(db: Session = Depends(get_db), admin=Depends(admin_required)):
    certs = db.query(Certificate).all()
    return [
        {
            "id": c.id,
            "user_id": c.user_id,
            "course_id": c.course_id,
            "code": c.code,
            "issued_at": c.issued_at,
        }
        for c in certs
    ]
