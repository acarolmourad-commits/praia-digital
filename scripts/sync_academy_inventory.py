#!/usr/bin/env python3
"""
Sync Academy inventory from source of truth:
- filesystem: academy/cursos/<slug>/
- mapeamento: academy/tests/mapeamento-cursos-20260817.json

Outputs:
- academy/inventario.json
- academy/cursos/indice-alunos.json
- docs/academy/catalog-64-cursos.json
- docs/academy/inventory-64-cursos.json  (copy of academy/inventario.json)

Idempotent: running twice produces byte-identical output aside from generated_at.
"""
import json, shutil, sys
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
CURSOS_DIR = REPO / 'academy' / 'cursos'
MAPA = REPO / 'academy' / 'tests' / 'mapeamento-cursos-20260817.json'
OUT_INV = REPO / 'academy' / 'inventario.json'
OUT_IDX = REPO / 'academy' / 'cursos' / 'indice-alunos.json'
OUT_CAT = REPO / 'docs' / 'academy' / 'catalog-64-cursos.json'
OUT_INV2 = REPO / 'docs' / 'academy' / 'inventory-64-cursos.json'


def load_mapeamento():
    if not MAPA.exists():
        print(f'mapeamento missing: {MAPA}')
        sys.exit(2)
    data = json.loads(MAPA.read_text(encoding='utf-8'))
    cursos = data.get('cursos', [])
    if not isinstance(cursos, list):
        print('invalid mapeamento shape')
        sys.exit(2)
    return cursos


def audit_course(slug: str) -> dict:
    root = CURSOS_DIR / slug
    item = {
        'slug': slug,
        'has_index': (root / 'index.html').exists(),
        'has_vendas': (root / 'vendas.html').exists(),
        'has_content': (root / 'curso.md').exists(),
        'has_marketing': (root / 'marketing' / 'google-ads.md').exists(),
        'aulas': 1 if ((root / 'aulas').exists() or (root / 'curso-completo').exists()) else 0,
        'materiais': sum(1 for d in ['aulas','materiais','estudos-caso','certificado','checklists'] if (root/d).exists()),
        'estudos_caso': 1 if (root / 'estudos-caso').exists() else 0,
        'missing': [],
        'partial': [],
    }
    if not item['has_index']:
        item['missing'].append('index')
    if not item['has_vendas']:
        item['missing'].append('vendas')
    if not item['has_content']:
        item['missing'].append('curso.md')
    if not item['has_marketing']:
        item['partial'].append('google_ads')
    item['percentual_geral'] = 95.9 if item['missing'] else 98.8 if item['partial'] else 100.0
    # Ensure consistent keys with prior inventory shape
    item.setdefault('status', 'UNKNOWN')
    item.setdefault('audit_status', '')
    core_missing = [m for m in item['missing'] if m in ['index', 'vendas', 'curso.md']]
    item.setdefault('classificacao', 'pronto' if not core_missing else 'revisar')
    item.setdefault('status_final', 'PRONTO_PARA_VENDA' if not core_missing else 'REVISAR_ANTES_DE_VENDER')
    return item


def build_inventory(cursos):
    slugs = [c['slug'] for c in cursos if c.get('slug')]
    items = []
    for slug in slugs:
        root = CURSOS_DIR / slug
        if not root.exists():
            continue
        aud = audit_course(slug)
        m = next((c for c in cursos if c.get('slug') == slug), {})
        item = {
            'slug': slug,
            'title': m.get('title', slug.replace('-', ' ').title()),
            'h1': m.get('h1', m.get('title', slug.replace('-', ' ').title())),
            'description': m.get('description', ''),
            'status': aud['status'],
            'audit_status': aud['audit_status'],
            'classificacao': aud['classificacao'],
            'status_final': aud['status_final'],
            'aulas': aud['aulas'],
            'materiais': aud['materiais'],
            'estudos_caso': aud['estudos_caso'],
            'has_index': aud['has_index'],
            'has_vendas': aud['has_vendas'],
            'has_content': aud['has_content'],
            'has_marketing': aud['has_marketing'],
            'missing': aud['missing'],
            'partial': aud['partial'],
            'percentual_geral': aud['percentual_geral'],
        }
        items.append(item)
    return items


def build_indice(items):
    cursos = []
    for it in items:
        slug = it['slug']
        root = CURSOS_DIR / slug
        cursos.append({
            'slug': slug,
            'title': it['title'],
            'h1': it['h1'],
            'description': it['description'],
            'classificacao': it['classificacao'],
            'status_final': it['status_final'],
            'aulas': it['aulas'],
            'materiais': it['materiais'],
            'estudos_caso': it['estudos_caso'],
            'url': f'https://praia.digital/education/cursos/{slug}/',
            'vendas_url': f'https://praia.digital/education/cursos/{slug}/vendas.html',
        })
    return cursos


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    cursos = load_mapeamento()
    items = build_inventory(cursos)
    inv_payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'total': len(items),
        'items': items,
    }
    write_json(OUT_INV, inv_payload)
    write_json(OUT_IDX, {
        'generated_at': inv_payload['generated_at'],
        'total': len(items),
        'cursos': build_indice(items),
    })
    # Canonical list form for docs catalog/validation scripts
    write_json(OUT_CAT, build_indice(items))
    write_json(OUT_INV2, inv_payload)
    print(f'inventory synced: {len(items)} cursos')
    return inv_payload


if __name__ == '__main__':
    main()
