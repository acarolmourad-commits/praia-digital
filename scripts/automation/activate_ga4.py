from pathlib import Path
import sys, re
REPO = Path('.').resolve()
PUBLIC_DIRS = [
    REPO,
    REPO / 'imoveis',
    REPO / 'blog',
    REPO / 'cidades',
    REPO / 'hub',
    REPO / 'anfitrioes',
    REPO / 'personas',
    REPO / 'cases',
    REPO / 'exclusivos',
    REPO / 'investidores',
]
if len(sys.argv) < 2:
    print('Usage: python activate_ga4.py GA4_ID')
    sys.exit(1)
ga4_id = sys.argv[1].strip()
if not re.match(r'^G-[A-Z0-9]+$', ga4_id):
    print('Invalid GA4 ID format. Expected G-XXXXXXXXXX')
    sys.exit(1)
ga_block = f'''  <script async src="https://www.googletagmanager.com/gtag/js?id={ga4_id}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{ga4_id}', {{ anonymize_ip: true }});
  </script>
'''
patched = 0
skipped = 0
for base in PUBLIC_DIRS:
    if not base.exists():
        continue
    for path in base.rglob('*.html'):
        text = path.read_text(encoding='utf-8', errors='ignore')
        if 'googletagmanager.com/gtag/js' in text or 'dataLayer.push(arguments);' in text:
            skipped += 1
            continue
        if '</head>' in text:
            text = text.replace('</head>', ga_block + '</head>', 1)
            path.write_text(text, encoding='utf-8')
            patched += 1
print('GA4_ACTIVATED', patched)
print('GA4_SKIPPED', skipped)
