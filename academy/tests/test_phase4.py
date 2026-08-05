import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"C:\Users\Carolina\praia-digital").resolve()))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from academy.core.database import Base, get_db
from academy.core.models import Course, Module, Lesson, User, Order, OrderItem, Payment, PaymentStatus, Enrollment, Certificate
from academy.core.email_service import send_email
from academy.core.security import hash_password
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

# seed data and keep scalar ids
course_id = None
user_id = None
lesson_id = None
with TestingSessionLocal() as db:
    course = Course(slug="curso-admin-teste", title="Curso Admin Teste", description="Teste", status="published", price=9900, currency="BRL")
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
    lesson_id = lesson.id
    user = User(name="Admin Teste", email="admin@example.com", password_hash=hash_password("test"), role="admin")
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    order = Order(user_id=user.id, status="paid", subtotal=9900, discount=0, total=9900, currency="BRL")
    db.add(order)
    db.commit()
    db.refresh(order)
    order_item = OrderItem(order_id=order.id, course_id=course.id, price=9900)
    db.add(order_item)
    db.commit()
    payment = Payment(user_id=user.id, course_id=course.id, gateway="mock", gateway_payment_id="MOCK-123", status=PaymentStatus.paid, amount=9900, currency="BRL")
    db.add(payment)
    db.commit()
    db.refresh(payment)
    enrollment = Enrollment(user_id=user.id, course_id=course.id, status="active", access_until=None, source="checkout")
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    certificate = Certificate(user_id=user.id, course_id=course.id, enrollment_id=enrollment.id, code="CERT-123")
    db.add(certificate)
    db.commit()

# health
r = client.get("/health")
assert r.status_code == 200, r.text
assert r.json()["status"] == "ok"

# register student
r = client.post("/auth/register", json={"name": "Student Teste", "email": "student@example.com", "password": "123456"})
assert r.status_code == 200, r.text
student_token = r.json()["access_token"]
student_headers = {"Authorization": f"Bearer {student_token}"}

# add to cart + checkout via public payments endpoint
r = client.post("/academy/cart/add", json={"course_id": course_id}, headers=student_headers)
assert r.status_code == 200, r.text
r = client.post("/academy/checkout", json={"items": [{"course_id": course_id}]}, headers=student_headers)
assert r.status_code == 200, r.text
checkout = r.json()
assert checkout["status"] == "pending"
order_id = checkout["order_id"]
payment_id = checkout["payment_id"]

# webhook
r = client.post(f"/academy/payments/{payment_id}/webhook", json={"status": "paid"})
assert r.status_code == 200, r.text
assert r.json()["ok"] is True

# verify enrollment and progress created
r = client.get("/academy/me/enrollments", headers=student_headers)
assert r.status_code == 200, r.text
enrollments = r.json()
assert len(enrollments) == 1, enrollments
enrollment_id = enrollments[0]["id"]

# admin endpoints require admin role; test with student token returns 403
r = client.get("/admin/users", headers=student_headers)
assert r.status_code == 403, r.text

# admin endpoints work with admin token
admin_headers = {"Authorization": f"Bearer {client.post('/auth/login', json={'email':'admin@example.com','password':'test'}).json()['access_token']}"}
r = client.get("/admin/users", headers=admin_headers)
assert r.status_code == 200, r.text

# email service smoke test
result = send_email("test@example.com", "Teste Praia Digital Academy", "Corpo do e-mail de teste.")
assert isinstance(result, bool)

print("fase4 all checks passed")
