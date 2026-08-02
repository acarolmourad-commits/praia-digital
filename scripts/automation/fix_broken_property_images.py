from pathlib import Path
import re

root = Path('imoveis')

broken = [
    'img/bertioga-apartamento.png',
    'img/guaruja-sobrado.png',
    'img/itanhaem-terreno.png',
    'img/mongagua-apartamento.png',
    'img/peruibe-chacara.png',
    'img/pg-studio.png',
    'img/santos-cobertura-duplex.png',
    'img/santos-terreno-alto-padrao.png',
]

replacement = '<div class="property-media" style="background:#e2e8f0;height:280px;border-radius:12px;display:flex;align-items:center;justify-content:center;color:#64748b;font-size:0.9rem">Imagem indisponível</div>'

updated = 0
for path in root.rglob('*.html'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    new_text = text
    changed = False
    for b in broken:
        pattern = re.compile(r'<img[^>]*src="' + re.escape(b) + r'"[^>]*>')
        if pattern.search(new_text):
            new_text = pattern.sub(replacement, new_text, count=1)
            changed = True
    if changed:
        path.write_text(new_text, encoding='utf-8')
        print('updated', path.relative_to(root))
        updated += 1

print('updated', updated, 'pages')
