import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"C:\Users\Carolina\praia-digital").resolve()))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from academy.core.database import Base, get_db
from academy.core.models import Course, Module, Lesson, User, Enrollment
from academy.main import app
from fastapi.testclient import TestClient

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

course_id = None
with TestingSessionLocal() as db:
    course = Course(slug="curso-player-teste", title="Curso Player Teste", description="Teste", status="published", price=9900, currency="BRL")
    db.add(course)
    db.commit()
    db.refresh(course)
    course_id = course.id
    module = Module(course_id=course.id, order=1, title="Módulo 1", description="Descrição")
    db.add(module)
    db.commit()
    db.refresh(module)
    lesson = Lesson(module_id=module.id, order=1, title="Aula 1", content_type="text", duration_minutes=10)
    db.add(lesson)
    db.commit()
    db.refresh(lesson)

# register/login
r = client.post("/auth/register", json={"name": "Aluno Teste", "email": "aluno@example.com", "password": "123456"})
assert r.status_code == 200, r.text
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# create enrollment manually using scalar ids
with TestingSessionLocal() as db:
    user = db.query(User).filter(User.email == "aluno@example.com").first()
    enrollment = Enrollment(user_id=user.id, course_id=course_id, status="active", access_until=None, source="checkout")
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

# frontend pages mounted
r = client.get("/education/aluno/login.html")
assert r.status_code == 200, r.text

r = client.get("/education/aluno/index.html")
assert r.status_code == 200, r.text

r = client.get("/education/aluno/curso.html")
assert r.status_code == 200, r.text

print("fase3 all checks passed")
