"""Keep recorded indexing decisions when legacy templates regenerate pages.

Decisions come from PR #130's manifest, not inferred property characteristics.
The empty-article rule matches the existing validator's exact draft template.
"""
import json
import re
from pathlib import Path
from validate_sitemap_targets import is_placeholder_article, IndexingDirectives

ROOT = Path(__file__).resolve().parents[1]
NOTE = '<p class="pd-indexing-note" role="note"><strong>Registro demonstrativo.</strong> Preço e características deste exemplo foram gerados automaticamente e não constituem uma oferta confirmada. <a href="/imoveis.html">Consulte o catálogo atual de imóveis.</a></p>'


def preserve(text, path, root=ROOT):
    root = Path(root)
    rel = Path(path).resolve().relative_to(root.resolve()).as_posix()
    intent = json.loads((root / 'data/indexing-intent-20261111.json').read_text(encoding='utf-8'))
    canonical = intent['canonicals'].get(rel)
    directives = IndexingDirectives()
    directives.feed(text)
    if canonical and directives.canonicals != [canonical]:
        tag = '<link rel="canonical" href="' + canonical + '">'
        pattern = r'[ \t]*<link\b[^>]*rel=[\"\']canonical[\"\'][^>]*>'
        if re.search(pattern, text, re.I):
            text = re.sub(pattern, '', text, flags=re.I)
        text = text.replace('</head>', tag + '\n</head>', 1)
    demonstrative = rel.startswith('litoral-prime-imoveis/imoveis/') and Path(rel).stem in intent['evidence']['generated_listings']['slugs']
    if 'noindex' not in directives.reasons and (rel in intent['noindex'] or (rel.startswith('blog/') and is_placeholder_article(text))):
        text = re.sub(r'<meta\b[^>]*name=[\"\']robots[\"\'][^>]*>', '', text, flags=re.I)
        text = text.replace('</head>', '<meta name="robots" content="noindex, follow">\n</head>', 1)
    if demonstrative:
        old = 'https://praia.digital/imoveis/' + Path(rel).name
        text = text.replace(old, canonical)
        if 'class="pd-indexing-note"' not in text:
            text = text.replace('<main id="main">', '<main id="main">\n' + NOTE, 1)
    return text
