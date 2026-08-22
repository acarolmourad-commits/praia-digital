"""Implementação controlada da Arquitetura B."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
CHECKPOINT = BASE / 'scripts/arquitetura-b-checkpoint.json'
BATCH_LOG = BASE / 'scripts/arquitetura-b-batch-log.json'

# Arquivos-alvo na ordem de implementação
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

# Mapa de breadcrumbs por arquivo
BREADCRUMBS = {
    'index.html': [
        {'name': 'Início', 'item': 'https://praia.digital/'}
    ],
    'servicos.html': [
        {'name': 'Início', 'item': 'https://praia.digital/'},
        {'name': 'Serviços', 'item': 'https://praia.digital/servicos.html'}
    ],
    'contato.html': [
        {'name': 'Início', 'item': 'https://praia.digital/'},
        {'name': 'Contato', 'item': 'https://praia.digital/contato.html'}
    ],
    'education/index.html': [
        {'name': 'Início', 'item': 'https://praia.digital/'},
        {'name': 'Academy', 'item': 'https://praia.digital/education/index.html'}
    ],
}

# Mapa de CTAs por jornada
CTAS = {
    'servicos.html': {
        'primary': 'Solicitar orçamento',
        'href': 'https://wa.me/5511954346288?text=Olá!%20Quero%20solicitar%20um%20orçamento%20de%20serviço%20imobiliário.',
        'label': 'Ver serviços'
    },
    'education/index.html': {
        'primary': 'Ver cursos',
        'href': 'https://praia.digital/education/cursos/index.html',
        'label': 'Acessar Academy'
    },
    'contato.html': {
        'primary': 'Falar com a Praia Digital',
        'href': 'https://wa.me/5511954346288?text=Olá!%20Quero%20falar%20com%20a%20Praia%20Digital.',
        'label': 'Contato'
    }
}


def breadcrumb_json(items):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": item['name'],
                "item": item['item']
            }
            for i, item in enumerate(items)
        ]
    }, ensure_ascii=False)


def inject_breadcrumb(text, items):
    tag = f'<script type="application/ld+json">\n{breadcrumb_json(items)}\n  </script>\n'
    if 'BreadcrumbList' in text:
        # Replace existing breadcrumb
        import re
        text = re.sub(
            r'<script type="application/ld+json">\s*{\s*"@context".*?"BreadcrumbList".*?</script>',
            tag.strip(),
            text,
            flags=re.DOTALL | re.IGNORECASE
        )
    else:
        # Insert after first script tag or in head
        text = text.replace('</title>', '</title>\n  ' + tag.strip())
    return text


def inject_cta(text, cta):
    if not cta:
        return text
    cta_html = f'<a class="btn" href="{cta["href"]}">{cta["primary"]}</a>'
    if cta_html in text:
        return text
    # Add before closing </body> or before footer
    if '</body>' in text:
        text = text.replace('</body>', f'  <div class="cta-section">\n    {cta_html}\n  </div>\n</body>')
    return text


def main():
    checkpoint = json.loads(CHECKPOINT.read_text(encoding='utf-8'))
    batch_id = 'arquitetura-b-lote-1-' + datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    results = []
    
    for rel in HTML_TARGETS:
        p = BASE / rel
        if not p.exists():
            continue
        
        text = p.read_text(encoding='utf-8', errors='ignore')
        original_hash = checkpoint['files'].get(rel, {}).get('hash', '')
        
        # Apply breadcrumb if defined
        if rel in BREADCRUMBS:
            text = inject_breadcrumb(text, BREADCRUMBS[rel])
        
        # Apply CTA if defined
        if rel in CTAS:
            text = inject_cta(text, CTAS[rel])
        
        # Write if changed
        new_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]
        if new_hash != original_hash:
            p.write_text(text, encoding='utf-8')
            results.append({
                'file': rel,
                'status': 'APPLIED',
                'hash_before': original_hash,
                'hash_after': new_hash,
                'breadcrumb': rel in BREADCRUMBS,
                'cta': rel in CTAS,
            })
        else:
            results.append({
                'file': rel,
                'status': 'NO_CHANGE',
                'hash_before': original_hash,
                'hash_after': new_hash,
            })
    
    output = {
        'batch_id': batch_id,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'results': results,
        'applied': sum(1 for r in results if r['status'] == 'APPLIED'),
    }
    BATCH_LOG.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    print('batch_id=', batch_id)
    print('applied=', output['applied'])
    for r in results:
        print(r['file'], r['status'])


if __name__ == '__main__':
    main()
