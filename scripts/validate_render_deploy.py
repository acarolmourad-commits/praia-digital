#!/usr/bin/env python3
"""
Validação pré-deploy da Academy no Render.
Uso:
  python scripts/validate_render_deploy.py
"""

import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
REPO_ROOT = BASE

CHECKS = []

def check(name, condition, detail=""):
    status = "OK" if condition else "FAIL"
    CHECKS.append((name, condition))
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))


def main():
    print("=== Validação Pré-Deploy — Praia Digital Academy ===\n")

    # 1. Branch principal
    try:
        os.chdir(REPO_ROOT)
        with os.popen("git rev-parse --abbrev-ref HEAD") as f:
            branch = f.read().strip()
        check("Branch principal", branch == "main", branch)
    except Exception as e:
        check("Branch principal", False, str(e))

    # 2. Sem alterações não commitadas
    try:
        os.chdir(REPO_ROOT)
        with os.popen("git status --porcelain") as f:
            dirty = f.read().strip()
        check("Sem alterações não commitadas", not dirty, dirty or "limpo")
    except Exception as e:
        check("Sem alterações não commitadas", False, str(e))

    # 3. Arquivos críticos existem
    critical = [
        "render.yaml",
        "academy/.env.example",
        "academy/main.py",
        "academy/requirements.txt",
        "academy/routers/payments.py",
        "academy/routers/automation_whatsapp.py",
        "academy/routers/monitoring.py",
        "academy/core/whatsapp_service.py",
        "academy/core/config.py",
        "docs/deploy-render.md",
        "docs/deploy-summary.md",
        "education/checkout.html",
        "scripts/check_academy_deploy.py",
    ]
    for f in critical:
        check(f"Arquivo crítico: {f}", (REPO_ROOT / f).exists())

    # 4. requirements.txt tem dependências essenciais
    req = (REPO_ROOT / "academy/requirements.txt").read_text(encoding="utf-8")
    check("requests em requirements.txt", "requests==" in req)
    check("fpdf em requirements.txt", "fpdf==" in req)

    # 5. .env.example tem variáveis de integração
    env_example = (REPO_ROOT / "academy/.env.example").read_text(encoding="utf-8")
    check("MERCADOPAGO_TOKEN em .env.example", "MERCADOPAGO_TOKEN" in env_example)
    check("WHATSAPP_API_URL em .env.example", "WHATSAPP_API_URL" in env_example)
    check("BASE_URL em .env.example", "BASE_URL" in env_example)

    # 6. render.yaml tem variáveis de ambiente
    render = (REPO_ROOT / "render.yaml").read_text(encoding="utf-8")
    check("render.yaml: DATABASE_URL", "DATABASE_URL" in render)
    check("render.yaml: MERCADOPAGO_TOKEN", "MERCADOPAGO_TOKEN" in render)
    check("render.yaml: WHATSAPP_API_URL", "WHATSAPP_API_URL" in render)
    check("render.yaml: ALLOWED_ORIGINS", "ALLOWED_ORIGINS" in render)

    # 7. Router de monitoring registrado no main.py
    main_py = (REPO_ROOT / "academy/main.py").read_text(encoding="utf-8")
    check("main.py: monitoring router", "monitoring" in main_py)

    # 8. Router de WhatsApp registrado no main.py
    check("main.py: automation_whatsapp router", "automation_whatsapp" in main_py)

    # 9. Router de payments registrado no main.py
    check("main.py: payments router", "payments" in main_py)

    # 10. Deploy docs existem
    check("docs/deploy-render.md existe", (REPO_ROOT / "docs/deploy-render.md").exists())
    check("docs/deploy-summary.md existe", (REPO_ROOT / "docs/deploy-summary.md").exists())

    # 11. Python import test
    os.chdir(REPO_ROOT)
    sys.path.insert(0, str(REPO_ROOT))
    try:
        from academy.core import config
        from academy.core import whatsapp_service
        from academy.routers import monitoring, payments, certificates, automation_whatsapp
        check("Imports Python OK", True)
    except Exception as e:
        check("Imports Python OK", False, str(e))

    # Resultado final
    print("\n=== Resultado ===")
    ok = sum(1 for _, c in CHECKS if c)
    total = len(CHECKS)
    print(f"Checks: {ok}/{total} passaram")

    if ok == total:
        print("\n✅ Tudo OK para deploy no Render.")
        print("1. Abra o Render e crie um Web Service apontando para este repositório")
        print("2. Configure as variáveis de ambiente conforme docs/deploy-summary.md")
        print("3. Execute: python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30")
        return 0
    else:
        print("\n❌ Existem problemas a corrigir antes do deploy.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
