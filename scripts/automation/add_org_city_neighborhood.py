from pathlib import Path
import re

root = Path('.')

pages = list(root.glob('cidades/*.html')) + list(root.glob('bairros/*.html'))

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
for path in pages:
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'Organization' in text and 'ContactPoint' in text and 'OpeningHoursSpecification' in text:
        continue
    marker = '</head>' if '</head>' in text else '<body>'
    new_text = text.replace(marker, org_block + marker, 1)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        updated += 1
        print('updated', path)
    else:
        print('no-insert', path)

print('updated', updated, 'of', len(pages))
