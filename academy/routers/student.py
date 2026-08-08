from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from academy.core.database import get_db
from academy.core.models import Course, Module, Lesson, Enrollment, Progress, ContentAttachment
from academy.core.schemas import CourseOut, ModuleOut, LessonOut, LessonContentOut, ContentAttachmentOut, ProgressOut
from academy.core.security import get_current_user_optional

router = APIRouter(prefix="/academy/me", tags=["student"])
optional_bearer = HTTPBearer(auto_error=False)

def _current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_bearer)):
    user = get_current_user_optional(credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    return user

@router.get("/courses", response_model=List[dict])
def list_my_courses(db: Session = Depends(get_db), user=Depends(_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    enrollments = db.query(Enrollment).filter(
        Enrollment.user_id == user["id"],
        Enrollment.status == "active"
    ).all()
    result = []
    for enrollment in enrollments:
        course = db.query(Course).filter(Course.id == enrollment.course_id).first()
        if not course:
            continue
        result.append({
            "enrollment_id": enrollment.id,
            "course_id": course.id,
            "slug": course.slug,
            "title": course.title,
            "status": enrollment.status,
            "access_until": enrollment.access_until,
        })
    return result

@router.get("/enrollments", response_model=List[dict])
def list_my_enrollments(db: Session = Depends(get_db), user=Depends(_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == user["id"]).all()
    result = []
    for enrollment in enrollments:
        course = db.query(Course).filter(Course.id == enrollment.course_id).first()
        result.append({
            "id": enrollment.id,
            "course_id": course.id,
            "course_slug": course.slug,
            "course_title": course.title,
            "status": enrollment.status,
            "access_until": enrollment.access_until,
        })
    return result

@router.get("/courses/{slug}/modules", response_model=List[ModuleOut])
def get_my_course_modules(slug: str, db: Session = Depends(get_db), user=Depends(_current_user)):
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
def get_my_module_lessons(module_id: int, db: Session = Depends(get_db), user=Depends(_current_user)):
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
def get_my_lesson_content(lesson_id: int, db: Session = Depends(get_db), user=Depends(_current_user)):
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

@router.get("/progress", response_model=List[dict])
def get_my_progress(db: Session = Depends(get_db), user=Depends(_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == user["id"]).all()
    result = []
    for enrollment in enrollments:
        progresses = db.query(Progress).filter(Progress.enrollment_id == enrollment.id).all()
        total = len(progresses)
        completed = sum(1 for p in progresses if p.status == "completed")
        course = db.query(Course).filter(Course.id == enrollment.course_id).first()
        result.append({
            "course_id": enrollment.course_id,
            "course_title": course.title,
            "course_slug": course.slug,
            "total_lessons": total,
            "completed_lessons": completed,
            "progress_percent": round((completed / total) * 100, 1) if total else 0,
        })
    return result

@router.post("/progress/complete", response_model=dict)
def mark_lesson_complete(lesson_id: int, db: Session = Depends(get_db), user=Depends(_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Aula não encontrada.")
    module = db.query(Module).filter(Module.id == lesson.module_id).first()
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user["id"],
        Enrollment.course_id == module.course_id,
        Enrollment.status == "active"
    ).first()
    if not enrollment:
        raise HTTPException(status_code=403, detail="Você não tem acesso a esta aula.")
    progress = db.query(Progress).filter(
        Progress.enrollment_id == enrollment.id,
        Progress.lesson_id == lesson_id
    ).first()
    if not progress:
        progress = Progress(enrollment_id=enrollment.id, lesson_id=lesson_id)
        db.add(progress)
    progress.status = "completed"
    progress.completed_at = datetime.utcnow()
    db.commit()
    return {"status": "ok"}
