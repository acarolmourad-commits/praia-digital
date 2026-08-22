"""Bounded internal link checker: top-level and first-subdir HTML only."""
import re
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
html_files = sorted([p for p in BASE.rglob('*.html') if len(p.relative_to(BASE).parts) <= 2])
print(f'Checking {len(html_files)} HTML files...')
link_re = re.compile(r'href=[\"\']([^\"\']+)[\"\']', re.IGNORECASE)
src_re = re.compile(r'src=[\"\']([^\"\']+)[\"\']', re.IGNORECASE)
broken = []
checked = 0
for html_path in html_files:
    rel = html_path.relative_to(BASE)
    text = html_path.read_text(encoding='utf-8', errors='ignore')
    refs = link_re.findall(text) + src_re.findall(text)
    for ref in refs:
        if ref.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', '//', 'data:')):
            continue
        target = ref.lstrip('/').replace('/', '\\')
        if not (BASE / target).exists():
            broken.append((str(rel), ref, target))
    checked += 1
print(f'Checked: {checked}')
print(f'Broken internal refs: {len(broken)}')
for source, ref, target in broken[:80]:
    print(f'{source} -> {ref}')
