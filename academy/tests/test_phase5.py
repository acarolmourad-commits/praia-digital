import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"C:\Users\Carolina\praia-digital").resolve()))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from academy.core.database import Base, get_db
from academy.core.models import Course, Module, Lesson, User, Order, OrderItem, Payment, PaymentStatus, Enrollment, Certificate, UpsellRule, CrossSellRule, Cart
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

# seed data
course_id = None
with TestingSessionLocal() as db:
    course = Course(slug="curso-upsell-teste", title="Curso Upsell Teste", description="Teste", status="published", price=9900, currency="BRL")
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
    user = User(name="Student Teste", email="student@example.com", password_hash="test")
    db.add(user)
    db.commit()
    db.refresh(user)
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

# register student
r = client.post("/auth/register", json={"name": "Student Teste F5", "email": "student-f5@example.com", "password": "123456"})
assert r.status_code == 200, r.text
student_token = r.json()["access_token"]
student_headers = {"Authorization": f"Bearer {student_token}"}

# upsell/cross-sell rules empty by default
r = client.get(f"/recommendations/upsell/{course_id}", headers=student_headers)
assert r.status_code == 200, r.text
assert r.json() == []

r = client.get(f"/recommendations/cross-sell/{course_id}", headers=student_headers)
assert r.status_code == 200, r.text
assert r.json() == []

# cart recovery when no cart
r = client.post("/automation/cart-recovery", headers=student_headers)
assert r.status_code == 200, r.text
assert r.json()["message"] == "Sem carrinhos para recuperar."

# create cart and test recovery
r = client.post("/academy/cart/add", json={"course_id": course_id}, headers=student_headers)
assert r.status_code == 200, r.text
r = client.post("/automation/cart-recovery", headers=student_headers)
assert r.status_code == 200, r.text
assert "Recuperação de carrinho enviada" in r.json()["message"]

print("fase5 all checks passed")
