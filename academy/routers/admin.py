from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from academy.core.database import get_db
from academy.core.models import User, Course, Enrollment, Payment, Order, OrderStatus, Certificate, TrackingEvent, TrackingEventType, CourseContentSource, ContentSourceType
from academy.core.schemas import UserOut, CourseOut, EnrollmentOut, PaymentOut, OrderOut
from academy.core.security import get_current_user, admin_required
from academy.core.tracking import track
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

@router.get("/students/{student_id}/courses")
def admin_student_courses(student_id: int, db: Session = Depends(get_db), admin=Depends(admin_required)):
    user = db.query(User).filter(User.id == student_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == student_id).all()
    return [
        {
            "enrollment_id": e.id,
            "course_id": e.course_id,
            "status": e.status,
            "access_until": e.access_until,
            "created_at": e.created_at,
        }
        for e in enrollments
    ]

@router.get("/courses/{course_id}/students")
def admin_course_students(course_id: int, db: Session = Depends(get_db), admin=Depends(admin_required)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    enrollments = db.query(Enrollment).filter(Enrollment.course_id == course_id).all()
    return [
        {
            "user_id": e.user_id,
            "enrollment_id": e.id,
            "status": e.status,
            "access_until": e.access_until,
        }
        for e in enrollments
    ]

@router.post("/enrollments/grant")
def admin_grant_access(user_id: int, course_id: int, db: Session = Depends(get_db), admin=Depends(admin_required)):
    user = db.query(User).filter(User.id == user_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    if not user or not course:
        raise HTTPException(status_code=404, detail="Aluno ou curso não encontrado")
    enrollment = db.query(Enrollment).filter(Enrollment.user_id == user_id, Enrollment.course_id == course_id).first()
    if not enrollment:
        enrollment = Enrollment(user_id=user_id, course_id=course_id, status=EnrollmentStatus.active.value, source="manual_admin")
        db.add(enrollment)
        db.flush()
    else:
        enrollment.status = EnrollmentStatus.active.value
        enrollment.source = "manual_admin"
    enrollment.access_until = datetime.utcnow() + __import__("datetime").timedelta(days=365)
    db.commit()
    db.refresh(enrollment)
    track(db, TrackingEventType.manual_access_granted, user_id=user_id, course_id=course_id, enrollment_id=enrollment.id, payload={"admin_user_id": admin.get("id")}, commit=True)
    return {"status": "ok", "enrollment_id": enrollment.id}

@router.post("/enrollments/revoke")
def admin_revoke_access(user_id: int, course_id: int, db: Session = Depends(get_db), admin=Depends(admin_required)):
    enrollment = db.query(Enrollment).filter(Enrollment.user_id == user_id, Enrollment.course_id == course_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    enrollment.status = EnrollmentStatus.revoked.value
    db.commit()
    db.refresh(enrollment)
    track(db, TrackingEventType.manual_access_revoked, user_id=user_id, course_id=course_id, enrollment_id=enrollment.id, payload={"admin_user_id": admin.get("id")}, commit=True)
    return {"status": "ok", "enrollment_id": enrollment.id}

@router.get("/tracking/events")
def list_tracking_events(
    user_id: Optional[int] = None,
    course_id: Optional[int] = None,
    event: Optional[str] = None,
    db: Session = Depends(get_db),
    admin=Depends(admin_required),
):
    query = db.query(TrackingEvent)
    if user_id is not None:
        query = query.filter(TrackingEvent.user_id == user_id)
    if course_id is not None:
        query = query.filter(TrackingEvent.course_id == course_id)
    if event:
        query = query.filter(TrackingEvent.event == event)
    events = query.order_by(TrackingEvent.created_at.desc()).limit(200).all()
    return [
        {
            "id": ev.id,
            "user_id": ev.user_id,
            "course_id": ev.course_id,
            "enrollment_id": ev.enrollment_id,
            "event": ev.event,
            "payload": ev.payload,
            "created_at": ev.created_at,
        }
        for ev in events
    ]
