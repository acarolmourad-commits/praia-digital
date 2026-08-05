import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"C:\Users\Carolina\praia-digital").resolve()))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from academy.core.database import Base, get_db
from academy.core.models import Course, Module, Lesson
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
    db.refresh(lesson)
    course_id = course.id
    lesson_id = lesson.id
finally:
    db.close()

# register/login
r = client.post("/auth/register", json={"name": "Carol Teste", "email": "carol@example.com", "password": "123456"})
assert r.status_code == 200, r.text
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# add to cart
r = client.post("/academy/cart/add", json={"course_id": course_id}, headers=headers)
assert r.status_code == 200, r.text

# get cart
r = client.get("/academy/cart", headers=headers)
assert r.status_code == 200, r.text
data = r.json()
assert any(item["course_id"] == course_id for item in data), data

# checkout
r = client.post("/academy/cart/checkout", headers=headers)
assert r.status_code == 200, r.text
order = r.json()
assert order["total"] == 9900
assert order["status"] == "open"
order_id = order["order_id"]

# create payment
r = client.post("/academy/payments", json={"order_id": order_id, "gateway": "mock", "gateway_payment_id": "MOCK-123"}, headers=headers)
assert r.status_code == 200, r.text
payment = r.json()
assert payment["amount"] == 9900
assert payment["status"] == "pending"
payment_id = payment["payment_id"]

# webhook
r = client.post(f"/academy/payments/{payment_id}/webhook", json={"status": "paid"})
assert r.status_code == 200, r.text
assert r.json()["message"] == "Pagamento confirmado e acesso liberado."

# enrollments
r = client.get("/academy/me/enrollments", headers=headers)
assert r.status_code == 200, r.text
enrollments = r.json()
assert len(enrollments) == 1, enrollments
enrollment_id = enrollments[0]["id"]

# progress
r = client.post(f"/academy/me/progress/{lesson_id}/complete", headers=headers)
assert r.status_code == 200, r.text
assert r.json()["message"] == "Aula marcada como concluída."

r = client.get(f"/academy/me/enrollments/{enrollment_id}/progress", headers=headers)
assert r.status_code == 200, r.text
progresses = r.json()
assert len(progresses) == 1, progresses
assert progresses[0]["status"] == "completed"

print("fase2 all checks passed")
