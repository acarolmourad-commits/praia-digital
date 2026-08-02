from pathlib import Path
from PIL import Image

root = Path('.')
img_root = root / 'img'
img_root.mkdir(exist_ok=True)

source_images = [
    img_root / 'santos-apartamento-vista-mar.png',
    img_root / 'pg-studio-moderno.png',
    img_root / 'gua-casa-duplex.png',
    img_root / 'sv-cobertura-duplex.png',
    img_root / 'it-casa-terrea.png',
    img_root / 'mon-ap-compacto.png',
    img_root / 'per-sobrado.png',
    img_root / 'berta-alto-padrao.png',
]

generated = 0
for src in source_images:
    if not src.exists():
        print('missing', src)
        continue
    dst = src.with_suffix('.webp')
    if dst.exists():
        print('exists', dst)
        continue
    try:
        im = Image.open(src).convert('RGB')
        im.save(dst, 'WEBP', quality=85)
        generated += 1
        print('generated', dst)
    except Exception as e:
        print('error', src, e)

print('generated', generated)
