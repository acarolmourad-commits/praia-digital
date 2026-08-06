from fastapi.testclient import TestClient
from academy.tests._shared_test_db import Base, get_db, override_get_db, TestingSessionLocal
from academy.main import app
from academy.core.models import Course, EnrollmentStatus

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def seed_course(slug: str, price: int = 9900):
    with TestingSessionLocal() as db:
        course = Course(
            slug=slug,
            title=slug.replace("-", " ").title(),
            description="Teste",
            status="published",
            price=price,
        )
        db.add(course)
        db.commit()


def test_public_checkout_creates_enrollment_and_payment():
    seed_course("curso-checkout-publico")
    payload = {
        "items": [{"course_id": 1, "quantity": 1}],
        "buyer_name": "Teste Checkout",
        "buyer_email": "teste@example.com",
        "buyer_document": "12345678900",
    }
    r = client.post("/academy/checkout", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["status"] == "pending"
    assert data["order_id"] == 1
    assert data["payment_id"] == 1
    assert data["total"] == 9900
    assert "checkout_url" in data


def test_checkout_status_returns_pending():
    seed_course("curso-checkout-status")
    r = client.post("/academy/checkout", json={
        "items": [{"course_id": 2, "quantity": 1}],
        "buyer_name": "Status Test",
        "buyer_email": "status@example.com",
        "buyer_document": "12345678900",
    })
    assert r.status_code == 200
    order_id = r.json()["order_id"]
    r = client.get(f"/academy/checkout/status?order_id={order_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["order_id"] == order_id
    assert data["status"] == EnrollmentStatus.pending.value


if __name__ == "__main__":
    test_public_checkout_creates_enrollment_and_payment()
    print("public checkout checks passed")
    test_checkout_status_returns_pending()
    print("checkout status checks passed")
