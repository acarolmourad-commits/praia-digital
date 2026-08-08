from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from academy.core.database import get_db
from academy.core.models import Course, Module, Lesson, Enrollment, ContentAttachment
from academy.core.schemas import CourseOut, ModuleOut, LessonOut, ContentAttachmentOut, LessonContentOut
from academy.core.security import get_current_user

router = APIRouter(prefix="/content", tags=["content"])

@router.get("/courses/{slug}", response_model=CourseOut)
def get_course_public(slug: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.slug == slug, Course.status == "published").first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    return course

@router.get("/courses/{slug}/modules", response_model=List[ModuleOut])
def get_course_modules(slug: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    course = db.query(Course).filter(Course.slug == slug).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user["id"],
        Enrollment.course_id == course.id,
        Enrollment.status == "active"
    ).first()
    if not enrollment:
        raise HTTPException(status_code=403, detail="Você não tem acesso a este curso.")
    
    return course.modules

@router.get("/modules/{module_id}/lessons", response_model=List[LessonOut])
def get_module_lessons(module_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado.")
    
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user["id"],
        Enrollment.course_id == module.course_id,
        Enrollment.status == "active"
    ).first()
    if not enrollment:
        raise HTTPException(status_code=403, detail="Você não tem acesso a este módulo.")
    
    return module.lessons

@router.get("/lessons/{lesson_id}", response_model=LessonContentOut)
def get_lesson_content(lesson_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
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
        Enrollment.status == "active"
    ).first()
    if not enrollment:
        raise HTTPException(status_code=403, detail="Você não tem acesso a esta aula.")
    
    attachments = db.query(ContentAttachment).filter(ContentAttachment.lesson_id == lesson_id).all()
    
    return {
        "lesson_id": lesson.id,
        "title": lesson.title,
        "content_type": lesson.content_type,
        "content_url": lesson.content_url,
        "duration_minutes": lesson.duration_minutes,
        "module_id": module.id,
        "course_id": module.course_id,
        "attachments": attachments,
    }

@router.get("/courses/{slug}/attachments")
def get_course_attachments(slug: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    
    course = db.query(Course).filter(Course.slug == slug).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user["id"],
        Enrollment.course_id == course.id,
        Enrollment.status == "active"
    ).first()
    if not enrollment:
        raise HTTPException(status_code=403, detail="Você não tem acesso a este curso.")
    
    attachments = db.query(ContentAttachment).join(Lesson).join(Module).filter(
        Module.course_id == course.id
    ).all()
    
    return [
        {
            "id": a.id,
            "lesson_id": a.lesson_id,
            "file_name": a.file_name,
            "file_url": a.file_url,
            "file_type": a.file_type,
            "file_size": a.file_size,
        }
        for a in attachments
    ]

# Public course structure (catalog/landing)
@router.get("/courses/{slug}/public", response_model=CourseOut)
def get_course_public(slug: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.slug == slug, Course.status == "published").first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    return course

@router.get("/courses/{slug}/modules/public", response_model=List[ModuleOut])
def get_course_modules_public(slug: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.slug == slug, Course.status == "published").first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    return course.modules

@router.get("/modules/{module_id}/lessons/public", response_model=List[LessonOut])
def get_module_lessons_public(module_id: int, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado.")
    return module.lessons
