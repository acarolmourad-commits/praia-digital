"""Validação automática da Arquitetura B."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
REPORT = BASE / 'scripts/arquitetura-b-validation-report.json'

HTML_TARGETS = [
    'index.html',
    'servicos.html',
    'contato.html',
    'education/index.html',
    'cidades/santos.html',
    'cidades/guaruja.html',
    'cidades/praia-grande.html',
    'cidades/bertioga.html',
    'cidades/itanhaem.html',
    'cidades/sao-vicente.html',
    'cidades/mongagua.html',
    'cidades/peruibe.html',
    'servicos/cidade-servico/santos-captacao.html',
]


def validate_file(rel):
    p = BASE / rel
    if not p.exists():
        return {'file': rel, 'exists': False, 'valid': False, 'issues': ['missing']}
    
    text = p.read_text(encoding='utf-8', errors='ignore')
    issues = []
    
    # Check schema
    if not re.search(r'<script[^>]+type="application/ld\+json"', text, re.I):
        issues.append('missing_schema')
    
    # Check title
    if not re.search(r'<title[^>]*>.*?</title>', text, re.I | re.S):
        issues.append('missing_title')
    
    # Check canonical
    if not re.search(r'<link[^>]+rel="canonical"', text, re.I):
        issues.append('missing_canonical')
    
    # Check viewport
    if not re.search(r'<meta[^>]+name="viewport"', text, re.I):
        issues.append('missing_viewport')
    
    # Check lang
    if not re.search(r'<html[^>]+lang="pt-BR"', text, re.I):
        issues.append('missing_lang')
    
    return {
        'file': rel,
        'exists': True,
        'valid': len(issues) == 0,
        'issues': issues,
    }


def main():
    results = []
    for rel in HTML_TARGETS:
        results.append(validate_file(rel))
    
    valid = sum(1 for r in results if r['valid'])
    invalid = [r for r in results if not r['valid']]
    
    report = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'total': len(results),
        'valid': valid,
        'invalid': len(invalid),
        'details': results,
        'invalid_details': invalid,
    }
    
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('total=', len(results))
    print('valid=', valid)
    print('invalid=', len(invalid))
    for r in invalid:
        print(r['file'], r['issues'])


if __name__ == '__main__':
    main()
