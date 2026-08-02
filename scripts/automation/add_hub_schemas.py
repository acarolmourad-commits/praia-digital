from pathlib import Path
import re

root = Path('.')

targets = [
    'index.html',
    'servicos.html',
    'imoveis.html',
    'cases.html',
    'blog/index.html',
    'litoral-prime-imoveis/imoveis.html',
]

websites = {
    'index.html': 'https://praia.digital/',
    'servicos.html': 'https://acarolmourad.github.io/praia-digital/servicos.html',
    'imoveis.html': 'https://acarolmourad.github.io/praia-digital/imoveis.html',
    'cases.html': 'https://acarolmourad.github.io/praia-digital/cases.html',
    'blog/index.html': 'https://acarolmourad.github.io/praia-digital/blog/index.html',
    'litoral-prime-imoveis/imoveis.html': 'https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/imoveis.html',
}

organizations = [
    'index.html',
    'servicos.html',
    'imoveis.html',
    'cases.html',
    'blog/index.html',
]

for rel in targets:
    path = root / rel
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'WebSite' not in text and rel in websites:
        url = websites[rel]
        block = '<script type="application/ld+json">\n'
        block += '{\n'
        block += '  "@context": "https://schema.org",\n'
        block += '  "@type": "WebSite",\n'
        block += f'  "url": "{url}",\n'
        block += '  "potentialAction": {\n'
        block += '    "@type": "SearchAction",\n'
        block += f'    "target": "{url}?search={{search_term_string}}",\n'
        block += '    "query-input": "required name=search_term_string"\n'
        block += '  }\n'
        block += '}\n'
        block += '</script>\n'
        new_text = text.replace('</head>', block + '</head>', 1)
        if new_text != text:
            path.write_text(new_text, encoding='utf-8')
            print('added WebSite', rel)
        else:
            print('skip WebSite', rel)

for rel in organizations:
    path = root / rel
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'Organization' not in text:
        block = '<script type="application/ld+json">\n'
        block += '{\n'
        block += '  "@context": "https://schema.org",\n'
        block += '  "@type": "Organization",\n'
        block += '  "name": "Litoral Prime Imóveis",\n'
        block += '  "url": "https://praia.digital/",\n'
        block += '  "logo": "https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/img/logo.png",\n'
        block += '  "contactPoint": {\n'
        block += '    "@type": "ContactPoint",\n'
        block += '    "telephone": "+55-11-95434-6288",\n'
        block += '    "contactType": "sales",\n'
        block += '    "areaServed": "BR",\n'
        block += '    "availableLanguage": ["pt-BR", "en"]\n'
        block += '  }\n'
        block += '}\n'
        block += '</script>\n'
        new_text = text.replace('</head>', block + '</head>', 1)
        if new_text != text:
            path.write_text(new_text, encoding='utf-8')
            print('added Organization', rel)
        else:
            print('skip Organization', rel)
