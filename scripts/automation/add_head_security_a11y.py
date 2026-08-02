#!/usr/bin/env python3
"""
add_head_security_a11y.py
Adiciona head improvements de segurança e acessibilidade: referrer policy, preconnect e skip navigation.
"""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[2]
exclude = {'.git', 'node_modules', 'backups', 'scripts', 'assets', 'docs', 'outreach', 'leads'}

updated = 0
skipped = 0
errors = 0
for path in sorted(BASE.rglob('*.html')):
    rel = path.relative_to(BASE)
    if any(part in exclude for part in rel.parts):
        skipped += 1
        continue
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        errors += 1
        continue

    head_tags = []
    if not re.search(r'<meta[^>]*name=["\']referrer["\']', text, re.S|re.I):
        head_tags.append('<meta name="referrer" content="no-referrer-when-downgrade">')
    if not re.search(r'<link[^>]*rel=["\'](preconnect|dns-prefetch)', text, re.S|re.I):
        head_tags.append('<link rel="preconnect" href="https://images.unsplash.com" crossorigin>')
        head_tags.append('<link rel="preconnect" href="https://acarolmourad.github.io" crossorigin>')

    if head_tags:
        tag_block = '\n'.join(head_tags)
        if '</head>' in text:
            text = text.replace('</head>', tag_block + '\n</head>', 1)
        elif '<head>' in text:
            text = text.replace('<head>', '<head>\n' + tag_block, 1)
        else:
            text = tag_block + '\n' + text

    if 'skip' not in text.lower() or 'nav' not in text.lower():
        if '<body>' in text:
            skip_link = '<a class="skip-link" href="#main" style="position:absolute;left:-9999px;">Pular para o conteúdo</a>'
            text = text.replace('<body>', '<body>\n' + skip_link, 1)
            if 'id="main"' not in text.lower():
                text = text.replace('<main', '<main id="main"', 1)
        elif '<main' in text:
            skip_link = '<a class="skip-link" href="#main" style="position:absolute;left:-9999px;">Pular para o conteúdo</a>'
            text = text.replace('<main', skip_link + '\n<main', 1)

    if text != path.read_text(encoding='utf-8', errors='ignore'):
        try:
            path.write_text(text, encoding='utf-8')
            print('updated', rel)
            updated += 1
        except Exception as e:
            print('write error', rel, e)
            errors += 1
    else:
        skipped += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
