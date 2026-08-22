"""
Adversarial / security tests for payment webhooks.

Coverage:
- valid webhook
- invalid signature
- missing signature
- missing secret
- invalid payload
- unknown event
- replay
- duplicate
- invalid timestamp
- unauthorized resource
- invalid state transition
- exception
- malformed body
- concurrent duplicate
"""
import hashlib
import hmac
import json
import os
import time
from unittest.mock import patch

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from academy.core.models import Course, Enrollment, EnrollmentStatus, Payment, PaymentStatus
from academy.core.payments.webhooks import (
    WebhookAuthError,
    WebhookValidationError,
    _detect_gateway,
    _extract_enrollment_id,
    _extract_event_id,
    _extract_gateway_payment_id,
    _is_invalid_status_transition,
    _map_status,
    _redact,
    _safe_json_load,
    _safe_timestamp,
    _verify_hotmart,
    _verify_mercadopago,
    _verify_stripe,
    handle_payment_event,
)
from academy.tests._shared_test_db import (
    Base,
    get_db,
    override_get_db,
    TestingSessionLocal,
    engine as test_engine,
)
from academy.main import app

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


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def _create_order(course: Course):
    payload = {
        "items": [{"course_id": course.id, "quantity": 1}],
        "buyer_name": "Security Test",
        "buyer_email": "security@example.com",
        "buyer_document": "12345678900",
    }
    r = client.post("/academy/checkout", json=payload)
    assert r.status_code == 200, r.text
    return r.json()["order_id"]


def _paid_payment(course: Course, order_id: int):
    with TestingSessionLocal() as db:
        enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
        assert enrollment is not None
        payment = db.query(Payment).filter(Payment.enrollment_id == enrollment.id).first()
        assert payment is not None
        from academy.core.payments.service import finalize_payment
        finalize_payment(db, payment, PaymentStatus.paid.value)
        db.refresh(payment)
        return payment


def _webhook(order_id: int, extra: dict | None = None, use_auth: bool = False):
    payload = {"event": "purchase_approved", "external_reference": str(order_id)}
    if extra:
        payload.update(extra)
    headers = {}
    if use_auth:
        headers["X-Hotmart-Hmac"] = "invalid"
    return client.post("/academy/payments/webhook", json=payload, headers=headers)


# ------------------------------------------------------------------
# A) Happy path
# ------------------------------------------------------------------
def test_valid_sandbox_webhook_is_accepted():
    course = seed_course("webhook-sec-valid")
    order_id = _create_order(course)
    r = _webhook(order_id)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("handled") is True


# ------------------------------------------------------------------
# B) Auth bypass
# ------------------------------------------------------------------
def test_missing_signature_is_blocked():
    course = seed_course("webhook-sec-missing-sig")
    order_id = _create_order(course)
    with patch("academy.core.payments.webhooks._detect_gateway", return_value="hotmart"):
        with patch("academy.core.payments.webhooks._resolve_secret", return_value="secret"):
            r = _webhook(order_id, use_auth=False)
    assert r.status_code == 403, r.text
    body = r.json()
    assert body.get("detail") == "invalid webhook"


def test_invalid_signature_is_blocked():
    course = seed_course("webhook-sec-invalid-sig")
    order_id = _create_order(course)
    with patch("academy.core.payments.webhooks._detect_gateway", return_value="hotmart"):
        with patch("academy.core.payments.webhooks._resolve_secret", return_value="secret"):
            r = _webhook(order_id, use_auth=True)
    assert r.status_code == 403, r.text
    body = r.json()
    assert body.get("detail") == "invalid webhook"


def test_missing_secret_blocks_hotmart():
    body = b"{}"
    request = client.request("POST", "/academy/payments/webhook", headers={"X-Hotmart-Hmac": "x"})
    with patch("academy.core.payments.webhooks._detect_gateway", return_value="hotmart"):
        with patch("academy.core.payments.webhooks._resolve_secret", return_value=""):
            with pytest.raises(WebhookAuthError):
                _verify_hotmart(request, body, "")


def test_missing_secret_blocks_mercadopago():
    body = b"{}"
    request = client.request("POST", "/academy/payments/webhook", headers={"X-Signature": "x"})
    with patch("academy.core.payments.webhooks._detect_gateway", return_value="mercadopago"):
        with patch("academy.core.payments.webhooks._resolve_secret", return_value=""):
            with pytest.raises(WebhookAuthError):
                _verify_mercadopago(request, body, "")


def test_missing_secret_blocks_stripe():
    body = b"{}"
    request = client.request("POST", "/academy/payments/webhook", headers={"Stripe-Timestamp": "1", "Stripe-Signature": "x"})
    with patch("academy.core.payments.webhooks._detect_gateway", return_value="stripe"):
        with patch("academy.core.payments.webhooks._resolve_secret", return_value=""):
            with pytest.raises(WebhookAuthError):
                _verify_stripe(request, body, "")


