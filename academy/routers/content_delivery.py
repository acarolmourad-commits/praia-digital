from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
from academy.core.database import get_db
from academy.core.models import Course, Module, Lesson, Enrollment, ContentAttachment
from academy.core.security import get_current_user_optional
from academy.core.content_source import get_content_source, ensure_content_source, resolve_course_slug
import os

router = APIRouter(prefix="/academy/content", tags=["content"])
optional_bearer = HTTPBearer(auto_error=False)


def _current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_bearer)):
    user = get_current_user_optional(credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    return user


@router.get("/courses/{slug}/filesystem-modules")
def get_course_filesystem_modules(slug: str, db: Session = Depends(get_db), user=Depends(_current_user)):
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

    source = get_content_source(db, course.id)
    if not source or not source.is_active or source.source_type != "filesystem":
        raise HTTPException(status_code=404, detail="Conteúdo não disponível para este curso.")

    fs_root = Path(source.fs_root) if source.fs_root else None
    if not fs_root or not fs_root.exists():
        raise HTTPException(status_code=404, detail="Arquivos do curso não encontrados.")

    aulas_root = fs_root / "aulas"
    if not aulas_root.exists():
        aulas_root = fs_root / "curso-completo"
    if not aulas_root.exists():
        raise HTTPException(status_code=404, detail="Estrutura de aulas não encontrada.")

    modules = []
    module_dirs = sorted([d for d in aulas_root.iterdir() if d.is_dir()], key=lambda p: p.name)
    if not module_dirs:
        module_dirs = [aulas_root]
    for module_dir in module_dirs:
        lessons = []
        if module_dir.is_dir():
            lesson_files = sorted([f for f in module_dir.iterdir() if f.is_file()], key=lambda p: p.name)
        else:
            lesson_files = []
        for lesson_file in lesson_files:
            relative_path = lesson_file.relative_to(fs_root)
            lessons.append({
                "title": lesson_file.stem.replace("-", " ").replace("_", " ").title(),
                "file_name": lesson_file.name,
                "relative_path": str(relative_path),
                "content_type": guess_content_type(lesson_file),
            })
        modules.append({
            "title": module_dir.name.replace("-", " ").replace("_", " ").title(),
            "directory": module_dir.name,
            "lessons": lessons,
        })

    return {
        "course_id": course.id,
        "slug": course.slug,
        "fs_root": str(fs_root),
        "modules": modules,
    }


@router.get("/courses/{slug}/filesystem-content")
def get_course_filesystem_content(slug: str, relative_path: str, db: Session = Depends(get_db), user=Depends(_current_user)):
    course = db.query(Course).filter(Course.slug == slug).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")

    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user["id"],
        Enrollment.course_id == course.id,
        Enrollment.status == "active"
    ).first()
    if not enrollment:
        raise HTTPException(status_code=403, detail="Você não tem acesso a este conteúdo.")

    source = get_content_source(db, course.id)
    if not source or not source.is_active or source.source_type != "filesystem":
        raise HTTPException(status_code=404, detail="Conteúdo não disponível.")

    fs_root = Path(source.fs_root) if source.fs_root else None
    if not fs_root:
        raise HTTPException(status_code=404, detail="Caminho do curso não configurado.")

    target = fs_root / relative_path
    if not str(target).startswith(str(fs_root)):
        raise HTTPException(status_code=403, detail="Acesso negado.")
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")

    content = target.read_text(encoding="utf-8", errors="ignore")
    return {
        "path": str(target.relative_to(fs_root)),
        "content": content,
        "content_type": guess_content_type(target),
    }


def guess_content_type(path: Path) -> str:
    suffix = path.suffix.lower()
    mapping = {
        ".md": "text/markdown",
        ".html": "text/html",
        ".txt": "text/plain",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".pdf": "application/pdf",
        ".zip": "application/zip",
    }
    return mapping.get(suffix, "application/octet-stream")
