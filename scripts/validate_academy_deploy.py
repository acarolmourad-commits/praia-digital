#!/usr/bin/env python3
"""Validação pós-deploy da Academy no Render."""
import sys
import requests
from typing import Any, Dict, Optional, Tuple

BASE = "https://academy.praia.digital"


def check(name: str, method: str, path: str, payload: Optional[Dict[str, Any]], expected_status: int, expected_json: Optional[Dict[str, Any]]) -> Tuple[bool, Optional[str], Optional[int], Optional[Dict[str, Any]]]:
    url = BASE + path
    try:
        if method == "GET":
            r = requests.get(url, timeout=30)
        else:
            r = requests.post(url, json=payload, timeout=30)
    except requests.RequestException as e:
        return False, f"request error: {e}", None, None

    if r.status_code != expected_status:
        return False, f"status {r.status_code}, expected {expected_status}, body={r.text[:200]}", r.status_code, None

    data = None
    if expected_json is not None:
        try:
            data = r.json()
        except ValueError:
            return False, f"invalid json: {r.text[:200]}", r.status_code, None
        for k, v in expected_json.items():
            if data.get(k) != v:
                return False, f"{k}={data.get(k)!r}, expected {v!r}", r.status_code, data

    return True, None, r.status_code, data


checks = [
    ("health", "GET", "/health", None, 200, {"status": "ok", "service": "academy-api"}),
    ("docs", "GET", "/docs", None, 200, None),
    ("register", "POST", "/auth/register", {"name": "Carol Teste", "email": "deploy-check@example.com", "password": "123456"}, 200, None),
    ("leads_public", "POST", "/leads", {"name": "Deploy Check", "email": "lead-deploy@example.com", "source": "deploy"}, 200, None),
    ("security_headers", "GET", "/health", None, 200, None),
    ("monitoring", "GET", "/monitoring/status", None, 200, None),
]

failures = 0
for item in checks:
    name, method, path, payload, expected_status, expected_json = item
    ok, err, status_code, data = check(name, method, path, payload, expected_status, expected_json)
    if not ok:
        print(f"FAIL {name}: {err}")
        failures += 1
        continue
    print(f"OK   {name}: {status_code}")

    if name == "security_headers":
        try:
            url = BASE + path
            r = requests.get(url, timeout=30)
            required_headers = {
                "x-content-type-options": "nosniff",
                "x-frame-options": "DENY",
                "x-xss-protection": "1; mode=block",
                "referrer-policy": "strict-origin-when-cross-origin",
            }
            missing = [h for h, v in required_headers.items() if r.headers.get(h) != v]
            if missing:
                print(f"FAIL security_headers: missing headers {missing}")
                failures += 1
            else:
                print("OK   security_headers: all headers present")
        except requests.RequestException as e:
            print(f"FAIL security_headers: {e}")
            failures += 1

if failures:
    print(f"\n{failures} failure(s)")
    sys.exit(1)
print("\nAll checks passed")
