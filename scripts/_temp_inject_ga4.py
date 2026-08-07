from pathlib import Path

GA4_SNIPPET = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA4_MEASUREMENT_ID"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'GA4_MEASUREMENT_ID', { anonymize_ip: true });
</script>'''

# Public-facing directories to fill remaining gaps
PUBLIC_DIRS = [
    Path('servicos'),
    Path('education'),
    Path('cidades'),
    Path('bairros'),
    Path('cidades-expansao'),
    Path('imoveis'),
    Path('assets'),
    Path('anfitrioes'),
    Path('eventos-litoral-paulista-2026-2027'),
    Path('ferramentas-gratuitas'),
    Path('ferramentas'),
    Path('hub'),
    Path('leads'),
    Path('docs'),
    Path('litoral-prime-imoveis'),
]

count = 0
for html_file in Path('.').rglob('*.html'):
    try:
        text = html_file.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    if 'googletagmanager.com/gtag/js' in text:
        continue
    # Only process if under a public dir
    if not any(str(html_file).startswith(str(d)) for d in PUBLIC_DIRS):
        continue
    if '</head>' in text:
        text = text.replace('</head>', GA4_SNIPPET + '\n</head>', 1)
        html_file.write_text(text, encoding='utf-8')
        count += 1

print(f'Injected GA4 placeholder in {count} additional pages')
