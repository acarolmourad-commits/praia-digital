#!/usr/bin/env python3
"""
fix_meta_descriptions.py
Limpa tags HTML de meta descriptions e corrige títulos genéricos de imóveis.
"""
from pathlib import Path
import re, json

BASE = Path(__file__).resolve().parents[2]

# 1) Fix generic imovel titles
imoveis_dir = BASE / 'imoveis'
fixed_titles = 0
for path in sorted(imoveis_dir.glob('*.html')):
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    if '<title>Imóvel | Praia Digital</title>' not in text:
        continue
    # Try to extract from JSON-LD
    title = None
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try:
            data = json.loads(m.group(1).strip())
            t = data.get('@type')
            if t == 'RealEstateListing' or (isinstance(t, list) and 'RealEstateListing' in t):
                title = data.get('name')
                if title:
                    break
        except Exception:
            pass
    if not title:
        # Try h1
        m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S|re.I)
        if m:
            title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    if not title:
        title = path.stem.replace('-', ' ').title()
    if title:
        text = re.sub(r'<title>.*?</title>', f'<title>{title} | Litoral Prime Imóveis</title>', text, count=1, flags=re.S|re.I)
        path.write_text(text, encoding='utf-8')
        print('fixed title', path.relative_to(BASE))
        fixed_titles += 1
print('fixed titles:', fixed_titles)

# 2) Strip HTML from meta descriptions
fixed_descs = 0
for path in sorted(BASE.rglob('*.html')):
    rel = path.relative_to(BASE)
    if any(part in {'.git', 'node_modules', 'backups', 'scripts', 'assets', 'docs', 'outreach', 'leads'} for part in rel.parts):
        continue
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    def replace_desc(m):
        desc = m.group(1).strip()
        if '<' in desc and '>' in desc:
            clean = re.sub(r'<[^>]+>', '', desc)
            clean = re.sub(r'\s+', ' ', clean).strip()
            if len(clean) > 155:
                clean = clean[:152].rsplit(' ', 1)[0] + '...'
            return f'content="{clean}"'
        return m.group(0)
    new_text = re.sub(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', replace_desc, text, flags=re.S|re.I)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('fixed desc', rel)
        fixed_descs += 1
print('fixed descriptions:', fixed_descs)
