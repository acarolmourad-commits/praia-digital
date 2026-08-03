#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch em massa nos artigos de blog existentes para adicionar tags SEO faltantes.
Atualiza artigos que foram gerados pelo gerador antigo sem keywords/og/twitter/robots/schema.
"""
import os
import re
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BLOG_DIR = os.path.join(BASE, "blog")

def patch_article(path):
    txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
    if not re.search(r'<meta\s+name="keywords"', txt, re.I):
        return False
    slug = os.path.splitext(os.path.basename(path))[0]
    title_m = re.search(r'<title>\s*(.+?)\s*</title>', txt, re.I|re.S)
    title = title_m.group(1) if title_m else slug.replace('-', ' ').title()
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', txt, re.I)
    desc = desc_m.group(1) if desc_m else ''
    keywords = f'{title}, tema imobiliária, litoral paulista, Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente, Peruíbe, imóveis litoral, temporada, aluguel temporada'
    slug_safe = slug.replace("?", "").replace("&", "").replace("=", "").replace("%", "")
    head_additions = f'<meta name="keywords" content="{keywords}">\n<meta property="og:type" content="article">\n<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n<meta property="og:image" content="https://praia.digital/img/default-home.jpg">\n<meta property="og:url" content="https://praia.digital/blog/{slug_safe}.html">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="{title}">\n<meta name="twitter:description" content="{desc}">\n<meta name="twitter:image" content="https://praia.digital/img/default-home.jpg">\n<meta name="robots" content="index, follow">\n<script type="application/ld+json">\n{{\n  "@context": "https://schema.org",\n  "@type": "BlogPosting",\n  "headline": "{title}",\n  "description": "{desc}",\n  "url": "https://praia.digital/blog/{slug_safe}.html",\n  "author": {{"@type": "Organization", "name": "Litoral Prime Imóveis"}},\n  "publisher": {{"@type": "Organization", "name": "Litoral Prime Imóveis", "url": "https://praia.digital/"}}\n}}\n</script>\n<link rel="stylesheet" href="../css/style.css">\n'
    txt = txt.replace('</head>', head_additions + '</head>', 1)
    body_additions = '<header>\n  <nav aria-label="Navegação principal">\n    <div class="logo">\n      <h1>🏖️ Litoral Prime Imóveis</h1>\n      <p class="tagline">Conteúdo para o litoral paulista</p>\n    </div>\n    <ul class="nav-menu">\n      <li><a href="../index.html">Início</a></li>\n      <li><a href="../servicos.html">Serviços</a></li>\n      <li><a href="index.html">Blog</a></li>\n    </ul>\n  </nav>\n</header>\n<main id="main">\n  <article>\n'
    txt = txt.replace('<article>', body_additions, 1)
    cta = f'<p><a class="btn-whatsapp" href="https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20em%20{slug_safe.replace("-", "%20")}." target="_blank" rel="noopener">Fale com um especialista</a></p>\n'
    txt = txt.replace('</article>', '  </article>\n' + cta, 1)
    txt = txt.replace('</body>', '  </main>\n<footer aria-label="Rodapé">\n  <p>© Litoral Prime Imóveis • comercial@praia.digital • (11) 95434-6288</p>\n</footer>\n</body>\n', 1)
    open(path, 'w', encoding='utf-8').write(txt)
    return True

def main():
    files = [os.path.join(BLOG_DIR, f) for f in os.listdir(BLOG_DIR) if f.endswith('.html') and f != 'carrossel.html' and f != 'index.html']
    patched = 0
    for path in files:
        if patch_article(path):
            patched += 1
    print('BLOG_ARTICLES_PATCHED', patched)

if __name__ == '__main__':
    main()
