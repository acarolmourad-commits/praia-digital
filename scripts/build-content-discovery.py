#!/usr/bin/env python3
"""Build a searchable, crawlable directory from the site's approved public sitemaps.

No filesystem-wide publication: aliases, retired pages, robots exclusions and
noindex content stay out. Run before build-navigation.py in the Pages artifact.
"""
import argparse
import html
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_sitemap_targets import (blocked_by_robots, canonical_sitemap_path,
    excluded_path, indexing_exclusions, robots_rules)
from enforce_listing_retirements import retired_page, retired_slugs

ROOT = Path(__file__).resolve().parents[1]
PAGE_SIZE = 100
FEATURED = [
    ('/guias/ficha-comparacao-bairros-litoral.html', 'Comparar bairros', 'Uma ficha de visita para comparar endereços com os mesmos critérios.'),
    ('/guias/auditoria-fotos-descricao-temporada.html', 'Revisar seu anúncio', 'Confira se fotos, texto e comodidades contam a mesma história.'),
    ('/guias/conferencia-calendarios-temporada.html', 'Organizar a disponibilidade', 'Um roteiro para conferir reservas, bloqueios e calendários por imóvel.'),
    ('/blog/simulado-tti-questoes-gabarito-comentado.html', 'Estudar para o TTI', 'Questões autorais com respostas comentadas para praticar.'),
]

def normalize(value):
    return ''.join(c for c in unicodedata.normalize('NFD', value.casefold()) if unicodedata.category(c) != 'Mn')

def visitor_excluded(rel):
    """The legacy XML sitemap also lists operations; don't promote those to visitors.

    This controls discovery only. It does not change access or indexing intent.
    Public intelligence/newsletters and top-level editorial guides stay eligible.
    """
    if rel.startswith('docs/'):
        return not (rel.startswith(('docs/inteligencia/', 'docs/newsletter/')) or
                    (rel.startswith('docs/guia-') and rel.count('/') == 1))
    return (rel.startswith(('dashboard-', 'proposta-piloto-')) or rel in {
        'acoes-hoje.html', 'acompanhamento-prospeccao.html',
        'central-comando-praia-digital.html', 'form-tracker.html',
        'top5-leads-hoje.html', 'parcerias-imobiliarias-litoral-obrigado.html'})

def category(path):
    first = path.lstrip('/').split('/')[0]
    if first == 'blog': return 'Artigos'
    if first in ('cidades', 'cidades-expansao', 'bairros'): return 'Cidades e bairros'
    if first in ('apps', 'ferramentas', 'ferramentas-gratuitas', 'calculadoras'): return 'Ferramentas'
    if first in ('guias', 'checklists', 'proprietarios', 'anfitrioes'): return 'Guias e checklists'
    if first == 'imoveis' or first == 'imoveis.html': return 'Imóveis'
    if first == 'education': return 'Academy'
    if path.startswith('/docs/guia-'): return 'Guias e checklists'
    if first in ('docs', 'noticias', 'newsletter', 'conteudo-periodico'): return 'Boletins e notícias'
    if first in ('servicos', 'solucoes', 'profissionais', 'produtos') or first.startswith('servico'): return 'Serviços e soluções'
    return 'Outras páginas'

def clean(value):
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', value)).split()).strip(' >')

def collect(root):
    rules, retired = robots_rules(root), retired_slugs()
    urls = set()
    for sitemap in sorted(root.glob('sitemap*.xml')):
        for node in ET.parse(sitemap).iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            urls.add(node.text or '')
    entries, skipped, seen = [], [], set()
    for url in sorted(urls):
        parts = urlsplit(url)
        rel = unquote(parts.path).lstrip('/')
        if parts.scheme != 'https' or parts.netloc != 'praia.digital' or parts.query or parts.fragment:
            skipped.append(url); continue
        if rel == 'sitemap.html' or rel.startswith('explorar/'):
            continue
        if visitor_excluded(rel):
            skipped.append(url); continue
        path = root / rel
        if path.is_dir(): path /= 'index.html'
        if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError('Missing or unsafe sitemap target: ' + url)
        file_rel = path.relative_to(root).as_posix()
        if (excluded_path(file_rel) or blocked_by_robots(parts.path, rules)
                or retired_page(path, retired) or indexing_exclusions(path)):
            skipped.append(url); continue
        canonical = canonical_sitemap_path(path, root)
        if canonical is None or canonical != rel:
            skipped.append(url); continue
        if path.resolve() in seen: continue
        seen.add(path.resolve())
        text = path.read_text(encoding='utf-8')
        title = re.search(r'<title\b[^>]*>(.*?)</title>', text, re.I | re.S)
        title = clean(title[1]) if title else file_rel
        title = re.sub(r'\s*[|—–-]\s*Praia Digital\s*$', '', title, flags=re.I)
        if not title: title = file_rel
        entries.append({'url': parts.path, 'title': title, 'category': category(parts.path)})
    entries.sort(key=lambda entry: (normalize(entry['title']), entry['url']))
    return entries, skipped

def page_url(number):
    return '/sitemap.html' if number == 1 else f'/explorar/pagina-{number}.html'

