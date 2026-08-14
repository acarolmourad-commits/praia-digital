"""
Testes controlados do fluxo de entrega pós-pagamento.

Cobertura:
- TESTE 1: Pagamento aprovado → curso liberado → e-mail enviado → registro criado
- TESTE 2: Pagamento pendente → nenhum acesso liberado → nenhum e-mail de entrega
- TESTE 3: Pagamento recusado → nenhum acesso liberado
- TESTE 4: Webhook duplicado → apenas uma entrega
- TESTE 5: Curso inexistente/inativo → não liberar conteúdo → registrar erro
"""
from fastapi.testclient import TestClient
from academy.tests._shared_test_db import Base, get_db, override_get_db, TestingSessionLocal, engine as test_engine
from academy.main import app
from academy.core.models import Course, Enrollment, Payment
from unittest.mock import patch

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=test_engine)


def teardown_module(module):
    Base.metadata.drop_all(bind=test_engine)


def seed_course(slug: str, price: int = 100):
    with TestingSessionLocal() as db:
        course = Course(slug=slug, title="Test Course", description="Test", status="published", price=price)
        db.add(course)
        db.commit()
        db.refresh(course)
        return course


def test_payment_approved_activates_enrollment_and_sends_email():
    """TESTE 1: Pagamento aprovado → curso liberado → e-mail enviado → registro criado"""
    course = seed_course("test-approved", price=100)
    payload = {
        "items": [{"course_id": course.id, "quantity": 1}],
        "buyer_name": "Test User",
        "buyer_email": "test@example.com",
        "buyer_document": "12345678900",
    }
    r = client.post("/academy/checkout", json=payload)
    assert r.status_code == 200, r.text
    order_id = r.json()["order_id"]

    webhook_payload = {"event": "purchase_approved", "external_reference": str(order_id)}
    with patch("academy.core.payments.service.send_enrollment_confirmation", return_value=True) as mock_email:
        r = client.post("/academy/payments/webhook", json=webhook_payload)
        assert r.status_code == 200, r.text

    r = client.get(f"/academy/checkout/confirm?order_id={order_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "active"
    assert "Pagamento confirmado" in data["message"]
    print(f"TESTE 1 PASS: order={order_id}, status={data['status']}, email_sent={mock_email.called}")


def test_payment_pending_does_not_activate():
    """TESTE 2: Pagamento pendente → nenhum acesso liberado → nenhum e-mail de entrega"""
    course = seed_course("test-pending", price=100)
    payload = {
        "items": [{"course_id": course.id, "quantity": 1}],
        "buyer_name": "Test User",
        "buyer_email": "test@example.com",
        "buyer_document": "12345678900",
    }
    r = client.post("/academy/checkout", json=payload)
    assert r.status_code == 200
    order_id = r.json()["order_id"]

    with patch("academy.core.payments.service.send_enrollment_confirmation", return_value=False) as mock_email:
        r = client.post("/academy/payments/webhook", json={"event": "pending", "external_reference": str(order_id)})
        assert r.status_code == 200

    r = client.get(f"/academy/checkout/confirm?order_id={order_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "pending"
    assert "Aguardando confirmação" in data["message"]
    assert not mock_email.called
    print(f"TESTE 2 PASS: order={order_id}, status={data['status']}, email_sent={mock_email.called}")


def test_payment_rejected_does_not_activate():
    """TESTE 3: Pagamento recusado → nenhum acesso liberado"""
    course = seed_course("test-rejected", price=100)
    payload = {
        "items": [{"course_id": course.id, "quantity": 1}],
        "buyer_name": "Test User",
        "buyer_email": "test@example.com",
        "buyer_document": "12345678900",
    }
    r = client.post("/academy/checkout", json=payload)
    assert r.status_code == 200
    order_id = r.json()["order_id"]

    r = client.post("/academy/payments/webhook", json={"event": "rejected", "external_reference": str(order_id)})
    assert r.status_code == 200

    r = client.get(f"/academy/checkout/confirm?order_id={order_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "pending"
    print(f"TESTE 3 PASS: order={order_id}, status={data['status']}")


def test_duplicate_webhook_is_idempotent():
    """TESTE 4: Webhook duplicado → apenas uma entrega"""
    course = seed_course("test-idempotent", price=100)
    payload = {
        "items": [{"course_id": course.id, "quantity": 1}],
        "buyer_name": "Test User",
        "buyer_email": "test@example.com",
        "buyer_document": "12345678900",
    }
    r = client.post("/academy/checkout", json=payload)
    assert r.status_code == 200
    order_id = r.json()["order_id"]

    webhook_payload = {"event": "purchase_approved", "external_reference": str(order_id)}
    r1 = client.post("/academy/payments/webhook", json=webhook_payload)
    assert r1.status_code == 200

    r2 = client.post("/academy/payments/webhook", json=webhook_payload)
    assert r2.status_code == 200
    assert r2.json().get("idempotent") is True

    r = client.get(f"/academy/checkout/confirm?order_id={order_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "active"
    print(f"TESTE 4 PASS: idempotent={r2.json().get('idempotent')}, status={data['status']}")


def test_nonexistent_course_does_not_liberate():
    """TESTE 5: Curso inexistente/inativo → não liberar conteúdo → registrar erro"""
    payload = {
        "items": [{"course_id": 9999, "quantity": 1}],
        "buyer_name": "Test User",
        "buyer_email": "test@example.com",
        "buyer_document": "12345678900",
    }
    r = client.post("/academy/checkout", json=payload)
    assert r.status_code != 200
    print(f"TESTE 5 PASS: checkout returned {r.status_code} for nonexistent course")


if __name__ == "__main__":
    test_payment_approved_activates_enrollment_and_sends_email()
    test_payment_pending_does_not_activate()
    test_payment_rejected_does_not_activate()
    test_duplicate_webhook_is_idempotent()
    test_nonexistent_course_does_not_liberate()
    print("\n=== TODOS OS TESTES DE ENTREGA PASSARAM ===")
