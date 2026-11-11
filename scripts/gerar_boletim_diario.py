#!/usr/bin/env python3
"""Render only explicitly reviewed editions. No scraping, invented metrics or clock-based freshness."""
import argparse
import html
import hashlib
import json
import re
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from zoneinfo import ZoneInfo
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

def human_date(value):
    if 'T' not in value:
        return datetime.strptime(value, '%Y-%m-%d').strftime('%d/%m/%Y')
    return stamp(value).astimezone(ZoneInfo('America/Sao_Paulo')).strftime('%d/%m/%Y às %Hh%M (Brasília)')

def time_tag(value):
    return f'<time datetime="{esc(value)}">{esc(human_date(value))}</time>'

def modified_at(edition):
    return max([edition['reviewed_at']] + [u['noted_at'] for item in edition['items'] for u in item.get('updates', [])], key=stamp)

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
    ids = set()
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
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', item['id']) or item['id'] in ids:
            raise ValueError('Invalid or duplicate item ID')
        ids.add(item['id'])
        if item.get('deadline'):
            if datetime.strptime(item['deadline'], '%Y-%m-%d').date() < published:
                raise ValueError('Deadline precedes publication')
        for update in item.get('updates', []):
            if not update.get('text', '').strip() or not update.get('reviewer', '').strip():
                raise ValueError('Editorial update requires text and reviewer')
            noted = stamp(update['noted_at'])
            if noted < reviewed or noted > (as_of or datetime.now(timezone.utc)):
                raise ValueError('Invalid editorial update timeline')
    for note in edition.get('notes', []):
        if not note.get('title', '').strip() or not note.get('text', '').strip():
            raise ValueError('Editorial note needs a title and text')
        url = urlparse(note.get('source_url', ''))
        if url.scheme != 'https' or not url.netloc or url.username or url.password:
            raise ValueError('Editorial note source must use HTTPS')
        datetime.strptime(note['related_edition'], '%Y-%m-%d')
    return edition

