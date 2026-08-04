from pathlib import Path
import re

root = Path('.').resolve()
files = [
    'blog/abordagem-proprietarios-whatsapp-litoral-2026.html',
    'blog/indicadores-imobiliarias-litoral-paulista-2026.html',
    'blog/precificacao-dinamica-temporada-litoral-paulista-2026.html',
    'blog/automacao-leads-2026-vendas-2026-08-04.html',
    'blog/captacao-2026-imóveis-leads-2026-08-04.html',
    'blog/seo-google-2026-imobiliária-2026-08-04.html',
]

for rel in files:
    p = root / rel
    txt = p.read_text(encoding='utf-8', errors='ignore')
    original = txt

    title = re.search(r'<title>(.*?)</title>', txt, flags=re.I)
    title = title.group(1).strip() if title else rel
    desc = re.search(r'<meta\s+name="description"\s+(?:content=["\'](.*?)["\']|=["\'](.*?)["\'])', txt, flags=re.I)
    if desc:
        desc_text = desc.group(1) or desc.group(2) or ''
    else:
        desc_text = title
    desc_text = desc_text.strip().strip("'\"") or title
    url_canonical = f'https://praia.digital/{rel}'
    img = 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=60'

    # Fix malformed meta description: <meta name="description"=...> -> <meta name="description" content="...">
    txt = re.sub(
        r'<meta\s+name="description"\s*=\s*["\']([^"\']*)["\']',
        lambda m: f'<meta name="description" content="{m.group(1)}">',
        txt,
        flags=re.I,
    )

    # Fill empty og:description and twitter:description
    txt = re.sub(
        r'(<meta\s+property="og:description"\s+content=")([^"]*)"',
        lambda m: m.group(1) + desc_text.replace('"', '&quot;') + '"',
        txt,
        flags=re.I,
    )
    txt = re.sub(
        r'(<meta\s+name="twitter:description"\s+content=")([^"]*)"',
        lambda m: m.group(1) + desc_text.replace('"', '&quot;') + '"',
        txt,
        flags=re.I,
    )

    # Ensure canonical exists
    if not re.search(r'<link\s+rel="canonical"\s+href="https://praia\.digital/', txt, flags=re.I):
        insert_marker = '</head>'
        canonical_block = f'  <link rel="canonical" href="{url_canonical}">\n'
        txt = txt.replace(insert_marker, canonical_block + insert_marker, 1)

    # Ensure og tags exist
    if not re.search(r'<meta\s+property="og:title"', txt, flags=re.I):
        og_block = f'''  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc_text.replace('"', '&quot;')}">
  <meta property="og:image" content="{img}">
  <meta property="og:url" content="{url_canonical}">
'''
        txt = txt.replace('</head>', og_block + '</head>', 1)
    else:
        # fill missing og:title/url/image if empty
        txt = re.sub(r'(<meta\s+property="og:title"\s+content=")([^"]*)"', lambda m: m.group(1) + title.replace('"', '&quot;') + '"', txt, flags=re.I)
        txt = re.sub(r'(<meta\s+property="og:url"\s+content=")([^"]*)"', lambda m: m.group(1) + url_canonical + '"', txt, flags=re.I)
        if not re.search(r'<meta\s+property="og:image"', txt, flags=re.I):
            txt = re.sub(r'</head>', f'  <meta property="og:image" content="{img}">\n</head>', txt, flags=re.I)

    # Ensure twitter tags exist
    if not re.search(r'<meta\s+name="twitter:card"', txt, flags=re.I):
        tw_block = f'''  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc_text.replace('"', '&quot;')}">
  <meta name="twitter:image" content="{img}">
'''
        txt = txt.replace('</head>', tw_block + '</head>', 1)
    else:
        txt = re.sub(r'(<meta\s+name="twitter:title"\s+content=")([^"]*)"', lambda m: m.group(1) + title.replace('"', '&quot;') + '"', txt, flags=re.I)
        if not re.search(r'<meta\s+name="twitter:image"', txt, flags=re.I):
            txt = re.sub(r'</head>', f'  <meta name="twitter:image" content="{img}">\n</head>', txt, flags=re.I)

    # Ensure JSON-LD BlogPosting exists with non-empty description
    if 'application/ld+json' not in txt:
        ld = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{title}",
  "description": "{desc_text.replace('"', '&quot;')}",
  "url": "{url_canonical}",
  "author": {{"@type": "Organization", "name": "Litoral Prime Imóveis"}},
  "publisher": {{"@type": "Organization", "name": "Litoral Prime Imóveis", "url": "https://praia.digital/"}}
}}
</script>
'''
        txt = txt.replace('</head>', ld + '</head>', 1)
    else:
        # patch empty "description": "" in BlogPosting JSON-LD
        def fill_json_desc(m):
            block = m.group(0)
            block = re.sub(r'"description":\s*""', f'"description": "{desc_text.replace(chr(34), chr(34))}"', block)
            return block
        txt = re.sub(r'<script\s+type="application/ld\+json">.*?</script>', fill_json_desc, txt, flags=re.S|re.I)

    # Ensure hreflang tags exist
    if 'hreflang' not in txt:
        xdefault = url_canonical.replace('/blog/', '/blog\\')
        hr = f'''  <link rel="alternate" hreflang="x-default" href="{xdefault}" />
  <link rel="alternate" hreflang="pt-BR" href="{url_canonical}">
'''
        txt = txt.replace('</head>', hr + '</head>', 1)

    if txt != original:
        p.write_text(txt, encoding='utf-8')
        print('patched', rel)
    else:
        print('unchanged', rel)
