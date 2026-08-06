import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"C:\Users\Carolina\praia-digital").resolve()))

from academy.tests._shared_test_db import Base, get_db, override_get_db, TestingSessionLocal
from academy.core.models import Lead, LeadEvent, User, Course
from academy.core.security import hash_password
from academy.main import app
from fastapi.testclient import TestClient

Base.metadata.create_all(bind=TestingSessionLocal.kw["bind"])

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

db = TestingSessionLocal()
try:
    course = db.query(Course).filter(Course.slug == "curso-lead-teste").first()
    if not course:
        course = Course(slug="curso-lead-teste", title="Curso Lead Teste", description="Teste", status="published", price=9900, currency="BRL")
        db.add(course)
        db.commit()
        db.refresh(course)
    course_id = course.id

    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(name="Admin Teste", email="admin@example.com", password_hash=hash_password("test"), role="admin")
        db.add(user)
        db.commit()
        db.refresh(user)
    user_id = user.id
finally:
    db.close()
