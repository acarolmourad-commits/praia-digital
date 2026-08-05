#!/usr/bin/env python3
"""
Testa integração real do Mercado Pago.
Uso:
  python scripts/test_mercadopago.py
"""

import os
import sys
import requests

from academy.core.config import MERCADOPAGO_TOKEN, MERCADOPAGO_PUBLIC_KEY, BASE_URL, MERCADOPAGO_API as MERCADOPAGO_API_URL


def main():
    print("=== Teste Mercado Pago ===")
    if not MERCADOPAGO_TOKEN:
        print("[ERRO] MERCADOPAGO_TOKEN não definido no ambiente.")
        return 1

    print(f"API: {MERCADOPAGO_API_URL}")
    print(f"BASE_URL: {BASE_URL}")
    print(f"Token: {'*' * 8}...{MERCADOPAGO_TOKEN[-4:]}")

    headers = {"Authorization": f"Bearer {MERCADOPAGO_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "items": [
            {
                "title": "Teste Integração MP",
                "quantity": 1,
                "unit_price": 10,
                "currency_id": "BRL",
            }
        ],
        "payer": {
            "email": "teste@praia.digital",
            "first_name": "Teste",
            "identification": {"type": "CPF", "number": "00000000000"},
        },
        "back_urls": {
            "success": f"{BASE_URL}/education/checkout.html?status=approved",
            "failure": f"{BASE_URL}/education/checkout.html?status=rejected",
            "pending": f"{BASE_URL}/education/checkout.html?status=pending",
        },
        "auto_return": "approved",
        "external_reference": "TEST",
    }

    try:
        resp = requests.post(f"{MERCADOPAGO_API_URL}/checkout/preferences", json=payload, headers=headers, timeout=20)
        print(f"Status: {resp.status_code}")
        if resp.status_code in (200, 201):
            data = resp.json()
            print(f"init_point: {data.get('init_point')}")
            print(f"id: {data.get('id')}")
            print("✅ Integração OK")
            return 0
        print(resp.text)
        print("❌ Falha na integração")
        return 1
    except requests.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
