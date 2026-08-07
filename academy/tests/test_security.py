from fastapi.testclient import TestClient
from academy.main import app
from academy.core.config import SECRET_KEY as _SECRET_KEY

client = TestClient(app)


def test_request_id_header_accepted():
    r = client.get("/health", headers={"x-request-id": "test-123"})
    assert r.status_code == 200


def test_security_headers_present():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.headers.get("x-content-type-options") == "nosniff"
    assert r.headers.get("x-frame-options") == "DENY"
    assert r.headers.get("x-xss-protection") == "1; mode=block"
    assert r.headers.get("referrer-policy") == "strict-origin-when-cross-origin"
    assert r.headers.get("permissions-policy") == "camera=(), microphone=(), geolocation=()"


def test_payload_too_large_rejected():
    payload = "a" * (1024 * 1024 + 1)
    r = client.post("/leads", content=payload, headers={"content-type": "application/json"})
    assert r.status_code == 413


def test_dev_secret_key_is_not_hardcoded_production_value():
    assert _SECRET_KEY != "CHANGE_ME_IN_PRODUCTION"

