from pathlib import Path
import re

root = Path('blog')

breadcrumb_template = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Início",
      "item": "https://acarolmourad.github.io/praia-digital/index.html"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "https://acarolmourad.github.io/praia-digital/blog/index.html"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "__TITLE__",
      "item": "https://acarolmourad.github.io/praia-digital/blog/__SLUG__"
    }
  ]
}
</script>
'''

updated = 0
skipped = 0
for path in root.glob('*.html'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'BreadcrumbList' in text:
        skipped += 1
        continue

    # extract title from <title> tag
    title_match = re.search(r'<title>(.*?)</title>', text, re.I | re.S)
    if not title_match:
        skipped += 1
        continue
    title = title_match.group(1).strip()

    slug = path.name

    breadcrumb = breadcrumb_template.replace('__TITLE__', title).replace('__SLUG__', slug)

    # insert before </head>
    if '</head>' in text:
        new_text = text.replace('</head>', breadcrumb + '</head>', 1)
    else:
        skipped += 1
        continue

    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('updated', path.name)
        updated += 1
    else:
        skipped += 1

print('updated', updated, 'skipped', skipped)
