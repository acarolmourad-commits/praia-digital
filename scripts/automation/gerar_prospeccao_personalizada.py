#!/usr/bin/env python3
"""
gerar_prospeccao_personalizada.py
Gera páginas de prospecção personalizadas a partir do CSV de leads.
Uso: python scripts/automation/gerar_prospeccao_personalizada.py --limit 50
"""

import csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
LEADS_CSV = BASE / "docs/sales/leads-litoral-enriquecido.csv"
OUTREACH_DIR = BASE / "outreach"


def load_leads(path):
    leads = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    return leads


def safe(text):
    return (text or "").replace('"', "").replace("'", "").strip()


def generate(limit=50):
    leads = load_leads(LEADS_CSV)[:limit]
    for r in leads:
        lead_id = r.get("id")
        nome = safe(r.get("nome_da_imobiliaria", "Parceiro"))
        cidade = safe(r.get("cidade", "litoral"))
        contato = safe(r.get("pessoa_de_contato", ""))
        cargo = safe(r.get("cargo", ""))
        dor = safe(r.get("dor_principal", ""))
        dif = safe(r.get("diferencial", ""))
        email = safe(r.get("email", ""))
        status = safe(r.get("status", ""))
        path = OUTREACH_DIR / f"prospeccao-lead-{lead_id}-{cidade.lower().replace(' ','-')}.html"
        if path.exists():
            continue
        path.write_text(f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prospeccao personalizada — {nome} ({cidade})</title>
<style>
:root{{primary:#2563eb;bg:#fafafa;card:#fff;border:#e5e7eb;text:#0f172a;muted:#475569}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font:14px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--text);padding:18px}}
.wrap{{max-width:960px;margin:0 auto}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:18px;margin:14px 0}}
a{{color:var(--primary);text-decoration:none}}
pre{{background:#f1f5f9;border:1px solid #e5e7eb;border-radius:12px;padding:14px;overflow:auto}}
</style>
</head>
<body>
<div class="wrap">
<div class="card">
<span style="background:#eff6ff;color:#1e3a8a;border:1px solid #bfdbfe;padding:4px 8px;border-radius:999px;font-size:12px;display:inline-block;margin-bottom:8px">{status}</span>
<h1>Prospeccao personalizada — {nome} ({cidade})</h1>
<p><strong>Contato:</strong> {contato} • {cargo} • {email}</p>
<h3>Dor principal</h3>
<pre>{dor}</pre>
<h3>Diferencial atual</h3>
<pre>{dif}</pre>
<h3>E-mail sugerido</h3>
<pre>Olá {contato}, identifiquei que a {nome} tem como foco {dor}. A Praia Digital pode apoiar com {dif} sem custo inicial. Quer testar em 1 imóvel?</pre>
<p><a href="mailto:{email}?subject=Proposta%20personalizada%20para%20{nome}&body=Ol%C3%A1%20{contato}%2C%20quero%20conversar%20sobre%20{dor}%20na%20{nome}.">Responder</a></p>
</div>
</div>
</body>
</html>""", encoding="utf-8")
    print(f"Geradas {len(leads)} páginas personalizadas.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    generate(limit=args.limit)
