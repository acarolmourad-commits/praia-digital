#!/usr/bin/env python3
"""Validação pós-deploy da Academy em produção."""
import json, re, sys
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

BASE = Path(r'C:\Users\Carolina\praia-digital')
REQUIRED_SLUGS = [
    'airbnb-do-zero',
    'booking-do-zero',
    'venda-rapida-imoveis-litoral',
    'crm-para-corretores',
    'automacao-comercial',
    'financiamento-imobiliario',
]


def fetch_json(url, timeout=20):
    try:
        with urlopen(url, timeout=timeout) as r:
            if r.status != 200:
                return None, r.status
            return json.loads(r.read().decode('utf-8', errors='ignore')), r.status
    except (HTTPError, URLError, Exception) as e:
        return None, str(e)


def fetch_text(url, timeout=20):
    try:
        with urlopen(url, timeout=timeout) as r:
            if r.status != 200:
                return None, r.status
            return r.read().decode('utf-8', errors='ignore'), r.status
    except (HTTPError, URLError, Exception) as e:
        return None, str(e)


def validate_health(base_url):
    url = f"{base_url}/health"
    data, status = fetch_json(url)
    if data is None:
        return False, f"health failed: {status}"
    if data.get('status') != 'ok':
        return False, f"health status != ok: {data}"
    return True, 'health ok'


def validate_courses(base_url):
    url = f"{base_url}/courses"
    data, status = fetch_json(url)
    if data is None:
        return False, f"courses failed: {status}"
    items = data.get('items') or data.get('courses') or []
    if not isinstance(items, list):
        return False, f"courses unexpected shape: {type(items)}"
    slugs = [i.get('slug') for i in items if isinstance(i, dict)]
    missing = [s for s in REQUIRED_SLUGS if s not in slugs]
    if missing:
        return False, f"missing slugs: {missing}"
    return True, f"courses ok ({len(slugs)} items)"


def validate_checkout_page(base_url):
    slug = REQUIRED_SLUGS[0]
    url = f"{base_url}/education/checkout.html?slug={slug}&title=Teste&price=100"
    text, status = fetch_text(url)
    if text is None:
        return False, f"checkout page failed: {status}"
    if slug not in text:
        return False, 'checkout page missing slug in response'
    return True, 'checkout page ok'


def validate_slugs_remote(base_url):
    ok = []
    fail = []
    for slug in REQUIRED_SLUGS:
        url = f"{base_url}/education/cursos/{slug}/index.html"
        text, status = fetch_text(url)
        if text is None or status != 200:
            fail.append((slug, status))
        else:
            ok.append(slug)
    if fail:
        return False, f"slug pages failed: {fail}"
    return True, f"slug pages ok ({ok})"


def main():
    base = 'https://academy.praia.digital'
    checks = [
        ('health', validate_health(base)),
        ('courses', validate_courses(base)),
        ('checkout', validate_checkout_page(base)),
        ('slugs', validate_slugs_remote(base)),
    ]
    passed = 0
    failed = 0
    for name, result in checks:
        ok, msg = result if isinstance(result, tuple) else (bool(result), str(result))
        print(f"{name}: {msg}")
        if ok:
            passed += 1
        else:
            failed += 1
    print(f"result: {passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
