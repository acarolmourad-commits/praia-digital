from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from academy.core.database import get_db
from academy.core.models import Course, Module, Lesson
from academy.core.schemas import CourseOut, ModuleOut, LessonOut

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("", response_model=List[CourseOut])
def list_courses(status: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Course)
    if status:
        q = q.filter(Course.status == status)
    else:
        q = q.filter(Course.status == "published")
    return q.order_by(Course.created_at.desc()).all()

@router.get("/{slug}", response_model=CourseOut)
def get_course(slug: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.slug == slug).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    return course

@router.get("/{slug}/modules", response_model=List[ModuleOut])
def list_modules(slug: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.slug == slug).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    return course.modules

@router.get("/modules/{module_id}/lessons", response_model=List[LessonOut])
def list_lessons(module_id: int, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado.")
    return module.lessons
