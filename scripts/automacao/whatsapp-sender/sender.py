"""Script de envio de mensagens WhatsApp com templates por perfil/cidade.

Uso:
  python sender.py --csv contacts.csv --perfis-dir templates --dry-run
  python sender.py --csv contacts.csv --perfis-dir templates --envio-real

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
from pathlib import Path

TEMPLATE_DIR = Path(__file__).with_name('templates')


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
    return text


def enviar_whatsapp(numero: str, mensagem: str, api_url: str, api_token: str) -> dict:
    """Placeholder de integração real com API WhatsApp.

    Aqui você deve adaptar para a sua operadora/API (Evolution, Z-API, etc.).
    O retorno deve indicar sucesso/falha e o ID da mensagem enviada.
    """
    payload = {
        "numero": numero,
        "mensagem": mensagem,
    }
    # Exemplo genérico — adaptar conforme a API utilizada
    # response = requests.post(f"{api_url}/send-text", json=payload, headers={"Authorization": f"Bearer {api_token}"})
    # response.raise_for_status()
    # return response.json()
    return {"ok": True, "numero": numero}


def processar(csv_path: str, perfis_dir: Path, dry_run: bool, delay: int, api_url: str, api_token: str):
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
                print(f"[{idx}/{total}] Enviando para {row.get('telefone')}...")
                try:
                    resp = enviar_whatsapp(row.get('telefone', ''), mensagem, api_url, api_token)
                    if resp.get('ok'):
                        sucesso += 1
                    else:
                        falha += 1
                except Exception as e:
                    print(f"Erro: {e}")
                    falha += 1

                if idx < total:
                    time.sleep(delay)

        print(f"\nResumo: {sucesso} ok, {falha} falha(s).")


def main():
    parser = argparse.ArgumentParser(description="Envio de mensagens WhatsApp com templates")
    parser.add_argument('--csv', required=True, help='Caminho do CSV de contatos')
    parser.add_argument('--perfis-dir', default=str(TEMPLATE_DIR), help='Pasta com templates .md')
    parser.add_argument('--dry-run', action='store_true', help='Simula sem enviar')
    parser.add_argument('--delay', type=int, default=5, help='Segundos entre envios')
    parser.add_argument('--api-url', default=os.getenv('WHATSAPP_API_URL', ''), help='URL base da API WhatsApp')
    parser.add_argument('--api-token', default=os.getenv('WHATSAPP_API_TOKEN', ''), help='Token da API WhatsApp')
    args = parser.parse_args()

    if not args.dry_run and (not args.api_url or not args.api_token):
        print('Em modo de envio real, informe --api-url e --api-token ou defina WHATSAPP_API_URL e WHATSAPP_API_TOKEN.')
        sys.exit(1)

    processar(args.csv, Path(args.perfis_dir), args.dry_run, args.delay, args.api_url, args.api_token)


if __name__ == '__main__':
    main()
