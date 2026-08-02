from pathlib import Path
path = Path('litoral-prime-imoveis/index.html')
text = path.read_text(encoding='utf-8', errors='ignore')
if 'Organization' not in text:
    block = '''<script type="application/ld+json">
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
  }
}
</script>
'''
    new_text = text.replace('</head>', block + '</head>', 1)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('added Organization to litoral-prime-imoveis/index.html')
    else:
        print('skip')
else:
    print('already has Organization')
