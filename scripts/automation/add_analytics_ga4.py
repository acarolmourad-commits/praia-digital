from pathlib import Path
import argparse

REPO = Path('.').resolve()
PUBLIC_DIRS = [
    REPO,
    REPO / 'imoveis',
    REPO / 'bairros',
    REPO / 'hub',
    REPO / 'blog',
    REPO / 'cidades',
    REPO / 'anfitrioes',
    REPO / 'personas',
    REPO / 'cases',
    REPO / 'exclusivos',
    REPO / 'investidores',
]

parser = argparse.ArgumentParser()
parser.add_argument('--ga4-id', default='')
parser.add_argument('--dry-run', action='store_true')
args = parser.parse_args()

ga4_id = args.ga4_id.strip()
if not ga4_id:
    print('GA4_SKIPPED no id provided')
    exit(0)

ga_block = f'''  <script async src="https://www.googletagmanager.com/gtag/js?id={ga4_id}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{ga4_id}', {{ anonymize_ip: true }});
  </script>
'''

patched = 0
for base in PUBLIC_DIRS:
    if not base.exists():
        continue
    for path in base.rglob('*.html'):
        text = path.read_text(encoding='utf-8', errors='ignore')
        if 'googletagmanager.com/gtag/js' in text or 'dataLayer.push(arguments);' in text:
            continue
        if args.dry_run:
            continue
        text = text.replace('</head>', ga_block + '</head>', 1)
        path.write_text(text, encoding='utf-8')
        patched += 1

print('GA4_ADDED', patched)
