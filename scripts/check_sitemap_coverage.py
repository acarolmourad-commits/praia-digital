from pathlib import Path
import requests

sitemap_path = Path('sitemap.xml')
if not sitemap_path.exists():
    print('sitemap.xml not found')
    raise SystemExit(1)

txt = sitemap_path.read_text(encoding='utf-8', errors='ignore')

# Key URLs that should be in the sitemap
required_urls = [
    'https://praia.digital/education/marketing/lead-magnets/santos.html',
    'https://praia.digital/education/marketing/lead-magnets/guaruja.html',
    'https://praia.digital/education/marketing/lead-magnets/praia-grande.html',
    'https://praia.digital/education/marketing/lead-magnets/bertioga.html',
    'https://praia.digital/education/marketing/lead-magnets/itanhaem.html',
    'https://praia.digital/education/marketing/lead-magnets/mongagua.html',
    'https://praia.digital/education/marketing/lead-magnets/sao-vicente.html',
    'https://praia.digital/education/marketing/lead-magnets/peruibe.html',
    'https://praia.digital/education/marketing/lead-magnets/caraguatatuba.html',
    'https://praia.digital/education/marketing/lead-magnets/ilhabela.html',
    'https://praia.digital/education/marketing/lead-magnets/sao-sebastiao.html',
    'https://praia.digital/education/marketing/lead-magnets/ubatuba.html',
    'https://praia.digital/education/marketing/index.html',
    'https://praia.digital/bairros/caraguatatuba/index.html',
    'https://praia.digital/bairros/ubatuba/index.html',
    'https://praia.digital/bairros/ilhabela/index.html',
    'https://praia.digital/bairros/sao-sebastiao/index.html',
]

missing = []
for url in required_urls:
    if url not in txt:
        missing.append(url)

if missing:
    print('MISSING URLs in sitemap.xml:')
    for url in missing:
        print(f'  - {url}')
    print(f'\nTotal missing: {len(missing)}')
else:
    print('All required URLs are present in sitemap.xml')

# Also check production status for these URLs
print('\nChecking production status...')
for url in required_urls:
    path = url.replace('https://praia.digital', '')
    try:
        r = requests.get('https://praia.digital' + path, timeout=20)
        status = r.status_code
        title = r.text[r.text.find('<title>')+7:r.text.find('</title>')] if r.status_code == 200 else 'N/A'
        print(f'{path}: {status} - {title[:60]}')
    except Exception as e:
        print(f'{path}: ERROR - {e}')
