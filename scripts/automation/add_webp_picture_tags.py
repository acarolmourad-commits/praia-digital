from pathlib import Path
import re

root = Path('.')
pages = [
    'imoveis.html',
    'litoral-prime-imoveis/imoveis.html',
]

replacements = {
    'img/santos-apartamento-vista-mar.png': 'img/santos-apartamento-vista-mar.webp',
    'img/pg-studio-moderno.png': 'img/pg-studio-moderno.webp',
    'img/gua-casa-duplex.png': 'img/gua-casa-duplex.webp',
    'img/sv-cobertura-duplex.png': 'img/sv-cobertura-duplex.webp',
    'img/it-casa-terrea.png': 'img/it-casa-terrea.webp',
    'img/mon-ap-compacto.png': 'img/mon-ap-compacto.webp',
    'img/per-sobrado.png': 'img/per-sobrado.webp',
    'img/berta-alto-padrao.png': 'img/berta-alto-padrao.webp',
}

updated = 0
for rel in pages:
    path = root / rel
    text = path.read_text(encoding='utf-8', errors='ignore')
    new_text = text
    for png, webp in replacements.items():
        pattern = re.compile(
            r'(<div class="property-media"><img src="' + re.escape(png) + r'"[^>]+></div>)'
        )
        replacement = (
            '<div class="property-media"><picture><source srcset="' + webp + '" type="image/webp">'
            '<img src="' + png + '" alt='
        )
        # This is tricky; instead, rebuild from full img tag match
        def repl(m):
            tag = m.group(1)
            # insert picture wrapper around img
            return '<div class="property-media"><picture><source srcset="' + webp + '" type="image/webp">' + tag[len('<div class="property-media">'):-len('</div>')] + '</picture></div>'
        new_text = pattern.sub(repl, new_text, count=1)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('updated', rel)
        updated += 1
    else:
        print('skip', rel)

print('updated', updated, 'pages')
