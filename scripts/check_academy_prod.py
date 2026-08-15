"""Health check rápido para a Academy em produção."""
import requests, sys

URLS = [
    "https://academy.praia.digital/health",
    "https://academy.praia.digital/courses",
    "https://academy.praia.digital/academy/payments/webhook",
]

for url in URLS:
    try:
        r = requests.get(url, timeout=20)
        print(f"{url} => {r.status_code}")
        if r.status_code >= 500:
            print("  FALHA:", r.text[:200])
            sys.exit(1)
    except Exception as e:
        print(f"{url} => ERRO: {e}")
        sys.exit(1)

print("OK")
