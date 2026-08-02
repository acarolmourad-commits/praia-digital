#!/usr/bin/env python3
"""
add_localbusiness.py
Adiciona LocalBusiness/RealEstateAgent JSON-LD em páginas públicas relevantes sem esse schema.
"""
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

root_pages = {
    'index.html': {
        'name': 'Praia Digital',
        'type': 'RealEstateAgent',
        'city': 'Santos',
        'state': 'SP',
        'phone': '(11) 95434-6288',
        'email': 'comercial@praia.digital',
    },
    'imoveis.html': {
        'name': 'Litoral Prime Imóveis',
        'type': 'RealEstateAgent',
        'city': 'Santos',
        'state': 'SP',
        'phone': '(11) 95434-6288',
        'email': 'comercial@praia.digital',
    },
    'servicos.html': {
        'name': 'Praia Digital',
        'type': 'RealEstateAgent',
        'city': 'Santos',
        'state': 'SP',
        'phone': '(11) 95434-6288',
        'email': 'comercial@praia.digital',
    },
}

city_map = {
    'santos': 'Santos',
    'guaruja': 'Guarujá',
    'praia-grande': 'Praia Grande',
    'itanhaem': 'Itanhaém',
    'mongagua': 'Mongaguá',
    'sao-vicente': 'São Vicente',
    'peruibe': 'Peruíbe',
    'bertioga': 'Bertioga',
    'ubatuba': 'Ubatuba',
    'caraguatatuba': 'Caraguatatuba',
}

template = '''
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "{type}",
  "name": "{name}",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "{city}",
    "addressRegion": "{state}",
    "addressCountry": "BR"
  }},
  "telephone": "{phone}",
  "email": "{email}",
  "areaServed": [
    "Santos","Guarujá","Praia Grande","Bertioga","Itanhaém","Mongaguá","São Vicente","Peruíbe"
  ],
  "knowsLanguage": ["pt-BR","en"],
  "openingHoursSpecification": {{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "09:00",
    "closes": "18:00"
  }}
}}
</script>
'''

def allowed(path: Path):
    rel = path.relative_to(BASE)
    if rel.parts[0] in {'cidades', 'servicos'}:
        return True
    if rel.parts[0] == 'litoral-prime-imoveis' and rel.parts[1] in {'cidades', 'servicos'}:
        return True
    if rel.parent == BASE and rel.name in root_pages:
        return True
    return False

updated = 0
skipped = 0
errors = 0
for path in sorted(BASE.rglob('*.html')):
    rel = path.relative_to(BASE)
    name = path.name
    if not allowed(path):
        continue
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        errors += 1
        continue
    if 'LocalBusiness' in text or 'RealEstateAgent' in text:
        skipped += 1
        continue
    if rel.parent == BASE:
        data = root_pages.get(name)
    else:
        data = None
        if rel.parts[0] == 'cidades' or (rel.parts[0] == 'litoral-prime-imoveis' and len(rel.parts) > 1 and rel.parts[1] == 'cidades'):
            slug = name.replace('.html', '')
            city = city_map.get(slug)
            if city:
                data = {
                    'name': f'Litoral Prime Imóveis - {city}',
                    'type': 'RealEstateAgent',
                    'city': city,
                    'state': 'SP',
                    'phone': '(11) 95434-6288',
                    'email': 'comercial@praia.digital',
                }
        elif rel.parts[0] == 'servicos' or (rel.parts[0] == 'litoral-prime-imoveis' and len(rel.parts) > 1 and rel.parts[1] == 'servicos'):
            data = root_pages['servicos.html']
    if not data:
        skipped += 1
        continue
    block = template.format(**data)
    if '<head>' not in text:
        skipped += 1
        continue
    text = text.replace('<head>', '<head>\n' + block, 1)
    path.write_text(text, encoding='utf-8')
    print('updated', rel)
    updated += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
