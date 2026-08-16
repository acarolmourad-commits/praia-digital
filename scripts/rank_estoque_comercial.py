#!/usr/bin/env python3
"""
Recalcula a fila comercial ranqueada a partir dos estoques disponíveis.
Uso: python scripts/rank_estoque_comercial.py
"""
import csv
from pathlib import Path
from datetime import datetime

root = Path('C:/Users/Carolina/praia-digital')
OUT_DIR = root / 'docs' / 'comercial'
MOTOR_A = OUT_DIR / 'motor_a_novo_estoque_2026-08-16.csv'
MOTOR_B = root / 'docs' / 'comercial' / 'leads_sao_sebastiao_bertioga.csv'

SERVICE_ADJUST = {
    'administração airbnb': 6,
    'administracao airbnb': 6,
    'administração temporada': 5,
    'administracao temporada': 5,
    'edição de anúncio': 3,
    'edicao de anuncio': 3,
    'fotografia': 4,
    'seo local': 4,
}


def score_lead(score_raw: str, tipo: str, servico: str):
    try:
        base = float(score_raw)
    except Exception:
        base = 0.0
    tipo_lower = (tipo or '').lower()
    if any(x in tipo_lower for x in ['proprietário', 'proprietario', 'anfitriao', 'anfitrião']):
        base += 5
    elif 'imobiliaria' in tipo_lower:
        base += 0
    else:
        base += 2
    for key, adj in SERVICE_ADJUST.items():
        if key in (servico or '').lower():
            base += adj
            break
    return min(base, 100)


def build_queue():
    rows = []
    for src in [MOTOR_A, MOTOR_B]:
        if not src.exists():
            continue
        with src.open('r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                rows.append({
                    'lead_id': row.get('lead_id', ''),
                    'score_ajustado': score_lead(row.get('score', ''), row.get('tipo_cliente', ''), row.get('servico_potencial', '')),
                    'score_bruto': row.get('score', ''),
                    'nome': row.get('nome_empresa', ''),
                    'cidade': row.get('city', ''),
                    'tipo': row.get('tipo_cliente', ''),
                    'servico': row.get('servico_potencial', ''),
                    'status': row.get('status', ''),
                })
    rows.sort(key=lambda x: x['score_ajustado'], reverse=True)
    today = datetime.now().strftime('%Y-%m-%d')
    out = OUT_DIR / f'fila_comercial_rankeada_{today}.md'
    lines = [f'# Fila comercial ranqueada — {today}\n', 'Ranked por score ajustado (score + ajuste por tipo/serviço).\n']
    for i, r in enumerate(rows, 1):
        lines.append(f"{i}. {r['lead_id']} | {r['nome']} | {r['cidade']} | {r['servico']} | score={r['score_ajustado']}")
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Fila gerada: {out} ({len(rows)} leads)')
    return str(out)


if __name__ == '__main__':
    build_queue()
