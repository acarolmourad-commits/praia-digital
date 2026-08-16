#!/usr/bin/env python3
"""
Pós-D2 — aplicador automático de classificação e recomendação.
Entrada: docs/comercial/resultado_d2_2026-08-17.md
Saída: docs/comercial/pos_d2_rankeado_2026-08-17.md
Não altera leads; apenas gera classificação, score e recomendação.
"""
import re, csv
from pathlib import Path
from datetime import datetime

root = Path('C:/Users/Carolina/praia-digital')
RESULTADO = root / 'docs' / 'comercial' / 'resultado_d2_2026-08-17.md'
OUT = root / 'docs' / 'comercial' / f'pos_d2_rankeado_{datetime.now().strftime("%Y-%m-%d")}.md'
LEADS_SRC = root / 'docs' / 'comercial' / 'leads_sao_sebastiao_bertioga.csv'

DECISAO_REGRA = {
    'positiva': 'HANDOFF_HUMANO',
    'pediu preco': 'RESPONDENDO_PRECO',
    'pediu preço': 'RESPONDENDO_PRECO',
    'pediu agendamento': 'AGENDAMENTO_HUMANO',
    'negativa': 'ENCERRADO',
    'bloqueio': 'BLOQUEADO',
    'sem resposta': 'SEGUINDO_SEQUENCIA',
    'objeção': 'AGUARDANDO',
    'informação': 'AGUARDANDO',
}

NEXT_ACTION = {
    'HANDOFF_HUMANO': 'Contato humano imediato',
    'RESPONDENDO_PRECO': 'Responder preço aprovado',
    'AGENDAMENTO_HUMANO': 'Confirmar disponibilidade',
    'ENCERRADO': 'Parar follow-up',
    'BLOQUEADO': 'Parar follow-up',
    'SEGUINDO_SEQUENCIA': 'D5 em 20/08',
    'AGUARDANDO': 'Follow-up conforme objeção',
}


def parse_score(v):
    try:
        return float(v)
    except Exception:
        return 0.0


def classify(text: str):
    t = text.lower()
    for key, value in DECISAO_REGRA.items():
        if key in t:
            return value, NEXT_ACTION[value]
    return 'SEGUINDO_SEQUENCIA', NEXT_ACTION['SEGUINDO_SEQUENCIA']


def load_leads_map():
    if not LEADS_SRC.exists():
        return {}
    rows = {}
    with LEADS_SRC.open('r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            rows[row.get('lead_id', '')] = row
    return rows


def generate():
    if not RESULTADO.exists():
        print('Resultado D2 ainda não existe; sem dados para classificar.')
        return
    text = RESULTADO.read_text(encoding='utf-8')
    leads = load_leads_map()
    blocks = re.split(r'\n\s*---+\s*\n', text)
    results = []
    for block in blocks:
        lead_id = None
        m = re.search(r'lead[_\s]?id[:\s]+(\d+)', block, re.I)
        if m:
            lead_id = m.group(1)
        resposta = block.strip()[:120].replace('\n', ' ')
        decisao, proxima = classify(resposta)
        score = parse_score(leads.get(lead_id, {}).get('score', '')) if lead_id else 0.0
        if decisao == 'HANDOFF_HUMANO':
            score += 10
        elif decisao == 'RESPONDENDO_PRECO':
            score += 5
        elif decisao == 'ENCERRADO':
            score = 0
        score = min(score, 100)
        results.append({
            'lead_id': lead_id or '?',
            'decisao': decisao,
            'proxima': proxima,
            'score': score,
            'resumo': resposta,
        })

    results.sort(key=lambda x: x['score'], reverse=True)
    today = datetime.now().strftime('%Y-%m-%d')
    out = OUT
    lines = [f'# Pós-D2 classificado — {today}\n', 'Resultado automático: resultado D2 → classificação → score → próxima ação → recomendação D5\n']
    for r in results:
        d5 = 'Sim — executar em 20/08' if r['decisao'] == 'SEGUINDO_SEQUENCIA' else 'Não necessário'
        lines.append(f"- lead {r['lead_id']} | {r['decisao']} | score={r['score']} | próxima={r['proxima']} | D5={d5}")
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Pós-D2 classificado gerado em {out}')
    return str(out)


if __name__ == '__main__':
    generate()
