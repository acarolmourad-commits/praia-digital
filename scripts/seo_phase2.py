#!/usr/bin/env python3
# Fase 2/3 — Auditoria SEO praia.digital (2026-09-24)
# 1) Limpa sitemap.xml: remove URLs junk, duplicatas canonicalizadas e archives
# 2) Garante modulo v3.1 no js/shared.js: canonical das cidades duplicadas da raiz
# 3) Garante URLs estrategicas (paginas-pilar novas) presentes no sitemap
import re, sys, datetime

SM = 'sitemap.xml'
SHARED = 'js/shared.js'

EXTRA_URLS = [
    'https://praia.digital/servicos/edicao-anuncios-airbnb-booking.html',
    'https://praia.digital/guias/aluguel-temporada-airbnb-litoral-sp.html',
]

JUNK = re.compile(r'(_archive|\-print\-|proposta|propostas|dashboard|form-tracker|top5-leads|cadastrar|campaigns|onboarding|subscription|templates|kit-vendas|acompanhamento-prospeccao|central-comando|mapa-inteligente|obrigado|newsletter|/leads?/)', re.I)
CITY_DUP = re.compile(r'https://praia\.digital/(santos|guaruja|praia-grande|bertioga|sao-vicente|itanhaem|mongagua|peruibe)\.html')
LANDING_DUP = re.compile(r'landing-parcerias-(anuncios|captura-praia-digital-2026|captura-praia-digital-conversao-2026|conversao-praia-digital-2026|imobiliarias-litoral|proprietarios-luxo)\.html')

def keep(url):
    if JUNK.search(url): return False
    if url.endswith('/vendas.html'): return False
    if '/academy/' in url: return False
    if CITY_DUP.search(url): return False
    if LANDING_DUP.search(url): return False
    return True

xml = open(SM, encoding='utf-8').read()
entries = re.findall(r'<url>.*?</url>', xml, re.S)
kept = [e for e in entries if keep(re.search(r'<loc>(.*?)</loc>', e).group(1))]
removed = len(entries) - len(kept)
today = datetime.date.today().isoformat()
existing = set(re.search(r'<loc>(.*?)</loc>', e).group(1) for e in kept)
for u in EXTRA_URLS:
    if u not in existing:
        kept.append(f'<url><loc>{u}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>')
        print(f'sitemap: adicionada URL estrategica {u}')
out = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(kept) + '\n</urlset>\n'
open(SM, 'w', encoding='utf-8').write(out)
print(f'sitemap: {len(entries)} -> {len(kept)} URLs ({removed} removidas)')

MODULE = '''
/* ===== Praia Digital — SEO Module v3.1: canonical de cidades duplicadas (2026-09-24) ===== */
(function () {
  'use strict';
  var m = location.pathname.match(/^\/(santos|guaruja|praia-grande|bertioga|sao-vicente|itanhaem|mongagua|peruibe)\.html$/);
  if (!m) return;
  var canon = 'https://praia.digital/cidades/' + m[1] + '.html';
  var links = document.head.querySelectorAll('link[rel="canonical"]');
  if (links.length) { links[0].href = canon; }
  else {
    var l = document.createElement('link');
    l.rel = 'canonical'; l.href = canon;
    document.head.appendChild(l);
  }
})();
'''
s = open(SHARED, encoding='utf-8').read()
if 'SEO Module v3.1' not in s:
    open(SHARED, 'w', encoding='utf-8').write(s + MODULE)
    print('shared.js: modulo v3.1 adicionado')
else:
    print('shared.js: modulo v3.1 ja presente')
