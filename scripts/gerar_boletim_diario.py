#!/usr/bin/env python3
"""Render only explicitly reviewed editions. No scraping, invented metrics or clock-based freshness."""
import argparse
import html
import json
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://praia.digital'
PATH = '/docs/inteligencia/'

def esc(value):
    return html.escape(str(value), quote=True)

def stamp(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('Timestamp requires timezone')
    return result

def validate(edition, as_of=None):
    if edition['status'] != 'reviewed' or not edition['reviewer'].strip():
        raise ValueError('Only reviewed editions may be published')
    datetime.strptime(edition['date'], '%Y-%m-%d')
    reviewed = stamp(edition['reviewed_at'])
    if reviewed > (as_of or datetime.now(timezone.utc)):
        raise ValueError('Future editorial review is not publishable')
    if reviewed.date().isoformat() != edition['date']:
        raise ValueError('Edition date must match editorial review date')
    if not edition['summary'].strip():
        raise ValueError('Missing editorial summary')
    seen = set()
    for item in edition['items']:
        for key in ['id', 'title', 'summary', 'source_name', 'source_url', 'published_at', 'checked_at', 'category', 'city', 'impact', 'reviewer']:
            if not item.get(key):
                raise ValueError('Missing item field: ' + key)
        if item.get('status') != 'reviewed':
            raise ValueError('Unreviewed news item')
        url = urlparse(item['source_url'])
        if url.scheme != 'https' or not url.netloc or url.username or url.password:
            raise ValueError('Source must use HTTPS')
        published = datetime.strptime(item['published_at'], '%Y-%m-%d').date()
        checked = stamp(item['checked_at'])
        if published > checked.date() or checked > reviewed:
            raise ValueError('Invalid source timeline')
        if item['source_url'] in seen:
            raise ValueError('Duplicate source URL')
        seen.add(item['source_url'])
    return edition

def page(root, title, path, body, description):
    header = (root / 'partials/header.html').read_text(encoding='utf-8')
    schema = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': title, 'url': BASE + path, 'inLanguage': 'pt-BR', 'description': description}
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Praia Digital</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}/img/default-home.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="Boletim Praia Digital" href="{PATH}feed.xml"><link rel="stylesheet" href="/assets/css/pd-navigation.css?v=3"><link rel="stylesheet" href="/assets/css/boletim.css"><script defer src="/js/pd-navigation.js?v=3"></script><script defer src="/js/boletim.js"></script>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')}</script></head><body><a class="bulletin-skip" href="#main">Pular para o conteúdo</a>{header}
<main id="main" class="bulletin-wrap">{body}</main><footer class="bulletin-footer"><div class="bulletin-wrap">Praia Digital · Inteligência com fontes e contexto.<br><a href="/politica-de-privacidade.html">Privacidade</a> · <a href="/interesse.html">Contato e correções</a></div></footer></body></html>'''

def render_edition(root, edition, path):
    cards = ''
    for item in edition['items']:
        cards += f'''<article class="bulletin-card news-item" data-city="{esc(item['city'])}" data-category="{esc(item['category'])}"><p class="eyebrow">{esc(item['category'])} · {esc(item['city'])}</p><h2>{esc(item['title'])}</h2><p>{esc(item['summary'])}</p><p><strong>Por que importa — análise editorial:</strong> {esc(item['impact'])}</p><p class="metadata">Publicado pela fonte: <time datetime="{esc(item['published_at'])}">{esc(item['published_at'])}</time><br>Conferido: <time datetime="{esc(item['checked_at'])}">{esc(item['checked_at'])}</time></p><a href="{esc(item['source_url'])}" rel="noopener">Ler na fonte: {esc(item['source_name'])}</a></article>'''
    if not cards:
        cards = '<div class="bulletin-card"><h2>Nenhuma notícia nova aprovada nesta edição</h2><p>Não substituímos a ausência de informação verificada por manchetes automáticas. Consulte as fontes oficiais abaixo; o radar é uma ferramenta de triagem, não uma notícia.</p></div>'
    cities = sorted({i['city'] for i in edition['items']})
    categories = sorted({i['category'] for i in edition['items']})
    filters = ''.join(f'<label>{label}<select id="filter-{key}"><option value="">Todos</option>' + ''.join(f'<option>{esc(v)}</option>' for v in values) + '</select></label>' for key, label, values in [('city', 'Cidade / região', cities), ('category', 'Tema', categories)])
    sources = '<li><a href="https://news.airbnb.com/">Airbnb Newsroom</a></li><li><a href="https://partner.booking.com/en-us">Booking Partner Hub</a></li><li><a href="https://www.bcb.gov.br/">Banco Central</a></li><li><a href="https://www.ibge.gov.br/">IBGE</a></li><li><a href="https://www.agenciasp.sp.gov.br/">Agência SP</a></li>'
    body = f'''<p class="eyebrow">Litoral paulista · Edição {esc(edition['date'])}</p><h1>Boletim de Inteligência</h1><p class="lead">O que mudou, por que importa e onde conferir.</p>
