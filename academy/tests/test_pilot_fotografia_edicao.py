from fastapi.testclient import TestClient
from academy.tests._shared_test_db import Base, get_db, override_get_db, TestingSessionLocal, engine as test_engine
from academy.main import app
from academy.core.models import Course, Enrollment, Payment

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=test_engine)


def teardown_module(module):
    Base.metadata.drop_all(bind=test_engine)


def seed_course(slug: str, price: int = 9900):
    with TestingSessionLocal() as db:
        course = Course(
            slug=slug,
            title=slug.replace("-", " ").title(),
            description="Piloto",
            status="published",
            price=price,
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        return course


def test_pilot_flow_checkout_pending():
    course = seed_course("checkout-piloto-pendente-001", price=9900)
    payload = {
        "items": [{"course_id": course.id, "quantity": 1}],
        "buyer_name": "Piloto Teste",
        "buyer_email": "piloto@example.com",
        "buyer_document": "12345678900",
    }
    r = client.post("/academy/checkout", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["status"] == "pending"
    assert data["order_id"] == 1
    assert data["payment_id"] == 1
    assert data["total"] == 9900
    assert data["gateway"] == "sandbox"
    assert "checkout_url" in data


def test_access_not_allowed_without_payment():
    course = seed_course("checkout-piloto-bloqueado-002", price=9900)
    r = client.post("/academy/checkout", json={
        "items": [{"course_id": course.id, "quantity": 1}],
        "buyer_name": "Sem Pagamento",
        "buyer_email": "sem@example.com",
        "buyer_document": "12345678900",
    })
    assert r.status_code == 200
    order_id = r.json()["order_id"]

    r = client.get(f"/academy/checkout/confirm?order_id={order_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "pending"
    assert "Aguardando confirmação" in data["message"]


def test_payment_confirmed_activates_enrollment():
    course = seed_course("checkout-piloto-aprovado-003", price=9900)
    r = client.post("/academy/checkout", json={
        "items": [{"course_id": course.id, "quantity": 1}],
        "buyer_name": "Confirmado",
        "buyer_email": "confirmado@example.com",
        "buyer_document": "12345678900",
    })
    assert r.status_code == 200
    order_id = r.json()["order_id"]

    webhook_payload = {"event": "purchase_approved", "external_reference": str(order_id)}
    r = client.post("/academy/payments/webhook", json=webhook_payload)
    assert r.status_code == 200

    r = client.get(f"/academy/checkout/confirm?order_id={order_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "active"
    assert "Pagamento confirmado" in data["message"]
    assert data["enrollment_id"] == order_id
    assert data["course_id"] == course.id
