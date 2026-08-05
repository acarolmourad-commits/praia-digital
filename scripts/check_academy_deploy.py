#!/usr/bin/env python3
"""
Pós-deploy: sanity check da Academy no Render.
Uso:
  python scripts/check_academy_deploy.py --url https://academy.praia.digital
"""

import argparse
import sys
import time
import urllib.parse
import urllib.request
import urllib.error


def fetch(url, method="GET", payload=None):
    data = None
    if payload is not None:
        data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return None, str(e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--wait", default="0")
    args = parser.parse_args()
    base = args.url.rstrip("/")
    wait = int(args.wait)

    if wait > 0:
        print(f"aguardando {wait}s para propagar...")
        time.sleep(wait)

    checks = []

    # health
    code, body = fetch(f"{base}/health")
    checks.append(("health", code == 200 and '"status":"ok"' in body.replace(" ", "").replace("'",'"')))
    print(f"health: {code} -> {checks[-1][1]}")

    # public pages
    for path in [
        "/education/index.html",
        "/education/vendas.html",
        "/education/cursos/index.html",
        "/education/aluno/login.html",
        "/education/aluno/index.html",
        "/education/aluno/curso.html",
        "/education/aluno/admin.html",
    ]:
        code, body = fetch(base + path)
        checks.append((path, code == 200 and "Praia Digital Academy" in body))
        print(f"{path}: {code} -> {checks[-1][1]}")

    # api docs
    code, body = fetch(base + "/docs")
    checks.append(("/docs", code == 200))
    print(f"/docs: {code} -> {checks[-1][1]}")

    # register
    register_url = f"{base}/auth/register"
    code, body = fetch(register_url, method="POST", payload={
        "name": "Deploy Check",
        "email": "deploy-check@example.com",
        "password": "123456",
    })
    checks.append(("/auth/register", code == 200))
    print(f"/auth/register: {code} -> {checks[-1][1]}")

    # monitoring
    code, body = fetch(base + "/monitoring/status")
    checks.append(("/monitoring/status", code == 200 and '"checks"' in body))
    print(f"/monitoring/status: {code} -> {checks[-1][1]}")

    # public checkout stub
    code, body = fetch(base + "/payments/checkout", method="POST", payload={
        "items": [{"course_id": 1, "quantity": 1}],
        "buyer_name": "Deploy Check",
        "buyer_email": "deploy-check@example.com",
        "buyer_document": "12345678900",
    })
    checks.append(("/payments/checkout", code == 200 and '"status":"pending"' in body.replace(' ', '')))
    print(f"/payments/checkout: {code} -> {checks[-1][1]}")

    print("\nRESULTADO:")
    for name, ok in checks:
        print(f"  {'OK' if ok else 'FAIL'} {name}")
    if all(ok for _, ok in checks):
        print("\nDeploy OK")
        sys.exit(0)
    else:
        print("\nDeploy com problemas")
        sys.exit(1)


if __name__ == "__main__":
    main()
