#!/usr/bin/env python3
"""
Gera .env de produção a partir de .env.example para a Academy.
Uso:
  python scripts/generate_production_env.py
"""

import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ENV_EXAMPLE = BASE / "academy" / ".env.example"
ENV_PROD = BASE / "academy" / ".env.production.example"


def main():
    if not ENV_EXAMPLE.exists():
        print(f"Arquivo não encontrado: {ENV_EXAMPLE}")
        return 1

    content = ENV_EXAMPLE.read_text(encoding="utf-8")

    # Adiciona instruções e marcações de produção
    header = """# ===========================================
# Arquivo de ambiente de PRODUÇÃO — Academy
# Copie este arquivo para .env no servidor
# e preencha os valores reais.
# ===========================================

"""

    prod_content = header + content

    ENV_PROD.write_text(prod_content, encoding="utf-8")
    print(f"Arquivo gerado: {ENV_PROD}")
    print("Próximos passos:")
    print("1. Copie academy/.env.production.example para academy/.env no servidor")
    print("2. Preencha DATABASE_URL, SECRET_KEY, SMTP, MERCADOPAGO e WHATSAPP")
    print("3. Reinicie o Web Service no Render")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
