"""Script de envio de mensagens WhatsApp com templates por perfil/cidade.

Uso:
  python sender.py --csv contacts.csv --perfis-dir templates --dry-run
  python sender.py --csv contacts.csv --perfis-dir templates --envio-real

Variáveis de ambiente (.env):
  WHATSAPP_API_URL  — URL base da API (ex: https://evolution-api.exemplo.com)
  WHATSAPP_API_TOKEN — Token de autenticação
  WHATSAPP_INSTANCE — Nome da instância/instance (Evolution API)

Segurança:
  --dry-run: apenas simula no console, sem chamar API
  --delay: segundos entre envios (default 5)
"""

import argparse
import csv
import time
import re
import os
import sys
import json
from pathlib import Path
from urllib.parse import quote

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

TEMPLATE_DIR = Path(__file__).with_name('templates')


def load_env():
    """Carrega variáveis de ambiente do .env se disponível."""
    if load_dotenv:
        env_path = Path(__file__).parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
        else:
            load_dotenv()
    return {
        'api_url': os.getenv('WHATSAPP_API_URL', '').rstrip('/'),
        'api_token': os.getenv('WHATSAPP_API_TOKEN', ''),
        'instance': os.getenv('WHATSAPP_INSTANCE', ''),
    }


def load_template(perfil: str) -> str:
    path = TEMPLATE_DIR / f"{perfil}.md"
    if not path.exists():
        raise FileNotFoundError(f"Template não encontrado: {path}")
    return path.read_text(encoding='utf-8')


def render(template: str, row: dict) -> str:
    text = template
    text = re.sub(r"\{\{nome\}\}", row.get('nome', ''), text)
    text = re.sub(r"\{\{cidade\}\}", row.get('cidade', ''), text)
    text = re.sub(r"\{\{data\}\}", row.get('data', ''), text)
    text = re.sub(r"\{\{metrica\}\}", row.get('metrica', 'até 40%'), text)
    text = re.sub(r"\{\{link_guia\}\}", row.get('link_guia', ''), text)
    text = re.sub(r"\{\{link_calculadora\}\}", row.get('link_calculadora', ''), text)
    text = re.sub(r"\{\{cidade_slug\}\}", row.get('cidade_slug', ''), text)
    return text


def enviar_evolution(api_url: str, api_token: str, instance: str, numero: str, mensagem: str) -> dict:
    """Envio via Evolution API (padrão REST /message/sendText)."""
    try:
        import requests
    except ImportError:
        return {"ok": False, "erro": "requests não instalado"}

    numero_clean = re.sub(r"[^\d]", "", numero)
    if not numero_clean.startswith("55"):
        return {"ok": False, "erro": "Número inválido (use formato 5511999999999)"}

    url = f"{api_url}/message/sendText/{quote(instance, safe='')}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }
    payload = {
        "number": numero_clean,
        "text": mensagem,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        return {"ok": True, "id": data.get("key", {}).get("id"), "numero": numero_clean}
    except Exception as e:
        return {"ok": False, "erro": str(e), "numero": numero_clean}


def enviar_zapi(api_url: str, api_token: str, numero: str, mensagem: str) -> dict:
    """Envio via Z-API (padrão /send-text)."""
    try:
        import requests
    except ImportError:
        return {"ok": False, "erro": "requests não instalado"}

    numero_clean = re.sub(r"[^\d]", "", numero)
    if not numero_clean.startswith("55"):
        return {"ok": False, "erro": "Número inválido (use formato 5511999999999)"}

    url = f"{api_url}/send-text"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }
    payload = {
        "phone": numero_clean,
        "message": mensagem,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        return {"ok": True, "id": data.get("id") or data.get("messageId"), "numero": numero_clean}
    except Exception as e:
        return {"ok": False, "erro": str(e), "numero": numero_clean}


def enviar_whatsapp(numero: str, mensagem: str, api_url: str, api_token: str, provider: str, instance: str) -> dict:
    """Dispatch para o provider selecionado."""
    if provider == 'evolution':
        return enviar_evolution(api_url, api_token, instance, numero, mensagem)
    if provider == 'zapi':
        return enviar_zapi(api_url, api_token, numero, mensagem)
    return {"ok": False, "erro": f"Provider '{provider}' não suportado"}


def processar(csv_path: str, perfis_dir: Path, dry_run: bool, delay: int, env: dict, provider: str):
    api_url = env.get('api_url', '')
    api_token = env.get('api_token', '')
    instance = env.get('instance', '')

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            print("CSV vazio.")
            return

        total = len(rows)
        sucesso = 0
        falha = 0

        for idx, row in enumerate(rows, start=1):
            perfil = row.get('perfil')
            if not perfil:
                print(f"[{idx}/{total}] ❌ Perfil ausente na linha")
                falha += 1
                continue

            try:
                template = load_template(perfil)
            except FileNotFoundError as e:
                print(f"[{idx}/{total}] ❌ {e}")
                falha += 1
                continue

            mensagem = render(template, row)

            if dry_run:
                print(f"\n[{idx}/{total}] 🧪 DRY RUN — {row.get('nome')} / {row.get('cidade')} / {perfil}")
                print(f"Para: {row.get('telefone')}")
                print(mensagem)
                sucesso += 1
            else:
                if not api_url or not api_token:
                    print("❌ API_URL e API_TOKEN são obrigatórios fora do dry-run.")
                    sys.exit(1)

                print(f"[{idx}/{total}] Enviando para {row.get('telefone')}...")
                resp = enviar_whatsapp(row.get('telefone', ''), mensagem, api_url, api_token, provider, instance)
                if resp.get('ok'):
                    sucesso += 1
                else:
                    falha += 1
                    print(f"❌ Erro: {resp.get('erro')}")

                if idx < total:
                    time.sleep(delay)

        print(f"\nResumo: {sucesso} ok, {falha} falha(s).")


def main():
    parser = argparse.ArgumentParser(description="Envio de mensagens WhatsApp com templates")
    parser.add_argument('--csv', required=True, help='Caminho do CSV de contatos')
    parser.add_argument('--perfis-dir', default=str(TEMPLATE_DIR), help='Pasta com templates .md')
    parser.add_argument('--dry-run', action='store_true', help='Simula sem enviar')
    parser.add_argument('--delay', type=int, default=5, help='Segundos entre envios')
    parser.add_argument('--provider', choices=['evolution', 'zapi'], default='evolution', help='Provider WhatsApp')
    args = parser.parse_args()

    env = load_env()
    processar(args.csv, Path(args.perfis_dir), args.dry_run, args.delay, env, args.provider)


if __name__ == '__main__':
    main()
