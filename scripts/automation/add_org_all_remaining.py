from pathlib import Path
import re

root = Path('.')
exclude = {'.git', 'node_modules', 'backups', 'scripts', 'assets', 'docs', 'outreach', 'leads'}

org_block = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Litoral Prime Imóveis",
  "url": "https://praia.digital/",
  "logo": "https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/img/logo.png",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+55-11-95434-6288",
    "contactType": "sales",
    "areaServed": "BR",
    "availableLanguage": ["pt-BR", "en"]
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "opens": "09:00",
    "closes": "18:00"
  }
}
</script>
'''

updated = 0
skipped = 0
for path in root.rglob('*.html'):
    rel = path.relative_to(root)
    if any(part in exclude for part in rel.parts):
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'Organization' in text:
        continue
    marker = '</head>' if '</head>' in text else '<body>'
    if marker not in text:
        skipped += 1
        continue
    new_text = text.replace(marker, org_block + marker, 1)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        updated += 1

print('updated', updated, 'skipped', skipped)
