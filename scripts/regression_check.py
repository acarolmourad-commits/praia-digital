#!/usr/bin/env python3
"""Regressão estrutural da Academy: compara estado atual com baseline."""
import json, sys
from pathlib import Path

BASE = Path(r'C:\Users\Carolina\praia-digital')
INVENTORY = BASE / 'docs/academy/inventory-64-cursos.json'
BASELINE = BASE / 'docs/academy/regression-baseline.json'

REQUIRED_SLUGS = [
    'airbnb-do-zero',
    'booking-do-zero',
    'venda-rapida-imoveis-litoral',
    'crm-para-corretores',
    'automacao-comercial',
    'financiamento-imobiliario',
]


def load_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f'failed to load {path}: {e}')
        sys.exit(2)


def main():
    inventory = load_json(INVENTORY)
    items = inventory if isinstance(inventory, list) else inventory.get('items', [])
    slugs = [i['slug'] for i in items if 'slug' in i]
    prontos = [i['slug'] for i in items if i.get('status_final') == 'PRONTO_PARA_VENDA']
    has_index = [i['slug'] for i in items if i.get('has_index')]
    has_vendas = [i['slug'] for i in items if i.get('has_vendas')]

    failures = []
    if len(slugs) != 64:
        failures.append(f'slug count changed: {len(slugs)}')
    if len(prontos) != 64:
        failures.append(f'prontos count changed: {len(prontos)}')
    for slug in REQUIRED_SLUGS:
        if slug not in slugs:
            failures.append(f'required slug missing: {slug}')
        if slug not in has_index:
            failures.append(f'required slug missing index.html: {slug}')
        if slug not in has_vendas:
            failures.append(f'required slug missing vendas.html: {slug}')

    # Update baseline if missing
    if not BASELINE.exists():
        BASELINE.write_text(
            json.dumps({
                'slug_count': len(slugs),
                'prontos_count': len(prontos),
                'required_slugs': REQUIRED_SLUGS,
                'has_index': has_index,
                'has_vendas': has_vendas,
            }, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        print('baseline created')

    baseline = load_json(BASELINE)
    if baseline.get('slug_count') != len(slugs):
        failures.append('slug count regression from baseline')
    if baseline.get('prontos_count') != len(prontos):
        failures.append('prontos count regression from baseline')
    for slug in REQUIRED_SLUGS:
        if slug not in baseline.get('has_index', []):
            failures.append(f'baseline missing index for {slug}')
        if slug not in baseline.get('has_vendas', []):
            failures.append(f'baseline missing vendas for {slug}')

    if failures:
        print('REGRESSION FAILURES:')
        for f in failures:
            print(f' - {f}')
        sys.exit(1)

    print(f'regression ok: {len(slugs)} slugs, {len(prontos)} prontos')
    sys.exit(0)


if __name__ == '__main__':
    main()
