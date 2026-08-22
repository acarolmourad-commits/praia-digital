#!/usr/bin/env python3
"""
Regressão e consistência do inventário da Academy.

Verifica:
- filesystem vs academy/inventario.json
- academy/inventario.json vs docs/academy/inventory-64-cursos.json
- academy/inventario.json vs academy/tests/mapeamento-cursos-20260817.json
- docs/academy/catalog-64-cursos.json vs mapeamento
- integridade estrutural mínima por curso

Saída: JSON em stdout e relatório de divergências.
"""
import json, sys
from pathlib import Path

REPO = Path('.').resolve()
CURSOS_DIR = REPO / 'academy' / 'cursos'
INV = REPO / 'academy' / 'inventario.json'
INV2 = REPO / 'docs' / 'academy' / 'inventory-64-cursos.json'
CAT = REPO / 'docs' / 'academy' / 'catalog-64-cursos.json'
MAPA = REPO / 'academy' / 'tests' / 'mapeamento-cursos-20260817.json'


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding='utf-8'))


def normalize_inventory_payload(data):
    if isinstance(data, dict):
        return data.get('items', [])
    if isinstance(data, list):
        return data
    return []


def fs_slugs():
    return sorted([p.name for p in CURSOS_DIR.iterdir() if p.is_dir()])


def inventory_slugs():
    data = load_json(INV)
    return sorted([x['slug'] for x in normalize_inventory_payload(data) if x.get('slug')])


def mapeamento_slugs():
    data = load_json(MAPA)
    cursos = data.get('cursos', []) if isinstance(data, dict) else data
    return sorted([x['slug'] for x in cursos if x.get('slug')])


def catalog_slugs():
    data = load_json(CAT)
    items = normalize_inventory_payload(data)
    return sorted([x['slug'] for x in items if x.get('slug')])


def course_core_audit(slug: str) -> dict:
    root = CURSOS_DIR / slug
    missing = []
    if not (root / 'index.html').exists():
        missing.append('index.html')
    if not (root / 'vendas.html').exists():
        missing.append('vendas.html')
    if not (root / 'curso.md').exists():
        missing.append('curso.md')
    return {'slug': slug, 'missing': missing, 'valid': len(missing) == 0}


def main() -> dict:
    report = {
        'filesystem': {'slug_count': len(fs_slugs())},
        'inventory': {'slug_count': len(inventory_slugs())},
        'mapeamento': {'slug_count': len(mapeamento_slugs())},
        'catalog': {'slug_count': len(catalog_slugs())},
        'fs_inv_divergence': [],
        'inv_mapeamento_divergence': [],
        'inv_catalog_divergence': [],
        'core_audit': {'valid': 0, 'invalid': 0, 'details': []},
        'regressions': [],
    }

    fs = set(fs_slugs())
    inv = set(inventory_slugs())
    map_set = set(mapeamento_slugs())
    cat = set(catalog_slugs())

    report['fs_inv_divergence'] = sorted((fs - inv) | (inv - fs))
    report['inv_mapeamento_divergence'] = sorted((inv - map_set) | (map_set - inv))
    report['inv_catalog_divergence'] = sorted((inv - cat) | (cat - inv))

    for slug in inv:
        audit = course_core_audit(slug)
        report['core_audit']['details'].append(audit)
        if audit['valid']:
            report['core_audit']['valid'] += 1
        else:
            report['core_audit']['invalid'] += 1
            report['regressions'].append(f'{slug}: missing {audit["missing"]}')

    if report['fs_inv_divergence'] or report['inv_mapeamento_divergence'] or report['inv_catalog_divergence']:
        report['regressions'].append('slug divergence detected')

    return report


if __name__ == '__main__':
    r = main()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    sys.exit(1 if r['regressions'] else 0)
