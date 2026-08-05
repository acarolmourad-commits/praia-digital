from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from academy.core.database import get_db
from academy.core.models import User, UserRole, Course, Enrollment, EnrollmentStatus, Payment, PaymentStatus, Module, Lesson
from academy.core.schemas import (
    UserRegister, UserLogin, Token, UserOut,
    CourseOut, ModuleOut, LessonOut,
    EnrollmentOut, ProgressOut, PaymentOut, OrderOut, CouponOut, RecommendationOut
)
from academy.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from academy.core.security import hash_password, verify_password
from academy.core.auth import create_access_token
from typing import List, Optional

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        phone=payload.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return Token(access_token=token, role=user.role)

@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    if user.status != "active":
        raise HTTPException(status_code=403, detail="Usuário bloqueado.")
    user.last_login_at = datetime.utcnow()
    db.add(user)
    db.commit()
    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return Token(access_token=token, role=user.role)
