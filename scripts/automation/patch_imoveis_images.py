#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch em massa nas landings de imoveis: injeta imagem padrão onde faltar.
Também ajusta og:image e twitter:image para default-home.jpg.
"""
import os
import re

BASE = r'C:/Users/Carolina/praia-digital'
DIR = os.path.join(BASE, 'imoveis')
DEFAULT = 'https://praia.digital/img/default-home.jpg'
DEFAULT_WEBP = 'https://praia.digital/img/default-home.jpg.webp'

def process(path):
    txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
    slug = os.path.splitext(os.path.basename(path))[0]
    original = txt
    has_img = bool(re.search(r'<img[^>]+src="([^"]+)"', txt, re.I))
    # Determine if any image src points to an existing local file
    local_exists = False
    if has_img:
        for m in re.finditer(r'<img[^>]+src="([^"]+)"', txt, re.I):
            src = m.group(1)
            if src.startswith('http') or src.startswith('data:'):
                continue
            if os.path.exists(os.path.join(BASE, src)):
                local_exists = True
                break
    if not has_img or not local_exists:
        # Remove empty <picture> blocks without img/source
        txt = re.sub(r'<picture>\s*</picture>', '', txt, flags=re.I)
        # Inject default picture after h1
        injection = f'<picture><source srcset="{DEFAULT_WEBP}" type="image/webp"><img src="{DEFAULT}" alt="{slug}" loading="lazy" width="800" height="600" decoding="async"></picture>'
        txt = txt.replace('<h1>', f'<h1>{injection}', 1)
        # Update og:image and twitter:image to default
        txt = re.sub(r'(<meta\s+property="og:image"\s+content=")([^"]+)(")', r'\1' + DEFAULT + r'\3', txt, flags=re.I)
        txt = re.sub(r'(<meta\s+name="twitter:image"\s+content=")([^"]+)(")', r'\1' + DEFAULT + r'\3', txt, flags=re.I)
    if txt != original:
        open(path, 'w', encoding='utf-8').write(txt)
        return True
    return False

def main():
    files = [os.path.join(DIR, f) for f in os.listdir(DIR) if f.endswith('.html')]
    patched = 0
    for path in files:
        if process(path):
            patched += 1
    print('IMOVEIS_IMAGES_PATCHED', patched)

if __name__ == '__main__':
    main()
