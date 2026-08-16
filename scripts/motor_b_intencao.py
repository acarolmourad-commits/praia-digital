#!/usr/bin/env python3
"""
Motor de intenção comercial — Motor B
Classifica eventos locais em: VISITA → INTERAÇÃO → INTERESSE → INTENÇÃO → LEAD → CONVERSÃO
Saída: docs/comercial/motor_b_intencao_<data>.md
"""
import json, re
from pathlib import Path
from datetime import datetime

root = Path('C:/Users/Carolina/praia-digital')
OUT_DIR = root / 'docs' / 'comercial'

LEVELS = ['VISITA', 'INTERAÇÃO', 'INTERESSE', 'INTENÇÃO', 'LEAD', 'CONVERSÃO']

LEVEL_RULES = {
    'page_view': 'VISITA',
    'custom_click': 'INTERAÇÃO',
    'whatsapp_click': 'INTENÇÃO',
    'form_submit': 'LEAD',
}

CONVERSION_RULES = {
    'agendamento': 'CONVERSÃO',
    'venda': 'CONVERSÃO',
    'contrato': 'CONVERSÃO',
    'assinatura': 'CONVERSÃO',
}


def classify_event(event: dict):
    kind = event.get('event', '')
    level = LEVEL_RULES.get(kind)
    if not level:
        return None
    data = event.get('data', {}) or {}
    text = json.dumps(data, ensure_ascii=False).lower()
    if any(k in text for k in CONVERSION_RULES):
        level = 'CONVERSÃO'
    return {'event': kind, 'level': level, 'page': event.get('page'), 'data': data}


def generate_report(events_by_lead: dict):
    today = datetime.now().strftime('%Y-%m-%d')
    out_path = OUT_DIR / f'motor_b_intencao_{today}.md'
    lines = [
        f'# Motor B — Intenção comercial — {today}\n',
        'Classificação: VISITA → INTERAÇÃO → INTERESSE → INTENÇÃO → LEAD → CONVERSÃO\n'
    ]
    for lead_id, events in events_by_lead.items():
        classified = [classify_event(e) for e in events]
        classified = [c for c in classified if c]
        if not classified:
            continue
        best = sorted(classified, key=lambda c: LEVELS.index(c['level']), reverse=True)[0]
        lines.append(f'- Lead {lead_id}: melhor nível = {best["level"]} | último evento = {best["event"]} | página = {best.get("page")}')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    return str(out_path)


if __name__ == '__main__':
    # Placeholder: alimentado por dados reais após D2 ou via script de leitura do localStorage
    generate_report({})