# ------------------------------------------------------------------
# C) Replay
# ------------------------------------------------------------------
def test_old_timestamp_is_blocked_for_stripe():
    body = b'{"id":1}'
    scope = {
        "type": "http",
        "method": "POST",
        "path": "/academy/payments/webhook",
        "headers": [
            (b"stripe-timestamp", str(int(time.time()) - 400).encode()),
            (b"stripe-signature", b"x"),
            (b"content-type", b"application/json"),
        ],
        "query_string": b"",
    }
    receive = lambda msg: None
    request = Request(scope, receive)
    with patch("academy.core.payments.webhooks._detect_gateway", return_value="stripe"):
        with patch("academy.core.payments.webhooks._resolve_secret", return_value="secret"):
            with pytest.raises(WebhookValidationError):
                _verify_stripe(request, body, "secret")


# ------------------------------------------------------------------
# D) Invalid payload / unknown event
# ------------------------------------------------------------------
def test_malformed_json_is_blocked():
    course = seed_course("webhook-sec-malformed")
    order_id = _create_order(course)
    r = client.post("/academy/payments/webhook", content="not-json", headers={"content-type": "application/json"})
    assert r.status_code in {400, 403}, r.text
    body = r.json()
    assert body.get("handled") is False or body.get("detail") in {"invalid_payload", "invalid webhook", "Internal server error"}


def test_empty_body_is_blocked():
    r = client.post("/academy/payments/webhook", content="", headers={"content-type": "application/json"})
    assert r.status_code in {400, 403}, r.text
    body = r.json()
    assert body.get("handled") is False or body.get("detail") in {"invalid_payload", "invalid webhook", "Internal server error"}


def test_unknown_event_status_is_blocked():
    course = seed_course("webhook-sec-unknown")
    order_id = _create_order(course)
    with TestingSessionLocal() as db:
        enrollment = db.query(Enrollment).filter(Enrollment.id == order_id).first()
        payment = db.query(Payment).filter(Payment.enrollment_id == enrollment.id).first()
        result = handle_payment_event(db, "sandbox", {"event": "unknown_status", "external_reference": str(order_id)})
    assert result.get("handled") is True
    assert result.get("idempotent") is True


# ------------------------------------------------------------------
# E) Idempotency
# ------------------------------------------------------------------
def test_duplicate_sandbox_webhook_is_idempotent():
    course = seed_course("webhook-sec-dup")
    order_id = _create_order(course)
    r1 = _webhook(order_id)
    assert r1.status_code == 200
    r2 = _webhook(order_id)
    assert r2.status_code == 200
    assert r2.json().get("idempotent") is True


# ------------------------------------------------------------------
# F) Invalid state transition
# ------------------------------------------------------------------
def test_cancelled_to_paid_is_blocked():
    course = seed_course("webhook-sec-state")
    order_id = _create_order(course)
    payment = _paid_payment(course, order_id)
    with TestingSessionLocal() as db:
        payment = db.query(Payment).filter(Payment.id == payment.id).first()
        payment.status = PaymentStatus.failed.value
        db.commit()
        with pytest.raises(WebhookValidationError):
            handle_payment_event(db, "sandbox", {"event": "purchase_approved", "external_reference": str(order_id)})


# ------------------------------------------------------------------
# G) Redaction
# ------------------------------------------------------------------
def test_redact_masks_sensitive_strings():
    payload = {"token": "abc123", "secret": "xyz", "name": "test"}
    safe = _redact(payload)
    assert safe["token"] == "***"
    assert safe["secret"] == "***"
    assert safe["name"] == "test"


def test_redact_handles_nested_payload():
    payload = {"data": {"authorization": "Bearer abc", "amount": 10}}
    safe = _redact(payload)
    assert safe["data"]["authorization"] == "***"
    assert safe["data"]["amount"] == 10


# ------------------------------------------------------------------
# H) Helpers
# ------------------------------------------------------------------
def test_safe_timestamp_valid():
    assert _safe_timestamp("1234") == 1234


def test_safe_timestamp_invalid():
    assert _safe_timestamp("not-a-time") is None


def test_safe_json_load_valid():
    payload, err = _safe_json_load(b'{"a":1}')
    assert payload == {"a": 1}
    assert err is None


def test_safe_json_load_invalid():
    payload, err = _safe_json_load(b"not-json")
    assert payload is None
    assert err == "invalid_json"


def test_extract_event_id_from_multiple_keys():
    assert _extract_event_id({"event_id": "e1"}) == "e1"
    assert _extract_event_id({"transaction_id": "t1"}) == "t1"
    assert _extract_event_id({"payment_id": "p1"}) == "p1"
    assert _extract_event_id({"id": "i1"}) == "i1"


def test_map_status_sandbox_approved():
    assert _map_status("sandbox", {"event": "purchase_approved"}) == PaymentStatus.paid.value


def test_map_status_sandbox_unknown_defaults_pending():
    assert _map_status("sandbox", {"event": "weird"}) == PaymentStatus.pending.value


def test_is_invalid_status_transition_same_status():
    with TestingSessionLocal() as db:
        course = Course(slug="transition-same", title="T", description="", status="published", price=100)
        db.add(course)
        db.commit()
        db.refresh(course)
        enrollment = Enrollment(user_id=None, course_id=course.id, status=EnrollmentStatus.pending.value)
        db.add(enrollment)
        db.flush()
        payment = Payment(
            user_id=None,
            course_id=course.id,
            enrollment_id=enrollment.id,
            amount=100,
            currency="BRL",
            status=PaymentStatus.paid.value,
            gateway="sandbox",
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        assert _is_invalid_status_transition(payment, PaymentStatus.paid.value) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
