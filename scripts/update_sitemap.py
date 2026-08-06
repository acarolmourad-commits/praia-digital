from pathlib import Path

sitemap_path = Path('sitemap.xml')
if not sitemap_path.exists():
    print('sitemap.xml not found')
    raise SystemExit(1)

txt = sitemap_path.read_text(encoding='utf-8', errors='ignore')

# URLs to add
new_urls = [
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
]

# Check which are already present
missing = [url for url in new_urls if url not in txt]

if not missing:
    print('All URLs already present in sitemap.xml')
    raise SystemExit(0)

# Build XML entries
entries = []
for url in missing:
    entries.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>2026-08-06T03:00:00Z</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>""")

new_block = '\n'.join(entries)

# Insert before closing </urlset>
if '</urlset>' in txt:
    txt = txt.replace('</urlset>', f'{new_block}\n</urlset>')
else:
    print('Could not find </urlset> tag')
    raise SystemExit(1)

sitemap_path.write_text(txt, encoding='utf-8')
print(f'Added {len(missing)} URLs to sitemap.xml')

# Verify
added = sum(1 for url in missing if url in sitemap_path.read_text(encoding='utf-8', errors='ignore'))
print(f'Verification: {added}/{len(missing)} URLs confirmed in sitemap')
