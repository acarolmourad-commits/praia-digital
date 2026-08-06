#!/usr/bin/env python3
"""
Pre-deploy validation for Praia Digital Academy on Render.
Checks that all required files, configs, and environment variables are ready.
"""
import sys
from pathlib import Path

REQUIRED_FILES = [
    "academy/main.py",
    "academy/core/config.py",
    "academy/core/security.py",
    "academy/routers/payments.py",
    "academy/.env.production.example",
    "academy/.env.example",
    "render.yaml",
    "docs/render-academy-manual-steps.md",
    "docs/render-academy-deploy.md",
    "docs/deploy-readiness.md",
    "scripts/check_academy_deploy.py",
    "scripts/frontend_health_check.py",
    "scripts/check_deploy_docs.py",
]

REQUIRED_VARS = [
    "SECRET_KEY",
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USER",
    "SMTP_PASSWORD",
    "EMAIL_FROM",
    "ALLOWED_ORIGINS",
    "MERCADOPAGO_API_URL",
    "MERCADOPAGO_TOKEN",
    "MERCADOPAGO_PUBLIC_KEY",
    "WHATSAPP_API_URL",
    "WHATSAPP_TOKEN",
    "WHATSAPP_PHONE_ID",
    "WHATSAPP_TO_NUMBER",
    "BASE_URL",
    "DATABASE_URL",
]

BASE_URL_VALUE = "https://academy.praia.digital"

ok = True
base = Path(".")

# Check files
for f in REQUIRED_FILES:
    if not (base / f).exists():
        print(f"MISSING file: {f}")
        ok = False
    else:
        print(f"OK file: {f}")

# Check BASE_URL in render.yaml and .env files
for cfg in ["render.yaml", "academy/.env.production.example", "academy/.env.example"]:
    p = base / cfg
    if p.exists():
        txt = p.read_text(encoding="utf-8", errors="ignore")
        if BASE_URL_VALUE not in txt:
            print(f"MISSING BASE_URL={BASE_URL_VALUE} in {cfg}")
            ok = False
        else:
            print(f"OK BASE_URL in {cfg}")

# Check required variables are documented in .env.production.example
env_example = base / "academy/.env.production.example"
if env_example.exists():
    txt = env_example.read_text(encoding="utf-8", errors="ignore")
    for var in REQUIRED_VARS:
        if var not in txt:
            print(f"MISSING var doc: {var} in .env.production.example")
            ok = False
        else:
            print(f"OK var doc: {var}")

# Check frontend assets
for asset in ["img/logo.png", "img/default-home.jpg", "favicon.ico", "manifest.json"]:
    if not (base / asset).exists():
        print(f"MISSING asset: {asset}")
        ok = False
    else:
        print(f"OK asset: {asset}")

# Check git remotes
import subprocess
try:
    remote = subprocess.check_output(["git", "remote", "get-url", "origin"], text=True).strip()
    if "acarolmourad-commits/praia-digital" not in remote:
        print(f"UNEXPECTED remote: {remote}")
        ok = False
    else:
        print(f"OK remote: {remote}")
except Exception as e:
    print(f"ERROR checking git remote: {e}")
    ok = False

if ok:
    print("\nPRE-DEPLOY CHECKS PASSED")
    sys.exit(0)
else:
    print("\nPRE-DEPLOY CHECKS FAILED")
    sys.exit(1)
