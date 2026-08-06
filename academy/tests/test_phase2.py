import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"C:\Users\Carolina\praia-digital").resolve()))

from academy.tests._shared_test_db import Base, get_db, override_get_db, TestingSessionLocal
from academy.core.models import Course, Module, Lesson
from academy.main import app
from fastapi.testclient import TestClient

Base.metadata.create_all(bind=TestingSessionLocal.kw["bind"])

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# seed course + module + lesson
db = TestingSessionLocal()
try:
    course = Course(slug="curso-checkout-teste", title="Curso Checkout Teste", description="Teste", status="published", price=9900, currency="BRL")
    db.add(course)
    db.commit()
    db.refresh(course)
    module = Module(course_id=course.id, order=1, title="Módulo 1", description="Descrição")
    db.add(module)
    db.commit()
    db.refresh(module)
    lesson = Lesson(module_id=module.id, order=1, title="Aula 1", content_type="text", duration_minutes=10)
    db.add(lesson)
    db.commit()
finally:
    db.close()
