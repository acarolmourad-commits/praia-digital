from pathlib import Path
import re

root = Path('imoveis')

# Mapping of PNG to WebP for local images in img/
image_map = {
    'img/santos-apartamento-vista-mar.png': 'img/santos-apartamento-vista-mar.webp',
    'img/pg-studio-moderno.png': 'img/pg-studio-moderno.webp',
    'img/gua-casa-duplex.png': 'img/gua-casa-duplex.webp',
    'img/sv-cobertura-duplex.png': 'img/sv-cobertura-duplex.webp',
    'img/it-casa-terrea.png': 'img/it-casa-terrea.webp',
    'img/mon-ap-compacto.png': 'img/mon-ap-compacto.webp',
    'img/per-sobrado.png': 'img/per-sobrado.webp',
    'img/berta-alto-padrao.png': 'img/berta-alto-padrao.webp',
    'img/santos-cobertura-duplex.png': 'img/santos-cobertura-duplex.webp',
    'img/guaruja-sobrado.png': 'img/guaruja-sobrado.webp',
    'img/pg-studio.png': 'img/pg-studio.webp',
    'img/peruibe-chacara.png': 'img/peruibe-chacara.webp',
    'img/mongagua-apartamento.png': 'img/mongagua-apartamento.webp',
    'img/santos-terreno-alto-padrao.png': 'img/santos-terreno-alto-padrao.webp',
    'img/itanhaem-terreno.png': 'img/itanhaem-terreno.webp',
    'img/bertioga-apartamento.png': 'img/bertioga-apartamento.webp',
}

updated = 0
for path in root.rglob('*.html'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    new_text = text
    
    for png, webp in image_map.items():
        if png not in new_text:
            continue
        # Replace <img src="png" ...> with <picture><source srcset="webp" type="image/webp"><img src="png" ...>
        pattern = re.compile(r'(<img[^>]+src="' + re.escape(png) + r'"[^>]*>)')
        replacement = '<picture><source srcset="' + webp + '" type="image/webp">' + r'\1</picture>'
        new_text = pattern.sub(replacement, new_text, count=1)
    
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('updated', path.relative_to(root))
        updated += 1

print('updated', updated, 'pages')
