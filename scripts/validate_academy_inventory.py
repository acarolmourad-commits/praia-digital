#!/usr/bin/env python3
"""Valida inventário mínimo da Academy antes de deploy."""
import json, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
INVENTORY = BASE / 'docs/academy/inventory-64-cursos.json'


def main():
    if not INVENTORY.exists():
        print(f'inventory missing: {INVENTORY}')
        sys.exit(1)
    data = json.loads(INVENTORY.read_text(encoding='utf-8'))
    items = data if isinstance(data, list) else data.get('items', [])
    slugs = [i['slug'] for i in items if 'slug' in i]
    prontos = [i['slug'] for i in items if i.get('status_final') == 'PRONTO_PARA_VENDA']
    missing = [i['slug'] for i in items if not i.get('has_index')]
    missing_vendas = [i['slug'] for i in items if not i.get('has_vendas')]

    print(f'inventory: {len(slugs)} slugs, {len(prontos)} prontos')
    if len(slugs) != 64 or len(prontos) != 64:
        sys.exit(1)
    if missing or missing_vendas:
        print('missing files:', missing + missing_vendas)
        sys.exit(1)
    print('inventory validation passed')


if __name__ == '__main__':
    main()
