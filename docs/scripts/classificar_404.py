#!/usr/bin/env python3
"""
Classificador de 404s e gerador de plano de reparo — Praia Digital
Entrada: docs/comercial/auditoria_404_2026-08-18.csv
Saída: docs/comercial/plano_reparo_404_2026-08-18.csv
"""
import csv, re
from pathlib import Path
from collections import Counter, defaultdict

BASE = Path(__file__).resolve().parent.parent.parent
AUDIT_PATH = BASE / 'docs' / 'comercial' / 'auditoria_404_2026-08-18.csv'
PLAN_PATH = BASE / 'docs' / 'comercial' / 'plano_reparo_404_2026-08-18.csv'
BLOG_DIR = BASE / 'blog'
OUTREACH_DIR = BASE / 'outreach'
PROP_DIR = BASE / 'proprietarios'
SERVICES_DIR = BASE / 'servicos'

CATEGORIES = ['REPARAR_LINK', 'REDIRECT', 'RECRIAR', 'REMOVER_REFERENCIA', 'MANTER_404']
PRIORITY_ORDER = {
    'REPARAR_LINK': 1,
    'REDIRECT': 2,
    'RECRIAR': 3,
    'REMOVER_REFERENCIA': 4,
    'MANTER_404': 5,
}


def classify(url: str, status: str) -> str:
    u = url.lower()
    s = status.lower()

    # DNS errors — outside our direct control
    if 'name resolution error' in s or 'max retries exceeded' in s:
        return 'MANTER_404'

    # /rss.xml — likely intentionally removed
    if '/rss.xml' in u:
        return 'REMOVER_REFERENCIA'

    # /servicos/ URLs
    if '/servicos/' in u:
        # Check if there's a likely replacement
        if 'consultoria' in u:
            return 'REMOVER_REFERENCIA'
        if 'gestao-de-imovel' in u or 'gestao-imovel' in u:
            return 'REMOVER_REFERENCIA'
        return 'MANTER_404'

    # /proprietarios/ URLs
    if '/proprietarios/' in u:
        return 'REMOVER_REFERENCIA'

    # /outreach/ URLs
    if '/outreach/' in u:
        # These files exist locally in outreach/ directory
        path_part = url.split('praia.digital/outreach/')[-1]
        local_file = OUTREACH_DIR / path_part
        if local_file.exists():
            return 'REPARAR_LINK'
        # Check for common alternatives
        if 'convite-parcerias' in u:
            return 'REPARAR_LINK'
        if 'lote-prospeccao' in u or 'template-followup' in u:
            return 'REMOVER_REFERENCIA'
        return 'MANTER_404'

    # /blog/ URLs — exist locally but 404 in deploy
    if '/blog/' in u:
        path_part = url.split('praia.digital/blog/')[-1]
        local_file = BLOG_DIR / path_part
        if local_file.exists():
            return 'REPARAR_LINK'
        return 'MANTER_404'

    # academy DNS
    if 'academy.praia.digital' in u:
        return 'MANTER_404'

    # www DNS
    if 'www.praia.digital' in u:
        return 'MANTER_404'

    return 'MANTER_404'


def find_local_equivalent(url: str) -> str:
    u = url.lower()
    if '/outreach/' in u:
        path_part = url.split('praia.digital/outreach/')[-1]
        local = OUTREACH_DIR / path_part
        if local.exists():
            return f'/{local.relative_to(BASE).as_posix()}'
    if '/blog/' in u:
        path_part = url.split('praia.digital/blog/')[-1]
        local = BLOG_DIR / path_part
        if local.exists():
            return f'/{local.relative_to(BASE).as_posix()}'
    return ''


def main():
    rows = []
    if not AUDIT_PATH.exists():
        print(f'Arquivo não encontrado: {AUDIT_PATH}')
        return

    with AUDIT_PATH.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    classified = []
    for r in rows:
        url = r['url']
        status = r['status']
        categoria = classify(url, status)
        local_eq = find_local_equivalent(url)
        classified.append({
            'url': url,
            'status': status,
            'categoria': categoria,
            'prioridade': PRIORITY_ORDER.get(categoria, 99),
            'substituta_local': local_eq,
        })

    # Sort by priority then URL
    classified.sort(key=lambda x: (x['prioridade'], x['url']))

    # Stats
    stats = Counter(c['categoria'] for c in classified)
    print('=== Classificação ===')
    for cat in sorted(CATEGORIES, key=lambda x: PRIORITY_ORDER.get(x, 99)):
        print(f'{cat}: {stats.get(cat, 0)}')
    print(f'Total: {len(classified)}')

    # Write plan
    fieldnames = ['url', 'status', 'categoria', 'prioridade', 'substituta_local']
    with PLAN_PATH.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(classified)

    print(f'\nPlano gerado: {PLAN_PATH}')
    print('\nTop 20 REPARAR_LINK:')
    reparar = [c for c in classified if c['categoria'] == 'REPARAR_LINK']
    for c in reparar[:20]:
        print(f"  {c['url']}")
        if c['substituta_local']:
            print(f"    -> {c['substituta_local']}")
    print('\nTop 10 REMOVER_REFERENCIA:')
    remover = [c for c in classified if c['categoria'] == 'REMOVER_REFERENCIA']
    for c in remover[:10]:
        print(f"  {c['url']}")


if __name__ == '__main__':
    main()
