#!/usr/bin/env python3
"""
Health check do frontend Praia Digital / Academy.
Uso:
  python scripts/frontend_health_check.py --base https://praia.digital
"""

import argparse
import re
import sys
import time

import requests


DEFAULT_PATHS = [
    "/",
    "/servicos.html",
    "/bairros/index.html",
    "/bairros/caraguatatuba/index.html",
    "/bairros/ubatuba/index.html",
    "/education/index.html",
    "/education/vendas.html",
    "/education/cursos/index.html",
    "/education/checkout.html",
    "/education/aluno/index.html",
    "/education/aluno/login.html",
    "/education/cursos/investindo-imoveis-litoral/index.html",
    "/education/cursos/airbnb-do-zero/index.html",
    "/education/cursos/comprar-imovel-praia-sem-golpes/index.html",
]


def check_page(base: str, path: str, timeout: int = 20):
    url = base.rstrip("/") + path
    try:
        r = requests.get(url, timeout=timeout, allow_redirects=True)
        return url, r.status_code, r.text
    except requests.RequestException as e:
        return url, None, str(e)


def assert_has(body: str, pattern: str):
    return bool(re.search(pattern, body, re.IGNORECASE))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="https://praia.digital")
    parser.add_argument("--wait", default="0")
    parser.add_argument("--paths", default=",".join(DEFAULT_PATHS))
    args = parser.parse_args()
    base = args.base.rstrip("/")
    wait = int(args.wait)
    paths = [p.strip() for p in args.paths.split(",") if p.strip()]

    if wait > 0:
        print(f"Aguardando {wait}s para propagar...")
        time.sleep(wait)

    print(f"=== Frontend Health Check — {base} ===\n")

    checks = []
    for path in paths:
        url, status, body = check_page(base, path)
        ok = status == 200
        checks.append((path, ok, status, url))
        print(f"[{'OK' if ok else 'FAIL'}] {path} -> {status}")

        if ok and body:
            has_title = assert_has(body, r"<title>.*Praia Digital.*</title>")
            has_cta = assert_has(body, r'(class="cta"|href="[^"]*(checkout|cursos|login|vendas)[^"]*")')
            has_canonical = assert_has(body, r'<link rel="canonical"')
            checks.append((f"{path}: title", has_title, "title" if has_title else "missing", url))
            checks.append((f"{path}: cta", has_cta, "cta" if has_cta else "missing", url))
            checks.append((f"{path}: canonical", has_canonical, "canonical" if has_canonical else "missing", url))

    broken = [c for c in checks if not c[1]]
    print("\n=== Resultado ===")
    print(f"Checks: {sum(1 for c in checks if c[1])}/{len(checks)} passaram")
    if broken:
        print("Itens com problema:")
        for name, ok, detail, _ in broken[:20]:
            print(f"  FAIL {name}: {detail}")
    else:
        print("Frontend OK")

    return 0 if not broken else 1


if __name__ == "__main__":
    sys.exit(main())
