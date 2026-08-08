from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
from academy.core.database import get_db
from academy.core.models import (
    Course, Module, Lesson, ContentAttachment,
    User, Enrollment, Progress, Certificate, Order
)
from academy.core.schemas import (
    CourseOut, ModuleOut, LessonOut, ContentAttachmentOut,
    LessonContentOut, EnrollmentOut, ProgressOut, UserOut, OrderOut
)
from academy.core.security import get_current_user, admin_required
from datetime import datetime
import os
import uuid

router = APIRouter(prefix="/admin", tags=["admin"])

# Course CRUD
@router.post("/courses", response_model=CourseOut)
def create_course(
    title: str = Form(...),
    slug: str = Form(...),
    subtitle: Optional[str] = Form(None),
    headline: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    level: Optional[str] = Form(None),
    duration: Optional[str] = Form(None),
    price: Optional[int] = Form(None),
    currency: str = Form("BRL"),
    status: str = Form("draft"),
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    course = Course(
        title=title,
        slug=slug,
        subtitle=subtitle,
        headline=headline,
        description=description,
        level=level,
        duration=duration,
        price=price,
        currency=currency,
        status=status,
        published_at=datetime.utcnow() if status == "published" else None,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.put("/courses/{course_id}", response_model=CourseOut)
def update_course(
    course_id: int,
    title: Optional[str] = Form(None),
    subtitle: Optional[str] = Form(None),
    headline: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    level: Optional[str] = Form(None),
    duration: Optional[str] = Form(None),
    price: Optional[int] = Form(None),
    currency: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    
    for field in ["title", "subtitle", "headline", "description", "level", "duration", "price", "currency", "status"]:
        value = locals().get(field)
        if value is not None:
            setattr(course, field, value)
    
    if status == "published" and not course.published_at:
        course.published_at = datetime.utcnow()
    
    db.commit()
    db.refresh(course)
    return course

@router.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db), admin=Depends(admin_required)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    db.delete(course)
    db.commit()
    return {"message": "Curso excluído."}

# Module CRUD
@router.post("/courses/{course_id}/modules", response_model=ModuleOut)
def create_module(
    course_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    order: int = Form(...),
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")
    
    module = Module(course_id=course_id, title=title, description=description, order=order)
    db.add(module)
    db.commit()
    db.refresh(module)
    return module

@router.put("/modules/{module_id}", response_model=ModuleOut)
def update_module(
    module_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    order: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado.")
    
    for field in ["title", "description", "order"]:
        value = locals().get(field)
        if value is not None:
            setattr(module, field, value)
    
    db.commit()
    db.refresh(module)
    return module

@router.delete("/modules/{module_id}")
def delete_module(module_id: int, db: Session = Depends(get_db), admin=Depends(admin_required)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado.")
    db.delete(module)
    db.commit()
    return {"message": "Módulo excluído."}

# Lesson CRUD
@router.post("/modules/{module_id}/lessons", response_model=LessonOut)
def create_lesson(
    module_id: int,
    title: str = Form(...),
    content_type: str = Form("text"),
    content_url: Optional[str] = Form(None),
    duration_minutes: Optional[int] = Form(None),
    order: int = Form(...),
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado.")
    
    lesson = Lesson(
        module_id=module_id,
        title=title,
        content_type=content_type,
        content_url=content_url,
        duration_minutes=duration_minutes,
        order=order,
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson

@router.put("/lessons/{lesson_id}", response_model=LessonOut)
def update_lesson(
    lesson_id: int,
    title: Optional[str] = Form(None),
    content_type: Optional[str] = Form(None),
    content_url: Optional[str] = Form(None),
    duration_minutes: Optional[int] = Form(None),
    order: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Aula não encontrada.")
    
    for field in ["title", "content_type", "content_url", "duration_minutes", "order"]:
        value = locals().get(field)
        if value is not None:
            setattr(lesson, field, value)
    
    db.commit()
    db.refresh(lesson)
    return lesson

@router.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db), admin=Depends(admin_required)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Aula não encontrada.")
    db.delete(lesson)
    db.commit()
    return {"message": "Aula excluída."}

# Material upload
@router.post("/lessons/{lesson_id}/materials", response_model=ContentAttachmentOut)
def upload_material(
    lesson_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Aula não encontrada.")
    
    # Save file
    upload_dir = Path(__file__).resolve().parent.parent.parent / "static" / "materials"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{file_id}{file_extension}"
    file_path = upload_dir / file_name
    
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)
    
    file_size = len(content)
    file_type = file.content_type or os.path.splitext(file.filename)[1]
    
    attachment = ContentAttachment(
        lesson_id=lesson_id,
        file_name=file.filename,
        file_url=f"/static/materials/{file_name}",
        file_type=file_type,
        file_size=file_size,
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment

@router.delete("/materials/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db), admin=Depends(admin_required)):
    attachment = db.query(ContentAttachment).filter(ContentAttachment.id == material_id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Material não encontrado.")
    
    # Delete file from filesystem
    file_path = Path(__file__).resolve().parent.parent.parent / "static" / "materials" / os.path.basename(attachment.file_url)
    if file_path.exists():
        os.remove(file_path)
    
    db.delete(attachment)
    db.commit()
    return {"message": "Material excluído."}

# Enrollment management
@router.get("/enrollments", response_model=List[EnrollmentOut])
def list_enrollments(db: Session = Depends(get_db), admin=Depends(admin_required)):
    return db.query(Enrollment).all()

@router.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), admin=Depends(admin_required)):
    return db.query(User).all()

@router.get("/orders", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db), admin=Depends(admin_required)):
    return db.query(Order).all()

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
