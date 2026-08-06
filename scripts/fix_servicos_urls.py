from pathlib import Path
import re

base = Path('servicos/cidade-servico')
fixed = []
wrong_city_issues = []

for p in base.glob('*.html'):
    txt = p.read_text(encoding='utf-8', errors='ignore')
    stem = p.stem
    parts = stem.split('-', 1)
    if len(parts) != 2:
        continue
    city, service = parts
    expected_url = f'https://praia.digital/servicos/cidade-servico/{city}-{service}.html'
    
    new = txt
    new = re.sub(
        r'<link rel="alternate" hreflang="x-default" href="https://praia\.digital/servicoscidade-servico[^"]*" />',
        f'<link rel="alternate" hreflang="x-default" href="{expected_url}" />',
        new
    )
    new = new.replace('\\', '/')
    new = re.sub(
        r'<link rel="canonical" href="https://praia\.digital/servicos/cidade-servico/[^"]+"',
        f'<link rel="canonical" href="{expected_url}"',
        new
    )
    new = re.sub(
        r'<meta property="og:url" content="https://praia\.digital/servicos/cidade-servico/[^"]+"',
        f'<meta property="og:url" content="{expected_url}"',
        new
    )
    new = re.sub(
        r'"url": "https://praia\.digital/servicos/cidade-servico/[^"]+"',
        f'"url": "{expected_url}"',
        new
    )
    new = re.sub(
        r'\{"@type": "ListItem", "position": 4, "name": "[^"]+", "item": "https://praia\.digital/servicos/cidade-servico/[^"]+"\}',
        f'{{"@type": "ListItem", "position": 4, "name": "{city.title()}", "item": "{expected_url}"}}',
        new
    )
    
    if new != txt:
        p.write_text(new, encoding='utf-8')
        fixed.append(str(p))
        
        m = re.search(r'<link rel="canonical" href="([^"]+)"', new)
        if m and m.group(1) != expected_url:
            wrong_city_issues.append((p.name, m.group(1), expected_url))

print(f'Fixed: {len(fixed)}')
for f in fixed[:5]:
    print(f)
if wrong_city_issues:
    print('Still wrong canonical:', len(wrong_city_issues))
    for item in wrong_city_issues[:3]:
        print(item)
