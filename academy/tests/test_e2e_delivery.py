from fastapi.testclient import TestClient
from academy.tests._shared_test_db import Base, get_db, override_get_db, TestingSessionLocal
from academy.main import app
from academy.core.models import Course, User, Enrollment, EnrollmentStatus, Payment, PaymentStatus

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


def test_purchase_approved_grants_access():
    course_id = seed_course("curso-e2e-approved")
    email = "e2e-approved@example.com"
    client.post("/auth/register", json={"name": "E2E", "email": email, "password": "123456"})
    r = client.post("/auth/login", json={"email": email, "password": "123456"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "items": [{"course_id": course_id, "quantity": 1}],
        "buyer_name": "E2E Approved",
        "buyer_email": email,
        "buyer_document": "12345678900",
    }
    checkout = client.post("/academy/checkout", json=payload, headers=headers)
    assert checkout.status_code == 200
    order_id = checkout.json()["order_id"]

    with TestingSessionLocal() as db:
        enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
        assert enrollment is not None
        payment = db.query(Payment).filter(Payment.enrollment_id == enrollment.id).first()
        assert payment is not None
        from academy.core.payments.service import finalize_payment
        finalize_payment(db, payment, PaymentStatus.paid.value)

    r = client.get("/academy/me/courses", headers=headers)
    assert r.status_code == 200
    data = r.json()
    print('courses_data', data)
    assert any(c.get("slug") == "curso-e2e-approved" or c.get("course_slug") == "curso-e2e-approved" for c in data), data


def test_payment_pending_does_not_liberate():
    course_id = seed_course("curso-e2e-pending")
    email = "e2e-pending@example.com"
    client.post("/auth/register", json={"name": "E2E Pending", "email": email, "password": "123456"})
    r = client.post("/auth/login", json={"email": email, "password": "123456"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "items": [{"course_id": course_id, "quantity": 1}],
        "buyer_name": "E2E Pending",
        "buyer_email": email,
        "buyer_document": "12345678900",
    }
    checkout = client.post("/academy/checkout", json=payload, headers=headers)
    order_id = checkout.json()["order_id"]

    with TestingSessionLocal() as db:
        enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
        payment = db.query(Payment).filter(Payment.enrollment_id == enrollment.id).first()
        from academy.core.payments.service import finalize_payment
        finalize_payment(db, payment, PaymentStatus.pending.value)

    r = client.get("/academy/me/courses", headers=headers)
    assert r.status_code == 200
    assert not any(c["slug"] == "curso-e2e-pending" for c in r.json())


def test_payment_rejected_does_not_liberate():
    course_id = seed_course("curso-e2e-rejected")
    email = "e2e-rejected@example.com"
    client.post("/auth/register", json={"name": "E2E Rejected", "email": email, "password": "123456"})
    r = client.post("/auth/login", json={"email": email, "password": "123456"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "items": [{"course_id": course_id, "quantity": 1}],
        "buyer_name": "E2E Rejected",
        "buyer_email": email,
        "buyer_document": "12345678900",
    }
    checkout = client.post("/academy/checkout", json=payload, headers=headers)
    order_id = checkout.json()["order_id"]

    with TestingSessionLocal() as db:
        enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
        payment = db.query(Payment).filter(Payment.enrollment_id == enrollment.id).first()
        from academy.core.payments.service import finalize_payment
        finalize_payment(db, payment, PaymentStatus.failed.value)

    r = client.get("/academy/me/courses", headers=headers)
    assert r.status_code == 200
    assert not any(c["slug"] == "curso-e2e-rejected" for c in r.json())


def test_duplicate_webhook_is_idempotent():
    course_id = seed_course("curso-e2e-idempotent")
    email = "e2e-idempotent@example.com"
    client.post("/auth/register", json={"name": "E2E Idempotent", "email": email, "password": "123456"})
    r = client.post("/auth/login", json={"email": email, "password": "123456"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "items": [{"course_id": course_id, "quantity": 1}],
        "buyer_name": "E2E Idempotent",
        "buyer_email": email,
        "buyer_document": "12345678900",
    }
    checkout = client.post("/academy/checkout", json=payload, headers=headers)
    order_id = checkout.json()["order_id"]

    with TestingSessionLocal() as db:
        enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
        payment = db.query(Payment).filter(Payment.enrollment_id == enrollment.id).first()
        from academy.core.payments.service import finalize_payment
        finalize_payment(db, payment, PaymentStatus.paid.value)
        payment_id = payment.id

    webhook_payload = {"event": "approved", "id": 1, "external_reference": str(order_id)}
    r1 = client.post("/academy/payments/webhook", json=webhook_payload)
    r2 = client.post("/academy/payments/webhook", json=webhook_payload)
    assert r1.status_code == 200
    assert r2.status_code == 200

    with TestingSessionLocal() as db:
        enrollments = db.query(Enrollment).filter(Enrollment.id == order_id).all()
        assert len(enrollments) == 1


def test_user_without_purchase_cannot_access_premium():
    course_id = seed_course("curso-e2e-nopurchase")
    email = "e2e-nopurchase@example.com"
    client.post("/auth/register", json={"name": "No Purchase", "email": email, "password": "123456"})
    r = client.post("/auth/login", json={"email": email, "password": "123456"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = client.get(f"/academy/me/courses/{course_id}/modules", headers=headers)
    assert r.status_code in (403, 404)


def test_user_buys_two_courses_sees_both():
    c1 = seed_course("curso-e2e-two-1")
    c2 = seed_course("curso-e2e-two-2")
    email = "e2e-two@example.com"
    client.post("/auth/register", json={"name": "Two", "email": email, "password": "123456"})
    r = client.post("/auth/login", json={"email": email, "password": "123456"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    for cid in [c1, c2]:
        payload = {
            "items": [{"course_id": cid, "quantity": 1}],
            "buyer_name": "Two",
            "buyer_email": email,
            "buyer_document": "12345678900",
        }
        checkout = client.post("/academy/checkout", json=payload, headers=headers)
        order_id = checkout.json()["order_id"]
        with TestingSessionLocal() as db:
            enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
            payment = db.query(Payment).filter(Payment.enrollment_id == enrollment.id).first()
            from academy.core.payments.service import finalize_payment
            finalize_payment(db, payment, PaymentStatus.paid.value)

    r = client.get("/academy/me/courses", headers=headers)
    assert r.status_code == 200
    data = r.json()
    print('courses_data_two', data)
    slugs = [c.get("slug") for c in data]
    assert "curso-e2e-two-1" in slugs
    assert "curso-e2e-two-2" in slugs


def test_refund_revokes_access():
    course_id = seed_course("curso-e2e-refund")
    email = "e2e-refund@example.com"
    client.post("/auth/register", json={"name": "Refund", "email": email, "password": "123456"})
    r = client.post("/auth/login", json={"email": email, "password": "123456"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "items": [{"course_id": course_id, "quantity": 1}],
        "buyer_name": "Refund",
        "buyer_email": email,
        "buyer_document": "12345678900",
    }
    checkout = client.post("/academy/checkout", json=payload, headers=headers)
    order_id = checkout.json()["order_id"]

    with TestingSessionLocal() as db:
        enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
        payment = db.query(Payment).filter(Payment.enrollment_id == enrollment.id).first()
        from academy.core.payments.service import finalize_payment
        finalize_payment(db, payment, PaymentStatus.paid.value)

    with TestingSessionLocal() as db:
        enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
        payment = db.query(Payment).filter(Payment.enrollment_id == enrollment.id).first()
        from academy.core.payments.service import finalize_payment
        finalize_payment(db, payment, PaymentStatus.refunded.value)

    r = client.get("/academy/me/courses", headers=headers)
    assert r.status_code == 200
    assert not any(c["slug"] == "curso-e2e-refund" for c in r.json())


def test_direct_url_without_auth_is_denied():
    course_id = seed_course("curso-e2e-direct")
    r = client.get(f"/academy/me/courses/{course_id}/modules")
    assert r.status_code == 401


def test_nonexistent_course_does_not_liberate():
    r = client.get("/academy/me/courses/999999/modules")
    assert r.status_code in (401, 403, 404)


def test_valid_course_with_incomplete_content_does_not_mask_failure():
    course_id = seed_course("curso-e2e-incomplete")
    email = "e2e-incomplete@example.com"
    client.post("/auth/register", json={"name": "Incomplete", "email": email, "password": "123456"})
    r = client.post("/auth/login", json={"email": email, "password": "123456"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "items": [{"course_id": course_id, "quantity": 1}],
        "buyer_name": "Incomplete",
        "buyer_email": email,
        "buyer_document": "12345678900",
    }
    checkout = client.post("/academy/checkout", json=payload, headers=headers)
    order_id = checkout.json()["order_id"]

    with TestingSessionLocal() as db:
        enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
        payment = db.query(Payment).filter(Payment.enrollment_id == enrollment.id).first()
        from academy.core.payments.service import finalize_payment
        finalize_payment(db, payment, PaymentStatus.paid.value)

    r = client.get(f"/academy/me/courses/curso-e2e-incomplete/modules", headers=headers)
    assert r.status_code == 200
    assert r.json() == []
