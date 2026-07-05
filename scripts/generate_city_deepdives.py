#!/usr/bin/env python3
"""Gerador de Deep Dive por cidade para prospecção B2B."""
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r'C:\Users\Carolina\praia-digital')
LEADS_CSV = BASE / 'docs/sales/leads-litoral-enriquecido.csv'
OUT_DIR = BASE / 'docs/sales/deepdive-por-cidade'
OUT_DIR.mkdir(parents=True, exist_ok=True)

CITIES = ["Praia Grande","Santos","Guarujá","São Vicente","Peruíbe","Bertioga","Mongaguá","Itanhaém"]

def generate():
    with open(LEADS_CSV, 'r', encoding='utf-8') as f:
        leads = list(csv.DictReader(f))
    by_city = {}
    for lead in leads:
        city = lead.get('cidade_ref', lead.get('cidade', ''))
        by_city.setdefault(city, []).append(lead)
    for city in CITIES:
        city_leads = by_city.get(city, [])
        if not city_leads:
            continue
        top = sorted(city_leads, key=lambda x: int(x.get('_score', '0')), reverse=True)[:5]
        lines = []
        lines.append(f"# Deep Dive — {city}")
        lines.append(f"Data: {datetime.now().strftime('%Y-%m-%d')}\n")
        lines.append("## Visão geral")
        lines.append(f"- Leads na base: {len(city_leads)}")
        lines.append(f"- Top 5 por score: {top[0].get('_score','?')} → {top[-1].get('_score','?')}")
        lines.append(f"- Perfis comuns: {', '.join(sorted({l.get('perfil','') for l in top[:5]})).strip()}")
        lines.append(f"- Dores comuns: {', '.join(sorted({l.get('dor_principal','') for l in top[:5]})).strip()}")
        lines.append(f"- Diferenciais快速: {', '.join(sorted({l.get('diferencial','') for l in top[:5]})).strip()}")
        lines.append("\n## Oportunidades")
        lines.append("1) SEO local por bairro")
        lines.append("2) Follow-up automático por WhatsApp")
        lines.append("3) Automação de temporada")
        lines.append("\n## Próximos passos")
        lines.append("- Confirmar call de 30min")
        lines.append("- Apresentar plano 7-14 dias")
        lines.append("- Estabelecer modelo receita compartilhada")
        lines.append("\n## Contato")
        lines.append("Carolina Mourad")
        lines.append("CEO — Praia Digital")
        lines.append("(11) 95434-6288")
        lines.append("comercial@praia.digital")
        lines.append("https://praia.digital")
        (OUT_DIR / f'deepdive-{city.lower().replace(" ","-")}.md').write_text('\n'.join(lines), encoding='utf-8')
        print(f'CREATED deepdive/{city.lower().replace(" ","-")}.md')

if __name__ == '__main__':
    generate()