def render(entries, number, total):
    e = html.escape
    url = page_url(number)
    title = 'Buscar no site e mapa de conteúdos' if number == 1 else f'Mapa de conteúdos — página {number}'
    categories = sorted({entry['category'] for entry in entries})
    options = ''.join(f'<option>{e(name)}</option>' for name in categories)
    cards = ''.join(f'<article><h3><a href="{link}">{e(label)}</a></h3><p>{e(desc)}</p></article>' for link,label,desc in FEATURED)
    subset = entries[(number-1)*PAGE_SIZE:number*PAGE_SIZE]
    links = '\n'.join(f'<li><a href="{e(item["url"])}">{e(item["title"])}</a><span>{e(item["category"])}</span></li>' for item in subset)
    pages = ' '.join(f'<a href="{page_url(i)}"'+(' aria-current="page"' if i == number else '')+f' aria-label="Página {i}">{i}</a>' for i in range(1, total+1))
    previous = f'<a href="{page_url(number-1)}">← Página anterior</a>' if number > 1 else ''
    following = f'<a href="{page_url(number+1)}">Próxima página →</a>' if number < total else ''
    schema = json.dumps({'@context':'https://schema.org','@type':'CollectionPage','name':title,'url':'https://praia.digital'+url},ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | Praia Digital</title>
<meta name="description" content="Encontre artigos, cidades, bairros, imóveis, guias e ferramentas da Praia Digital. Busque por assunto ou explore o diretório de páginas públicas.">
<meta name="robots" content="{'index' if number == 1 else 'noindex'}, follow">
<link rel="canonical" href="https://praia.digital{url}">
<link rel="stylesheet" href="/css/content-discovery.css">
<script type="application/ld+json">{schema}</script>
<script defer src="/js/content-discovery.js"></script></head>
<body class="pd-discovery"><a class="skip-link" href="#conteudo">Pular para o conteúdo</a><meta name="pd-shared-nav">
<main id="conteudo"><nav class="breadcrumbs" aria-label="Caminho da página"><a href="/">Início</a> / <a href="/sitemap.html">Explorar conteúdos</a></nav>
<p class="eyebrow">PRAIA DIGITAL · EXPLORE POR ASSUNTO</p><h1>{e(title)}</h1>
<p class="intro">Uma busca para conectar sua dúvida ao próximo passo. Encontre guias, ferramentas, cidades e artigos em um só lugar.</p>
<form id="content-search" role="search" action="/sitemap.html" method="get">
<div><label for="content-query">O que você procura?</label><input id="content-query" name="q" type="search" maxlength="200" placeholder="Ex.: Bertioga, anúncio Airbnb, simulado TTI"></div>
<div><label for="content-category">Tipo de conteúdo</label><select id="content-category" name="categoria"><option value="">Todos os tipos</option>{options}</select></div>
<button type="submit">Buscar</button><button id="content-clear" type="button" hidden>Limpar busca</button></form>
<p id="search-status" role="status" aria-live="polite">{format(len(entries), ",").replace(",", ".")} páginas no diretório. Explore as listas abaixo ou use a busca.</p>
<div id="search-results" hidden><h2 tabindex="-1" id="results-heading">Resultados da busca</h2><ul id="results-list" class="directory-list"></ul><button type="button" id="load-more" hidden>Mostrar mais resultados</button></div>
<noscript><p>A busca por palavra precisa de JavaScript. Todos os links continuam disponíveis nas páginas numeradas do diretório abaixo.</p></noscript>
<section aria-labelledby="start-here"><h2 id="start-here">Por onde começar?</h2><div class="journey-grid">{cards}</div>
<p class="hub-links"><a href="/cidades/index.html">Cidades</a><a href="/bairros/index.html">Bairros</a><a href="/apps/">Apps gratuitos</a><a href="/ferramentas/index.html">Ferramentas</a><a href="/blog/index.html">Blog</a><a href="/servicos.html">Serviços</a></p></section>
<section id="directory" aria-labelledby="directory-title"><h2 id="directory-title">Diretório de A a Z</h2><p>Página {number} de {total} · {len(subset)} links nesta página. Os conteúdos têm datas e escopos próprios; confira as fontes de cada página.</p>
<ul class="directory-list">{links}</ul><nav class="page-neighbors" aria-label="Continuar no diretório">{previous}{following}</nav>
<details><summary>Ir para uma página do diretório</summary><nav class="page-numbers" aria-label="Páginas do diretório">{pages}</nav></details></section>
</main><footer><a href="/">Praia Digital</a> · <a href="/contato.html">Contato</a> · <a href="/politica-de-privacidade.html">Privacidade</a> · <a href="/metodologia.html">Fontes e metodologia</a></footer></body></html>
'''

def build(root):
    entries, skipped = collect(root)
    if not entries: raise ValueError('Refusing to publish an empty directory')
    total = (len(entries)+PAGE_SIZE-1)//PAGE_SIZE
    (root/'explorar').mkdir(exist_ok=True)
    (root/'data').mkdir(exist_ok=True)
    (root/'data/content-search.json').write_text(json.dumps(entries,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    expected = set()
    for number in range(1,total+1):
        path = root/page_url(number).lstrip('/')
        path.write_text(render(entries,number,total),encoding='utf-8')
        expected.add(path)
    for path in (root/'explorar').glob('pagina-*.html'):
        if re.fullmatch(r'pagina-\d+\.html',path.name) and path not in expected: path.unlink()
    return {'entries':len(entries),'pages':total,'excluded':len(skipped)}

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    args=parser.parse_args()
    print(json.dumps(build(args.root.resolve()),ensure_ascii=False))