<div class="bulletin-status"><strong>Piloto editorial — sem promessa de tempo real.</strong><p>Última revisão desta edição: <time datetime="{esc(edition['reviewed_at'])}">{esc(edition['reviewed_at'])}</time>. Responsável pela revisão: {esc(edition['reviewer'])}.</p><p>Publicação de novas edições depende de revisão. A data não muda só porque você abriu a página.</p></div>
<nav class="bulletin-actions" aria-label="Acompanhar boletim"><a class="bulletin-button" href="{PATH}feed.xml">Acompanhar por RSS — grátis</a><a href="{PATH}arquivo-boletins.html">Edições anteriores</a><a href="/newsletter/assinatura.html">Status da assinatura por e-mail</a></nav>
<section class="bulletin-card"><h2>Nesta edição</h2><p>{esc(edition['summary'])}</p></section>
<div class="bulletin-filters" hidden>{filters}<p id="filter-status" role="status" aria-live="polite"></p></div><section aria-label="Notícias verificadas" id="news">{cards}</section><p id="filter-empty" hidden>Nenhuma notícia desta edição corresponde aos filtros. Escolha “Todos” para ver as demais.</p>
<section class="bulletin-card"><h2>Radar de fontes</h2><p>A coleta automática prepara candidatos para revisão; não publica notícias sozinha. A <a href="/blog/novidades-airbnb-booking.html">Sentinela Airbnb + Booking</a> é um monitor separado. Alteração de página não comprova novidade e fontes podem estar indisponíveis.</p><ul>{sources}</ul><p>Links de consulta não significam que todas as fontes foram verificadas hoje.</p></section>
<section class="bulletin-card" id="metodologia"><h2>Como trabalhamos</h2><p>Notícias aprovadas trazem fonte primária, data da publicação, horário de conferência, região e contexto. A análise é identificada e não é recomendação individual de investimento. Não usamos quantidade de artigos do nosso site como procura imobiliária, preço ou valorização.</p><p>Estimativas financeiras só serão publicadas com hipóteses, custos, período e método verificáveis. Os indicadores inválidos do modelo anterior foram retirados; o histórico legado está identificado no arquivo.</p><p>O conteúdo é público e gratuito. Não há envio automático de e-mail ativo neste piloto. Nenhum cadastro é solicitado enquanto confirmação e descadastro não estiverem funcionando.</p><a href="/interesse.html">Sugerir pauta ou comunicar uma correção</a></section>'''
    return page(root, 'Boletim de Inteligência', path, body, 'Notícias verificadas e contexto para o litoral paulista. Fontes, datas reais, arquivo e RSS gratuito.')

def build(root=ROOT):
    editions = [validate(json.loads(p.read_text(encoding='utf-8'))) for p in sorted((root / 'data/boletim/edicoes').glob('*.json'))]
    if not editions:
        raise ValueError('At least one reviewed edition is required')
    if len({e['date'] for e in editions}) != len(editions):
        raise ValueError('Duplicate edition date')
    editions.sort(key=lambda e: e['date'])
    out = root / 'docs/inteligencia'
    for edition in editions:
        path = PATH + 'boletim-' + edition['date'] + '.html'
        (root / path.lstrip('/')).write_text(render_edition(root, edition, path), encoding='utf-8')
    (out / 'boletim-diario.html').write_text(render_edition(root, editions[-1], PATH + 'boletim-diario.html'), encoding='utf-8')
    rows = ''.join(f'<li><a href="boletim-{e["date"]}.html">{e["date"]}</a> — {len(e["items"])} notícia(s) verificada(s)</li>' for e in reversed(editions))
    body = f'<p class="eyebrow">Memória editorial</p><h1>Arquivo de boletins</h1><p>Edições efetivamente publicadas, sem reconstrução artificial de dias sem boletim.</p><ul>{rows}</ul><h2>Registro legado</h2><p><a href="boletim-2026-07-17.html">17/07/2026 — modelo antigo, não usar como indicador de mercado</a>. Não há arquivo diário completo do período anterior.</p><p><a href="boletim-diario.html">Voltar ao boletim</a> · <a href="feed.xml">RSS gratuito</a></p>'
    (out / 'arquivo-boletins.html').write_text(page(root, 'Arquivo de boletins', PATH + 'arquivo-boletins.html', body, 'Edições revisadas e registros históricos identificados do Boletim Praia Digital.'), encoding='utf-8')
    rss = ET.Element('rss', version='2.0'); channel = ET.SubElement(rss, 'channel')
    for key, val in [('title', 'Boletim Praia Digital'), ('link', BASE + PATH + 'boletim-diario.html'), ('description', 'Edições revisadas, fontes e contexto. Sem promessa de publicação em tempo real.'), ('language', 'pt-BR'), ('lastBuildDate', format_datetime(stamp(editions[-1]['reviewed_at'])))]:
        ET.SubElement(channel, key).text = val
    for e in reversed(editions):
        item = ET.SubElement(channel, 'item'); url = BASE + PATH + 'boletim-' + e['date'] + '.html'
        for key, val in [('title', 'Boletim Praia Digital — ' + e['date']), ('link', url), ('guid', url), ('pubDate', format_datetime(stamp(e['reviewed_at']))), ('description', e['summary'])]:
            ET.SubElement(item, key).text = val
    ET.indent(rss)
    ET.ElementTree(rss).write(out / 'feed.xml', encoding='utf-8', xml_declaration=True)
    sitemap = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for edition in editions:
        entry = ET.SubElement(sitemap, 'url')
        ET.SubElement(entry, 'loc').text = BASE + PATH + 'boletim-' + edition['date'] + '.html'
        ET.SubElement(entry, 'lastmod').text = edition['reviewed_at']
    ET.indent(sitemap)
    ET.ElementTree(sitemap).write(root / 'sitemap-boletim.xml', encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--root', type=Path, default=ROOT)
    build(parser.parse_args().root)
