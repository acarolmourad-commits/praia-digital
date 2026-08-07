from pathlib import Path
import re

GA4_SNIPPET = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA4_MEASUREMENT_ID"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'GA4_MEASUREMENT_ID', { anonymize_ip: true });
</script>'''

# Directories to inject GA4 into
INJECT_DIRS = [
    Path('blog'),
    Path('servicos'),
    Path('education'),
    Path('bairros'),
    Path('cidades'),
    Path('cidades-expansao'),
    Path('imoveis'),
    Path('assets'),
    Path('anfitrioes'),
]

# Exclude these subdirectories
EXCLUDE_DIRS = {
    'outreach',
    'templates',
    'marketing',
    'campaigns',
    'aluno',
    '__pycache__',
}

def should_process(path: Path) -> bool:
    # Must be under an inject dir
    if not any(str(path).startswith(str(d)) for d in INJECT_DIRS):
        return False
    # Exclude certain subpaths
    rel = path.relative_to(Path('.'))
    parts = rel.parts
    if any(ex in parts for ex in EXCLUDE_DIRS):
        return False
    if 'sitemap.xml' in str(path):
        return False
    return True

count = 0
errors = []
for html_file in Path('.').rglob('*.html'):
    if not should_process(html_file):
        continue
    try:
        text = html_file.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        errors.append(f"{html_file}: {e}")
        continue
    if 'googletagmanager.com/gtag/js' in text:
        continue
    # Insert GA4 snippet before </head>
    if '</head>' in text:
        text = text.replace('</head>', GA4_SNIPPET + '\n</head>', 1)
        html_file.write_text(text, encoding='utf-8')
        count += 1

print(f'Injected GA4 placeholder in {count} pages')
if errors:
    print(f'Errors: {len(errors)}')
    for e in errors[:10]:
        print(' ', e)
