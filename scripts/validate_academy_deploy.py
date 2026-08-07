#!/usr/bin/env python3
"""Validação pós-deploy da Academy no Render."""
import sys
import requests
from typing import Any, Dict, Optional

PRIMARY_BASE = "https://academy.praia.digital"
RENDER_BASE = "https://praia-digital-academy.onrender.com"


def check(base: str, name: str, method: str, path: str, payload: Optional[Dict[str, Any]], expected_status: int) -> Tuple[bool, Optional[str], Optional[int]]:
    url = base + path
    try:
        if method == "GET":
            r = requests.get(url, timeout=30)
        else:
            r = requests.post(url, json=payload, timeout=30)
    except requests.RequestException as e:
        return False, f"request error: {e}", None

    if r.status_code != expected_status:
        return False, f"status {r.status_code}, expected {expected_status}, body={r.text[:200]}", r.status_code

    return True, None, r.status_code


checks = [
    ("health", "GET", "/health", None, 200),
    ("docs", "GET", "/docs", None, 200),
    ("register", "POST", "/auth/register", {"name": "Carol Teste", "email": "deploy-check@example.com", "password": "123456"}, 200),
    ("leads_public", "POST", "/leads", {"name": "Deploy Check", "email": "lead-deploy@example.com", "source": "deploy"}, 200),
    ("monitoring", "GET", "/monitoring/status", None, 200),
]

failures = 0
base = PRIMARY_BASE
for name, method, path, payload, expected_status in checks:
    ok, err, status_code = check(base, name, method, path, payload, expected_status)
    if not ok:
        if base == PRIMARY_BASE:
            print(f"WARN {name}: {err}")
            print("Trying Render default URL...")
            base = RENDER_BASE
            ok, err, status_code = check(base, name, method, path, payload, expected_status)
        if not ok:
            print(f"FAIL {name}: {err}")
            failures += 1
            continue
    print(f"OK   {name}: {status_code} at {base}")

if failures:
    print(f"\n{failures} failure(s)")
    sys.exit(1)
print("\nAll checks passed")
