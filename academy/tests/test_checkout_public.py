from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from academy.core.database import Base, get_db
from academy.main import app
from academy.core.models import Course, EnrollmentStatus

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
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


def seed_course(slug: str, price: int = 9900):
    db = TestingSessionLocal()
    try:
        course = Course(
            slug=slug,
            title=slug.replace("-", " ").title(),
            description="Teste",
            status="published",
            price=price,
        )
        db.add(course)
        db.commit()
    finally:
        db.close()


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
