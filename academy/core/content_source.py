from sqlalchemy.orm import Session
from academy.core.models import Course, CourseContentSource, ContentSourceType
from pathlib import Path
from typing import Optional
import os

REPO = Path(__file__).resolve().parents[2]
COURSES_FS_ROOT = REPO / "academy" / "cursos"


def ensure_content_source(db: Session, course: Course) -> Optional[CourseContentSource]:
    if not course or not course.slug:
        return None
    existing = db.query(CourseContentSource).filter(CourseContentSource.course_id == course.id).first()
    if existing:
        return existing
    fs_path = COURSES_FS_ROOT / course.slug
    if not fs_path.exists():
        return None
    module_index = fs_path / "aulas" / "sumario.md"
    if not module_index.exists():
        module_index = fs_path / "curso-completo" / "sumario.md"
    source = CourseContentSource(
        course_id=course.id,
        source_type=ContentSourceType.filesystem.value,
        fs_root=str(fs_path),
        module_index_path=str(module_index) if module_index.exists() else None,
        is_active=True,
    )
    db.add(source)
    db.flush()
    db.refresh(source)
    return source


def get_content_source(db: Session, course_id: int) -> Optional[CourseContentSource]:
    return db.query(CourseContentSource).filter(CourseContentSource.course_id == course_id).first()


def resolve_course_slug(db: Session, course_id: int) -> Optional[str]:
    course = db.query(Course).filter(Course.id == course_id).first()
    return course.slug if course else None


def auto_ensure_all(db: Session) -> dict:
    courses = db.query(Course).all()
    result = {"total": len(courses), "created": 0, "skipped": 0, "missing_fs": 0}
    for course in courses:
        existing = db.query(CourseContentSource).filter(CourseContentSource.course_id == course.id).first()
        if existing:
            result["skipped"] += 1
            continue
        fs_path = COURSES_FS_ROOT / course.slug
        if not fs_path.exists():
            result["missing_fs"] += 1
            continue
        module_index = fs_path / "aulas" / "sumario.md"
        if not module_index.exists():
            module_index = fs_path / "curso-completo" / "sumario.md"
        source = CourseContentSource(
            course_id=course.id,
            source_type=ContentSourceType.filesystem.value,
            fs_root=str(fs_path),
            module_index_path=str(module_index) if module_index.exists() else None,
            is_active=True,
        )
        db.add(source)
        result["created"] += 1
    db.commit()
    return result
