from pathlib import Path
import re

root = Path('.')
pages = [
    'index.html',
    'servicos.html',
    'imoveis.html',
    'cases.html',
    'blog/index.html',
    'litoral-prime-imoveis/index.html',
    'litoral-prime-imoveis/imoveis.html',
]

utm = 'utm_source=site&utm_medium=whatsapp&utm_campaign=geral'

updated = 0
for rel in pages:
    path = root / rel
    text = path.read_text(encoding='utf-8', errors='ignore')
    # add UTM to main wa.me links, skip agent numbers
    def add_utm(m):
        url = m.group(1)
        if '551399999999' in url:
            return m.group(0)
        if '?' in url:
            return url + '&' + utm
        else:
            return url + '?' + utm
    new_text = re.sub(r'(https://wa\.me/5511954346288)(\?[^"\']*)?', add_utm, text)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('updated', rel)
        updated += 1
    else:
        print('skip', rel)

print('updated', updated, 'pages')