def page(root, title, path, body, description, edition=None):
    header = (root / 'partials/header.html').read_text(encoding='utf-8')
    css_version = hashlib.sha256((root / 'assets/css/boletim.css').read_bytes()).hexdigest()[:12]
    js_version = hashlib.sha256((root / 'js/boletim.js').read_bytes()).hexdigest()[:12]
    schema = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': title, 'url': BASE + path, 'inLanguage': 'pt-BR', 'description': description}
    if edition:
        schema.update(datePublished=edition['reviewed_at'], dateModified=modified_at(edition))
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Praia Digital</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}/img/default-home.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="Boletim Praia Digital" href="{PATH}feed.xml"><link rel="stylesheet" href="/assets/css/pd-navigation.css?v=3"><link rel="stylesheet" href="/assets/css/boletim.css?v={css_version}"><script defer src="/js/pd-navigation.js?v=3"></script><script defer src="/js/boletim.js?v={js_version}"></script>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')}</script></head><body><a class="bulletin-skip" href="#main">Pular para o conteúdo</a>{header}
<main id="main" class="bulletin-wrap">{body}</main><footer class="bulletin-footer"><div class="bulletin-wrap">Praia Digital · Inteligência com fontes e contexto.<br><a href="/politica-de-privacidade.html">Privacidade</a> · <a href="/interesse.html">Contato e correções</a></div></footer></body></html>'''

def render_edition(root, edition, path, latest_date=None):
    cards = ''
    for item in edition['items']:
        updates = ''.join(f'<aside class="bulletin-update" aria-label="Nota editorial posterior"><strong>Nota de {time_tag(u["noted_at"])}</strong><p>{esc(u["text"])}</p><p class="metadata">Revisão: {esc(u["reviewer"])}</p></aside>' for u in item.get('updates', []))
        deadline = f'<p class="metadata">Prazo informado pela fonte: {time_tag(item["deadline"])}. Consulte a fonte para eventuais alterações.</p>' if item.get('deadline') else ''
        cards += f'''<article id="{esc(item['id'])}" class="bulletin-card news-item" data-city="{esc(item['city'])}" data-category="{esc(item['category'])}"><p class="eyebrow">{esc(item['category'])} · {esc(item['city'])}</p><h2>{esc(item['title'])}</h2>{updates}<p>{esc(item['summary'])}</p><p><strong>Por que importa · análise editorial:</strong> {esc(item['impact'])}</p>{deadline}<p class="metadata">Publicado pela fonte: {time_tag(item['published_at'])}<br>Conferido: {time_tag(item['checked_at'])}</p><a href="{esc(item['source_url'])}" rel="noopener">Ler na fonte: {esc(item['source_name'])}</a></article>'''
    if not cards:
        cards = '<div class="bulletin-card"><h2>Nenhuma notícia nova aprovada nesta edição</h2><p>Não substituímos a ausência de informação verificada por manchetes automáticas. Consulte as fontes oficiais abaixo; o radar é uma ferramenta de triagem, não uma notícia.</p></div>'
    cities = sorted({i['city'] for i in edition['items']})
    categories = sorted({i['category'] for i in edition['items']})
    filters = ''.join(f'<div class="bulletin-filter"><label for="filter-{key}">{label}</label><select id="filter-{key}"><option value="">Todos</option>' + ''.join(f'<option>{esc(v)}</option>' for v in values) + '</select></div>' for key, label, values in [('city', 'Cidade / região', cities), ('category', 'Tema', categories)])
    archive_notice = ''
    if latest_date and edition['date'] != latest_date:
        archive_notice = f'<aside class="bulletin-update"><strong>Edição arquivada de {human_date(edition["date"])}.</strong> O texto registra o que estava publicado naquela data. Notas posteriores estão identificadas junto à notícia. <a href="boletim-diario.html">Ler a edição mais recente</a>.</aside>'
    notes = ''.join(f'<section class="bulletin-card bulletin-update"><h2>{esc(note["title"])}</h2><p>{esc(note["text"])}</p><a href="{esc(note["source_url"])}">Conferir a fonte oficial</a> · <a href="boletim-{esc(note["related_edition"])}.html">Consultar a edição anterior com a nota</a></section>' for note in edition.get('notes', []))
    sources = '<li><a href="https://news.airbnb.com/">Airbnb Newsroom</a></li><li><a href="https://partner.booking.com/en-us">Booking Partner Hub</a></li><li><a href="https://www.bcb.gov.br/">Banco Central</a></li><li><a href="https://www.ibge.gov.br/">IBGE</a></li><li><a href="https://www.agenciasp.sp.gov.br/">Agência SP</a></li>'
    review_label = 'Revisão original desta edição' if stamp(modified_at(edition)) > stamp(edition['reviewed_at']) else 'Última revisão desta edição'
    update_label = f' · Nota posterior: {time_tag(modified_at(edition))}' if stamp(modified_at(edition)) > stamp(edition['reviewed_at']) else ''
    body = f'''<p class="eyebrow">Litoral paulista · Edição {human_date(edition['date'])}</p><h1>Boletim de Inteligência</h1>
