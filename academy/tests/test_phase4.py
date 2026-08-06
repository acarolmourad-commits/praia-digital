import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"C:\Users\Carolina\praia-digital").resolve()))

from academy.tests._shared_test_db import Base, get_db, override_get_db, TestingSessionLocal
from academy.core.models import Course, Module, Lesson, User, Order, OrderItem, Payment, PaymentStatus, Enrollment, Certificate
from academy.core.email_service import send_email
from academy.core.security import hash_password
from academy.main import app
from fastapi.testclient import TestClient

Base.metadata.create_all(bind=TestingSessionLocal.kw["bind"])

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# seed data and keep scalar ids
course_id = None
user_id = None
lesson_id = None
with TestingSessionLocal() as db:
    course = db.query(Course).filter(Course.slug == "curso-admin-teste").first()
    if not course:
        course = Course(slug="curso-admin-teste", title="Curso Admin Teste", description="Teste", status="published", price=9900, currency="BRL")
        db.add(course)
        db.commit()
        db.refresh(course)
    course_id = course.id

    module = db.query(Module).filter(Module.course_id == course_id).first()
    if not module:
        module = Module(course_id=course.id, order=1, title="Módulo 1", description="Descrição")
        db.add(module)
        db.commit()
        db.refresh(module)

    lesson = db.query(Lesson).filter(Lesson.module_id == module.id).first()
    if not lesson:
        lesson = Lesson(module_id=module.id, order=1, title="Aula 1", content_type="text", duration_minutes=10)
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
    lesson_id = lesson.id

    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(name="Admin Teste", email="admin@example.com", password_hash=hash_password("test"), role="admin")
        db.add(user)
        db.commit()
        db.refresh(user)
    user_id = user.id
