from pathlib import Path

img_map = {
    'santos': 'img/santos-apartamento-vista-mar.webp',
    'guaruja': 'img/gua-casa-duplex.webp',
    'praia-grande': 'img/pg-studio-moderno.webp',
    'bertioga': 'img/berta-alto-padrao.webp',
    'itanhaem': 'img/it-casa-terrea.webp',
    'mongagua': 'img/mon-ap-compacto.webp',
    'sao-vicente': 'img/sv-cobertura-duplex.webp',
    'peruibe': 'img/per-sobrado.webp',
    'caraguatatuba': 'img/default-home.jpg',
    'ilhabela': 'img/default-home.jpg',
    'sao-sebastiao': 'img/default-home.jpg',
    'ubatuba': 'img/default-home.jpg',
}

base = Path('bairros')
for p in sorted(base.glob('*/index.html')):
    city = p.parent.name
    img = img_map.get(city)
    if not img:
        continue

    txt = p.read_text(encoding='utf-8', errors='ignore')

    # Check if image already present
    if img in txt:
        print(f'skip {p}: image already present')
        continue

    # Add image after the first CTA section closing, before the highlight section
    marker = '<div class="highlight">'
    img_html = f'<img src="https://praia.digital/{img}" alt="{city}" style="max-width:100%;border-radius:12px;margin-top:18px;">\n\n      <div class="highlight">'
    txt = txt.replace(marker, img_html, 1)

    # Update OG image
    txt = txt.replace('content="https://praia.digital/img/default-home.jpg"', f'content="https://praia.digital/{img}"')

    p.write_text(txt, encoding='utf-8')
    print(f'updated {p} with {img}')

print('done')