<p class="lead">{esc(edition['summary'])}</p><p class="metadata">{review_label}: {time_tag(edition['reviewed_at'])} · {len(edition['items'])} notícia(s) com fonte{update_label}.</p>{archive_notice}
<nav class="bulletin-actions" aria-label="Acompanhar boletim"><a class="bulletin-button" href="#news">Ler as notícias</a><a href="#acompanhar">Acompanhar por RSS</a><a href="{PATH}arquivo-boletins.html">Edições anteriores</a><a href="#metodologia">Como trabalhamos</a></nav>
<details class="bulletin-status"><summary>Sobre esta edição e a frequência de publicação</summary><p>Revisão: {esc(edition['reviewer'])}.</p><p>Piloto editorial: novas edições são publicadas após revisão, sem frequência fixa ou promessa de tempo real. A data editorial não muda ao abrir a página. A coleta automática prepara candidatos, mas não publica notícias.</p></details>
<div class="bulletin-filters" hidden>{filters}<button class="bulletin-reset" type="button" id="filter-reset">Limpar filtros</button><p id="filter-status" role="status" aria-live="polite"></p></div><section aria-label="Notícias verificadas" id="news">{cards}</section><p id="filter-empty" hidden>Nenhuma notícia desta edição corresponde aos filtros. Use “Limpar filtros” para ver todas.</p>{notes}
<section class="bulletin-card" id="acompanhar"><h2>Receba novas edições no seu leitor de RSS</h2><p>RSS é uma forma gratuita de acompanhar atualizações sem fornecer seu e-mail. Copie o endereço abaixo e cole na opção de adicionar feed do leitor que você já utiliza.</p><label for="rss-address">Endereço do feed</label><input id="rss-address" type="url" readonly value="{BASE}{PATH}feed.xml"><button type="button" id="copy-rss" hidden>Copiar endereço do RSS</button><p id="copy-status" role="status" aria-live="polite"></p><p><a href="{PATH}feed.xml">Abrir o arquivo RSS (XML)</a> · <a href="/newsletter/assinatura.html">Status da assinatura por e-mail</a></p><p class="metadata">O feed só muda quando uma edição revisada é publicada. A assinatura por e-mail ainda não está ativa.</p></section>
<details class="bulletin-card"><summary>Radar de fontes e limites da coleta</summary><p>A <a href="/blog/novidades-airbnb-booking.html">Sentinela Airbnb + Booking</a> é um monitor separado. Alteração de página não comprova novidade e fontes podem estar indisponíveis.</p><ul>{sources}</ul><p>Links de consulta não significam que todas as fontes foram verificadas hoje.</p></details>
<section class="bulletin-card" id="metodologia"><h2>Como trabalhamos</h2><p>Notícias aprovadas trazem fonte primária, data da publicação, horário de conferência, região e contexto. A revisão é assistida por IA e não equivale a apuração presencial. A análise é identificada e não é recomendação individual de investimento.</p><p>Não usamos quantidade de artigos do nosso site como procura imobiliária, preço ou valorização. Estimativas financeiras exigem hipóteses, custos, período e método verificáveis. O histórico legado está identificado no arquivo.</p><p>O conteúdo é público e gratuito. Não há envio automático de e-mail ativo neste piloto. Nenhum cadastro é solicitado enquanto confirmação e descadastro não estiverem funcionando.</p><a href="/interesse.html">Sugerir pauta ou comunicar uma correção</a></section>'''
    title = 'Boletim de Inteligência · ' + human_date(edition['date'])
    return page(root, title, path, body, edition.get('description', edition['summary']), edition)

def build(root=ROOT):
    editions = [validate(json.loads(p.read_text(encoding='utf-8'))) for p in sorted((root / 'data/boletim/edicoes').glob('*.json'))]
    if not editions:
        raise ValueError('At least one reviewed edition is required')
    if len({e['date'] for e in editions}) != len(editions):
        raise ValueError('Duplicate edition date')
    editions.sort(key=lambda e: e['date'])
    for edition in editions:
        for note in edition.get('notes', []):
            if note['related_edition'] not in {e['date'] for e in editions}:
                raise ValueError('Editorial note references missing edition')
    out = root / 'docs/inteligencia'
    for edition in editions:
        path = PATH + 'boletim-' + edition['date'] + '.html'
        (root / path.lstrip('/')).write_text(render_edition(root, edition, path, editions[-1]['date']), encoding='utf-8')
    (out / 'boletim-diario.html').write_text(render_edition(root, editions[-1], PATH + 'boletim-diario.html'), encoding='utf-8')
    rows = ''.join(f'<li><a href="boletim-{e["date"]}.html">{human_date(e["date"])}</a> — {len(e["items"])} notícia(s) verificada(s)</li>' for e in reversed(editions))
    body = f'<p class="eyebrow">Memória editorial</p><h1>Arquivo de boletins</h1><p>Edições efetivamente publicadas, sem reconstrução artificial de dias sem boletim.</p><ul>{rows}</ul><h2>Registro legado</h2><p><a href="boletim-2026-07-17.html">17/07/2026 — modelo antigo, não usar como indicador de mercado</a>. Não há arquivo diário completo do período anterior.</p><p><a href="boletim-diario.html">Voltar ao boletim</a> · <a href="feed.xml">RSS gratuito</a></p>'
    (out / 'arquivo-boletins.html').write_text(page(root, 'Arquivo de boletins', PATH + 'arquivo-boletins.html', body, 'Edições revisadas e registros históricos identificados do Boletim Praia Digital.'), encoding='utf-8')
    rss = ET.Element('rss', version='2.0'); channel = ET.SubElement(rss, 'channel')
    for key, val in [('title', 'Boletim Praia Digital'), ('link', BASE + PATH + 'boletim-diario.html'), ('description', 'Edições revisadas, fontes e contexto. Sem promessa de publicação em tempo real.'), ('language', 'pt-BR'), ('lastBuildDate', format_datetime(max(stamp(modified_at(e)) for e in editions)))]:
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
        ET.SubElement(entry, 'lastmod').text = modified_at(edition)
    ET.indent(sitemap)
    ET.ElementTree(sitemap).write(root / 'sitemap-boletim.xml', encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--root', type=Path, default=ROOT)
    build(parser.parse_args().root)
