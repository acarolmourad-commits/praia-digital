#!/usr/bin/env python3
"""
QA automático da Academy: impede curso de aparecer como pronto se faltar componente obrigatório.
Executa antes de deploy e pode ser chamado pelo CI/validação.
"""
import json, sys
from pathlib import Path

REPO = Path('.').resolve()
COURSES_DIR = REPO / 'academy' / 'cursos'
INVENTORY = REPO / 'docs' / 'academy' / 'inventory-64-cursos.json'

# Componentes obrigatórios por curso
REQUIRED_FILES = ['curso.md', 'README.md', 'index.html', 'vendas.html']
REQUIRED_DIRS = ['aulas', 'materiais', 'estudos-caso', 'certificado', 'checklists']


def audit_course(course_dir: Path) -> dict:
    issues = []
    missing_files = [f for f in REQUIRED_FILES if not (course_dir / f).exists()]
    missing_dirs = [d for d in REQUIRED_DIRS if not (course_dir / d).exists()]
    if missing_files:
        issues.append({'type': 'missing_file', 'items': missing_files})
    if missing_dirs:
        issues.append({'type': 'missing_dir', 'items': missing_dirs})
    # aulas must have content
    aulas_dir = course_dir / 'aulas'
    if not aulas_dir.exists():
        aulas_dir = course_dir / 'curso-completo'
    if aulas_dir.exists() and not list(aulas_dir.glob('*')):
        issues.append({'type': 'empty_dir', 'item': 'aulas'})
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'missing_files': missing_files,
        'missing_dirs': missing_dirs,
    }


def main() -> dict:
    inventory = json.loads(INVENTORY.read_text(encoding='utf-8'))
    items = inventory if isinstance(inventory, list) else inventory.get('items', [])
    slugs = [i['slug'] for i in items if i.get('status_final') == 'PRONTO_PARA_VENDA']
    results = []
    invalid = []
    for slug in slugs:
        course_dir = COURSES_DIR / slug
        if not course_dir.exists():
            invalid.append({'slug': slug, 'reason': 'course_dir_missing'})
            continue
        audit = audit_course(course_dir)
        results.append({'slug': slug, **audit})
        if not audit['valid']:
            invalid.append({'slug': slug, 'issues': audit['issues']})
    report = {
        'total': len(slugs),
        'audited': len(results),
        'valid': len([r for r in results if r['valid']]),
        'invalid': len(invalid),
        'details': results,
        'invalid_slugs': [i['slug'] for i in invalid],
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report


if __name__ == '__main__':
    result = main()
    sys.exit(0 if result['invalid'] == 0 else 1)
