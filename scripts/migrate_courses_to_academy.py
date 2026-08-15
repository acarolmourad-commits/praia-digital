#!/usr/bin/env python3
"""
Migração segura de cursos de `education/cursos/<slug>/` para `academy/cursos/<slug>/`.
Mapeia estrutura real existente para o padrão alvo sem alterar conteúdo editorial.
"""
import json, shutil, sys
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
SRC = REPO / 'education' / 'cursos'
DST = REPO / 'academy' / 'cursos'
INVENTORY = REPO / 'docs' / 'academy' / 'inventory-64-cursos.json'
MIGRATION_REPORT = REPO / 'docs' / 'academy' / 'migration-report.json'

# Estrutura alvo
REQUIRED_DIRS = ['aulas', 'materiais', 'estudos-caso', 'certificado', 'checklists']
REQUIRED_FILES = ['curso.md', 'README.md']

# Mapeamento de estrutura real -> alvo
DIRECTORY_MAPPING = {
    'curso-completo': 'aulas',
    'ebook': 'materiais',
    'planilhas': 'materiais',
    'mini-curso': 'aulas',
    'seo-articles': 'materiais',
    'estudos-caso': 'estudos-caso',
    'certificado': 'certificado',
    'checklists': 'checklists',
    'avaliacao': 'certificado',
    'email-sequence': 'materiais',
    'instagram': 'materiais',
    'marketing': 'materiais',
    'imagens': 'materiais',
}


def load_inventory():
    try:
        data = json.loads(INVENTORY.read_text(encoding='utf-8'))
        items = data if isinstance(data, list) else data.get('items', [])
        return [i for i in items if i.get('slug')]
    except Exception as e:
        print(f'failed to load inventory: {e}')
        sys.exit(2)


def migrate_course(slug: str, src_dir: Path, dst_dir: Path) -> dict:
    result = {
        'slug': slug,
        'status': 'ok',
        'copied': [],
        'mapped': [],
        'missing': [],
        'errors': [],
    }
    if not src_dir.exists():
        result['status'] = 'error'
        result['errors'].append('source_dir_missing')
        return result
    
    dst_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all files/dirs from source
    for item in src_dir.iterdir():
        dst_name = DIRECTORY_MAPPING.get(item.name, item.name)
        dst_item = dst_dir / dst_name
        try:
            if item.is_dir():
                if dst_item.exists():
                    shutil.rmtree(dst_item)
                shutil.copytree(item, dst_item)
                result['copied'].append(f'{item.name}/ -> {dst_name}/')
                if dst_name != item.name:
                    result['mapped'].append(f'{item.name} -> {dst_name}')
            else:
                shutil.copy2(item, dst_item)
                result['copied'].append(item.name)
        except Exception as e:
            result['errors'].append(f'{item.name}: {e}')
    
    # Create curso.md from index.html if it doesn't exist
    if not (dst_dir / 'curso.md').exists() and (dst_dir / 'index.html').exists():
        try:
            html_content = (dst_dir / 'index.html').read_text(encoding='utf-8', errors='ignore')
            # Extract text content from HTML
            import re
            text = re.sub(r'<[^>]+>', ' ', html_content)
            text = re.sub(r'\s+', ' ', text).strip()
            (dst_dir / 'curso.md').write_text(text, encoding='utf-8')
            result['copied'].append('index.html -> curso.md')
        except Exception as e:
            result['errors'].append(f'curso.md generation: {e}')
    
    # Create README.md if it doesn't exist
    if not (dst_dir / 'README.md').exists():
        try:
            readme = f'# {slug}\n\nCurso da Praia Digital Academy.\n'
            (dst_dir / 'README.md').write_text(readme, encoding='utf-8')
            result['copied'].append('README.md')
        except Exception as e:
            result['errors'].append(f'README.md generation: {e}')
    
    return result


def validate_course(dst_dir: Path) -> dict:
    issues = []
    missing = []
    
    # Check required files
    for req_file in REQUIRED_FILES:
        if not (dst_dir / req_file).exists():
            missing.append(req_file)
            issues.append(f'missing_file:{req_file}')
    
    # Check required dirs (after mapping)
    for req_dir in REQUIRED_DIRS:
        found = False
        for src_name, dst_name in DIRECTORY_MAPPING.items():
            if dst_name == req_dir and (dst_dir / src_name).exists():
                found = True
                break
        if not found and not (dst_dir / req_dir).exists():
            missing.append(req_dir)
            issues.append(f'missing_dir:{req_dir}')
    
    # Check aulas has content
    aulas_dir = dst_dir / 'aulas'
    if not aulas_dir.exists():
        # Try curso-completo
        aulas_dir = dst_dir / 'curso-completo'
    if aulas_dir.exists():
        files = list(aulas_dir.glob('*'))
        if not files:
            issues.append('empty_dir:aulas')
    else:
        issues.append('missing_dir:aulas')
    
    # Check materiais has content
    materiais_dirs = [d for d in ['materiais', 'ebook', 'planilhas', 'mini-curso'] if (dst_dir / d).exists()]
    if not materiais_dirs:
        issues.append('missing_dir:materiais')
    
    if missing:
        issues.append(f'missing_components:{", ".join(missing)}')
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'missing': missing,
    }


def main() -> dict:
    inventory = load_inventory()
    slugs = [i['slug'] for i in inventory if i.get('status_final') == 'PRONTO_PARA_VENDA']
    print(f'migrating {len(slugs)} courses...')
    migration_results = []
    validation_results = []
    
    for slug in slugs:
        src_dir = SRC / slug
        dst_dir = DST / slug
        migration = migrate_course(slug, src_dir, dst_dir)
        migration_results.append(migration)
        validation = validate_course(dst_dir)
        validation_results.append({
            'slug': slug,
            **validation,
        })
        if validation['valid']:
            print(f'  {slug}: OK')
        else:
            print(f'  {slug}: ISSUES {validation["issues"]}')
    
    report = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'total': len(slugs),
        'migrated': len([m for m in migration_results if m['status'] == 'ok']),
        'validated': len([v for v in validation_results if v['valid']]),
        'failed_validation': len([v for v in validation_results if not v['valid']]),
        'migrations': migration_results,
        'validations': validation_results,
    }
    MIGRATION_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\nmigration complete: {report["migrated"]} migrated, {report["validated"]} validated, {report["failed_validation"]} failed')
    return report


if __name__ == '__main__':
    result = main()
    sys.exit(0 if result['failed_validation'] == 0 else 1)
