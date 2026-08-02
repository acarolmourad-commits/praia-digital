from pathlib import Path
import re
import json

root = Path('.')

pages = {
    'servicos.html': [
        ('FAQPage', None),
        ('WebSite', None),
        ('LocalBusiness', None),
        ('Service', None),
        ('Organization', {
            "name": "Litoral Prime Imóveis",
            "url": "https://praia.digital/",
            "logo": "https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/img/logo.png",
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+55-11-95434-6288",
                "contactType": "sales",
                "areaServed": "BR",
                "availableLanguage": ["pt-BR", "en"]
            },
            "openingHoursSpecification": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "opens": "09:00",
                "closes": "18:00"
            }
        }),
    ],
    'cases.html': [
        ('FAQPage', None),
        ('WebSite', None),
        ('Organization', {
            "name": "Litoral Prime Imóveis",
            "url": "https://praia.digital/",
            "logo": "https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/img/logo.png",
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+55-11-95434-6288",
                "contactType": "sales",
                "areaServed": "BR",
                "availableLanguage": ["pt-BR", "en"]
            },
            "openingHoursSpecification": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "opens": "09:00",
                "closes": "18:00"
            }
        }),
    ],
    'blog/index.html': [
        ('FAQPage', None),
        ('Article', None),
        ('WebSite', None),
        ('Organization', {
            "name": "Litoral Prime Imóveis",
            "url": "https://praia.digital/",
            "logo": "https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/img/logo.png",
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+55-11-95434-6288",
                "contactType": "sales",
                "areaServed": "BR",
                "availableLanguage": ["pt-BR", "en"]
            },
            "openingHoursSpecification": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "opens": "09:00",
                "closes": "18:00"
            }
        }),
    ],
}

for rel, entries in pages.items():
    path = root / rel
    text = path.read_text(encoding='utf-8', errors='ignore')
    import re, json
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
    for idx, (typ, enrich) in enumerate(entries, 1):
        if idx > len(blocks):
            print('missing block', rel, typ)
            continue
        block = blocks[idx-1]
        try:
            data = json.loads(block)
        except Exception as e:
            print('invalid json', rel, idx, e)
            continue
        if data.get('@type') != typ:
            print('type mismatch', rel, idx, data.get('@type'), typ)
            continue
        if enrich:
            for k, v in enrich.items():
                data[k] = v
            new_block = json.dumps(data, ensure_ascii=False, indent=2)
            old_block = block
            marker = f'<script type="application/ld+json">{old_block}</script>'
            new_marker = f'<script type="application/ld+json">{new_block}</script>'
            if marker in text:
                text = text.replace(marker, new_marker, 1)
                print('updated', rel, typ)
            else:
                print('marker not found', rel, typ)
    if text != path.read_text(encoding='utf-8', errors='ignore'):
        path.write_text(text, encoding='utf-8')
