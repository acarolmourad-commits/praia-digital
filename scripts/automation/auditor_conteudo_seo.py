#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditor contínuo de conteúdo SEO para Praia Digital.
- Lista temas já publicados (blog, páginas, imóveis).
- Sugere próximos temas inéditos com base em gaps e sazonalidade.
- Gera relatório HTML simples.
"""

import os
import re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BLOG_DIR = os.path.join(ROOT, 'blog')
OUTPUT_PATH = os.path.join(ROOT, 'docs/materiais/relatorio-auditoria-seo-praia-digital.html')

KEYWORDS_CORE = [
    'IA', 'inteligência artificial', 'automação', 'WhatsApp', 'check-in', 'follow-up',
    'avaliação', 'preço', 'anúncio', 'SEO', 'Google', 'LGPD', 'temporada', 'verão',
    'outubro', 'novembro', 'dezembro', 'aluguel', 'venda', 'imóvel', 'imóveis',
    'corretor', 'imobiliária', 'litoral', 'praia', 'condomínio', 'financiamento'
]

SUGGESTIONS = [
    'Captação de imóveis em baixa temporada no litoral',
    'Como estruturar um funil de vendas para imobiliárias de pequeno porte',
    'Automação de WhatsApp para redução de faltas em visitas',
    'Modelo de avaliação automática de preço para apartamentos com vista',
    'Geração de descrições de anúncios com IA sem perder personalidade',
    'SEO local para condomínios: como aparecer primeiro no Google',
    'Checklist de LGPD para corretores no atendimento digital',
    'Estratégia de indicações no pós-venda para imóveis de temporada',
    'Gestão de carteira de imóveis com alertas inteligentes',
    'Diferença entre captação orgânica e anúncios pagos para imobiliárias'
]


def list_existing_titles():
    titles = set()
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith('.html'):
            path = os.path.join(BLOG_DIR, filename)
            text = open(path, 'r', encoding='utf-8').read()
            m = re.search(r'<title>(.*?)</title>', text, re.IGNORECASE)
            if m:
                titles.add(m.group(1).strip().lower())
            h1 = re.search(r'<h1>(.*?)</h1>', text, re.IGNORECASE)
            if h1:
                titles.add(h1.group(1).strip().lower())
    return titles


def detect_gaps(existing):
    gaps = []
    existing_lower = {t.lower() for t in existing}
    for s in SUGGESTIONS:
        if s.lower() not in existing_lower:
            gaps.append(s)
    return gaps


def build_report(existing, gaps):
    today = datetime.now().strftime('%d/%m/%Y %H:%M')
    lines = [
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Relatório Auditoria SEO</title>',
        '<style>body{font-family:sans-serif;background:#f6f8fb;color:#222;margin:0;padding:20px}',
        '.card{background:#fff;border-radius:10px;padding:20px;margin-bottom:20px;box-shadow:0 2px 6px rgba(0,0,0,.08)}',
        'h1{font-size:22px;margin:0 0 12px}h2{font-size:16px;margin:18px 0 8px}ul{padding-left:18px}li{margin:4px 0}</style></head><body>',
        f'<div class="card"><h1>Relatório de Auditoria SEO — Praia Digital</h1><p>Gerado em {today}</p>',
        f'<p>Títulos detectados em blog: <strong>{len(existing)}</strong></p>'
    ]

    lines.append('<h2>Temas já publicados (amostra)</h2><ul>')
    for t in sorted(existing)[:80]:
        lines.append(f'<li>{t}</li>')
    lines.append('</ul>')

    lines.append('<h2>Sugestões inéditas</h2><ul>')
    for g in gaps:
        lines.append(f'<li>{g}</li>')
    lines.append('</ul>')

    lines.append('</div></body></html>')
    return '\n'.join(lines)


def main():
    existing = list_existing_titles()
    gaps = detect_gaps(existing)
    report = build_report(existing, gaps)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f'Relatório gerado: {OUTPUT_PATH}')
    print(f'Temas existentes: {len(existing)} | Sugestões inéditas: {len(gaps)}')


if __name__ == '__main__':
    main()
