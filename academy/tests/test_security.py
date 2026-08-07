from fastapi.testclient import TestClient
from academy.main import app

client = TestClient(app)


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


def test_sanitize_removes_script_tags():
    from academy.core.middleware import sanitize_text

    dirty = "<script>alert('x')</script><p>ok</p>"
    clean = sanitize_text(dirty)
    assert "<script>" not in clean
    assert "<p>ok</p>" in clean
