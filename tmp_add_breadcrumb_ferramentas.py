from pathlib import Path
import re

# Process specific directories with missing breadcrumbs
dirs = ['ferramentas-gratuitas', 'ferramentas-gratuitas-imobiliarias']

for base_name in dirs:
    base = Path(base_name)
    if not base.exists():
        continue
    files = sorted(base.rglob('*.html'))
    for path in files:
        text = path.read_text(encoding='utf-8', errors='ignore')
        if 'BreadcrumbList' in text:
            continue

        rel = path.relative_to(base)
        parts = rel.parts

        items = [
            { 'name': 'Início', 'item': 'https://praia.digital/index.html' },
            { 'name': base_name.replace('-', ' ').title(), 'item': f'https://praia.digital/{base_name}/' }
        ]

        url_parts = [base_name]
        for part in parts[:-1]:
            url_parts.append(part)
            part_title = part.replace('-', ' ').title()
            items.append({ 'name': part_title, 'item': 'https://praia.digital/' + '/'.join(url_parts) + '/' })

        page_name = path.stem.replace('-', ' ').title()
        url_parts.append(path.name)
        url = 'https://praia.digital/' + '/'.join(url_parts)
        items.append({ 'name': page_name, 'item': url })

        json_items = []
        for idx, item in enumerate(items, 1):
            json_items.append('      { "@type": "ListItem", "position": ' + str(idx) + ', "name": "' + item['name'] + '", "item": "' + item['item'] + '" }')

        breadcrumb = '\n  <link rel="preconnect" href="https://praia.digital">\n  <script type="application/ld+json">\n  {\n    "@context": "https://schema.org",\n    "@type": "BreadcrumbList",\n    "itemListElement": [\n' + '\n'.join(json_items) + '\n    ]\n  }\n  </script>'

        text = text.replace('</title>', '</title>' + breadcrumb, 1)
        path.write_text(text, encoding='utf-8')
        print('updated', path)
