#!/usr/bin/env python3
"""Validação pós-deploy da Academy no Render."""
import sys
import requests

BASE = "https://academy.praia.digital"

checks = [
    ("health", "GET", "/health", None, 200, {"status": "ok", "service": "academy-api"}),
    ("docs", "GET", "/docs", None, 200, None),
    ("register", "POST", "/auth/register", {"name": "Carol Teste", "email": "deploy-check@example.com", "password": "123456"}, 200, None),
    ("leads_public", "POST", "/leads", {"name": "Deploy Check", "email": "lead-deploy@example.com", "source": "deploy"}, 200, None),
]

failures = 0
for name, method, path, payload, expected_status, expected_json in checks:
    url = BASE + path
    try:
        if method == "GET":
            r = requests.get(url, timeout=20)
        else:
            r = requests.post(url, json=payload, timeout=20)
    except requests.RequestException as e:
        print(f"FAIL {name}: request error: {e}")
        failures += 1
        continue

    if r.status_code != expected_status:
        print(f"FAIL {name}: status {r.status_code}, expected {expected_status}, body={r.text[:160]}")
        failures += 1
        continue

    if expected_json is not None:
        try:
            data = r.json()
        except ValueError:
            print(f"FAIL {name}: invalid json: {r.text[:160]}")
            failures += 1
            continue
        for k, v in expected_json.items():
            if data.get(k) != v:
                print(f"FAIL {name}: {k}={data.get(k)!r}, expected {v!r}")
                failures += 1
                continue

    print(f"OK   {name}: {r.status_code}")

if failures:
    print(f"\n{failures} failure(s)")
    sys.exit(1)
print("\nAll checks passed")
