"""notificar.py — notificacao unica via Telegram (substitui notificar_*.py e notificar_vendas_b2b.py).

Configurar variaveis de ambiente (uma unica vez):
    setx TELEGRAM_TOKEN "123456:ABC..."
    setx TELEGRAM_CHAT_ID "123456789"

Uso:
    python scripts/pipeline/notificar.py --mensagem "Vendas B2B prontas: 8 leads"
"""
import argparse, json, os, urllib.request

def notificar(mensagem: str) -> bool:
    token, chat_id = os.environ.get("TELEGRAM_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Telegram nao configurado; seguindo apenas com log local.")
        print(mensagem)
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": mensagem}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=15)
        print("Notificacao enviada ao Telegram.")
        return True
    except Exception as e:
        print(f"Falha ao notificar Telegram: {e}")
        return False

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--mensagem", required=True)
    a = p.parse_args()
    notificar(a.mensagem)
