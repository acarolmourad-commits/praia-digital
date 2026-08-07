from fastapi.testclient import TestClient
from academy.tests._shared_test_db import Base, get_db, override_get_db, TestingSessionLocal
from academy.main import app
from academy.core.models import Course, User, Enrollment, EnrollmentStatus, Payment, PaymentStatus, Lead

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
Base.metadata.create_all(bind=TestingSessionLocal.kw["bind"])


def seed_course(slug: str, price: int = 9900):
    with TestingSessionLocal() as db:
        c = db.query(Course).filter(Course.slug == slug).first()
        if not c:
            c = Course(slug=slug, title=slug.replace("-", " ").title(), description="x", status="published", price=price, currency="BRL")
            db.add(c)
            db.commit()
            db.refresh(c)
        return c.id


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["service"] == "academy-api"


def test_register_login_flow():
    r = client.post("/auth/register", json={"name": "Smoke", "email": "smoke@example.com", "password": "123456"})
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    r = client.post("/auth/login", json={"email": "smoke@example.com", "password": "123456"})
    assert r.status_code == 200, r.text
    assert r.json()["access_token"]


def test_leads_public():
    payload = {"name": "Lead Smoke", "email": "lead-smoke@example.com", "source": "smoke"}
    r = client.post("/leads", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["name"] == "Lead Smoke"
    assert data["status"] == "new"
    assert data["magnet"] is None


def test_checkout_public():
    course_id = seed_course("curso-smoke")
    payload = {
        "items": [{"course_id": course_id, "quantity": 1}],
        "buyer_name": "Comprador Smoke",
        "buyer_email": "smoke-compra@example.com",
        "buyer_document": "12345678900",
    }
    r = client.post("/academy/checkout", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["status"] == "pending"
    assert data["total"] == 9900
    assert "checkout_url" in data


def test_courses_list():
    seed_course("curso-lista")
    r = client.get("/courses")
    assert r.status_code == 200, r.text
    data = r.json()
    assert any(c["slug"] == "curso-lista" for c in data), data


def test_admin_leads_unauthorized():
    r = client.get("/admin/leads")
    assert r.status_code == 403, r.text


def test_monitoring_status():
    r = client.get("/monitoring/status")
    assert r.status_code == 200, r.text


if __name__ == "__main__":
    import sys
    tests = [
        test_health,
        test_register_login_flow,
        test_leads_public,
        test_checkout_public,
        test_courses_list,
        test_admin_leads_unauthorized,
        test_monitoring_status,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"OK {t.__name__}")
        except Exception as e:
            print(f"FAIL {t.__name__}: {e}")
            failed += 1
    if failed:
        print(f"\n{failed} failure(s)")
        sys.exit(1)
    print("\nAll smoke tests passed")
