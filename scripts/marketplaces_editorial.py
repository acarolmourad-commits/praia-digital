"""Render reviewed marketplace information separately from automatic link detection."""
import html
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
EDITORIAL = ROOT / "automation/marketplaces/informativos-revisados.json"
OFFICIAL_HOSTS = {"news.airbnb.com", "www.airbnb.com", "www.airbnb.com.br",
                  "news.booking.com", "partner.booking.com", "join.booking.com",
                  "www.airbnb.org", "airbnb.org"}


def esc(value):
    return html.escape(str(value), quote=True)


def load_editorial(path=EDITORIAL):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    reviewed = date.fromisoformat(data["reviewed_on"])
    if reviewed > date.today():
        raise ValueError("Review date cannot be in the future")
    files = set()
    for article in data["articles"]:
        name = article["file"]
        if Path(name).name != name or not name.startswith("novidades-") or not name.endswith(".html") or name in files:
            raise ValueError(f"Invalid or duplicate article filename: {name}")
        files.add(name)
        for field in ["platform", "title", "category", "summary", "brazil"]:
            if not article.get(field):
                raise ValueError(f"Missing {field}: {name}")
        if date.fromisoformat(article["source_published"]) > reviewed:
            raise ValueError(f"Source publication is later than review: {name}")
        if not article.get("sources") or not article.get("details") or not article.get("actions"):
            raise ValueError(f"Incomplete reviewed article: {name}")
        for source in article["sources"]:
            url = urlparse(source["url"])
            if url.scheme != "https" or url.hostname not in OFFICIAL_HOSTS or url.username:
                raise ValueError(f"Source must be official HTTPS: {source['url']}")
            if date.fromisoformat(source["date"]) > reviewed:
                raise ValueError(f"Source date is later than review: {name}")
    for article in data["articles"]:
        if article.get("related_file") and article["related_file"] not in files:
            raise ValueError("Related article is missing")
    return data


def human_date(value):
    return date.fromisoformat(value).strftime("%d/%m/%Y")


STYLE = """
*{box-sizing:border-box}body{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;color:#0a2540;line-height:1.65;margin:0;background:#fff}
.wrap{max-width:960px;margin:0 auto;padding:0 20px}header{background:#0a2540;color:#fff;padding:18px 0}header a,footer a{color:#a2e3df}
main{padding:32px 0 48px}h1{font-size:clamp(1.7rem,4vw,2.7rem);line-height:1.18}h2{line-height:1.3;margin-top:32px}h3{line-height:1.4}
a{color:#075e5d;text-underline-offset:3px;overflow-wrap:anywhere}a:hover{text-decoration-thickness:2px}a:focus-visible{outline:3px solid #f3b33e;outline-offset:4px}
.tag{display:inline-block;background:#edf6f5;color:#075e5d;padding:3px 10px;border-radius:99px;font-size:.8rem;font-weight:700;margin:0 5px 5px 0}
.meta{color:#40566b;font-size:.9rem}.card{border:1px solid #dce4e9;border-radius:14px;padding:20px;margin:20px 0;background:#f7f9fa}.card h2,.card h3{margin-top:0}
.notice{border-left:4px solid #ae7423;background:#fff8eb;padding:16px 20px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.grid .card{margin:0}
li{margin:9px 0}ul,ol{padding-left:24px}nav.links{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}.source-list{font-size:.95rem}footer{background:#081c30;color:#d1e0ea;padding:24px 0}
@media(max-width:650px){.grid{grid-template-columns:1fr}.wrap{padding:0 16px}.card{padding:16px}h1{overflow-wrap:anywhere}}
"""


def page(title, description, body, filename):
    canonical = "https://praia.digital/blog/" + filename
    return f'''<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | Praia Digital</title><meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}"><style>{STYLE}</style></head><body>
<header class="pd-header"><div class="wrap"><a href="/">Praia Digital</a> · <a href="/blog/novidades-airbnb-booking.html">Informativos Airbnb e Booking</a></div></header>
<main id="conteudo"><div class="wrap">{body}</div></main>
<footer><div class="wrap">Praia Digital · <a href="/anfitrioes/central-airbnb.html">Central Airbnb</a> · <a href="/anfitrioes/central-booking.html">Central Booking</a> · <a href="/contato.html">Contato e correções</a></div></footer>
</body></html>
'''


def article_html(article, reviewed_on, detected_on=None):
    a = article
    details = ''.join(f'<li>{esc(text)}</li>' for text in a["details"])
    actions = ''.join(f'<li>{esc(text)}</li>' for text in a["actions"])
    sources = ''.join(f'<li><a href="{esc(s["url"])}">{esc(s["label"])}</a> · {human_date(s["date"])}</li>' for s in a["sources"])
    detected = f'<p class="meta">Primeira detecção neste site: {esc(detected_on)}. Essa data não é a data de publicação da fonte.</p>' if detected_on else ''
    related = ''
    if a.get("related_file"):
        related = f'<p>Este assunto também foi detectado em outra fonte oficial. <a href="/blog/{esc(a["related_file"])}">Consultar o informativo principal</a>.</p>'
    body = f'''
<p><span class="tag">{esc(a["platform"])}</span><span class="tag">{esc(a["category"])}</span><span class="tag">Revisado</span></p>
<h1>{esc(a["title"])}</h1>
<p class="meta">Publicado pela fonte: <time datetime="{a["source_published"]}">{human_date(a["source_published"])}</time> · Revisão editorial: <time datetime="{reviewed_on}">{human_date(reviewed_on)}</time>.</p>
{detected}<p>{esc(a["summary"])}</p>
<section class="card"><h2>O que a fonte confirma</h2><ul>{details}</ul></section>
<section class="notice"><h2>Disponibilidade e impacto no Brasil</h2><p>{esc(a["brazil"])}</p></section>
<section><h2>O que fazer agora</h2><p class="meta">Sugestões editoriais da Praia Digital, a partir das informações acima.</p><ol>{actions}</ol></section>
{related}<section><h2>Fontes e datas</h2><ul class="source-list">{sources}</ul></section>
<p class="meta">A disponibilidade pode mudar e depender da conta ou do mercado. Confirme na plataforma antes de alterar preços, regras ou configurações.</p>
<p><a href="/blog/novidades-airbnb-booking.html">Voltar a todos os informativos</a></p>
'''
    return page(a["title"], a["summary"], body, a["file"])


def automatic_html(platform, title, detected_on, items, source, is_hash, filename="novidades-airbnb-booking.html"):
    links = ''.join(f'<li><a href="{esc(url)}">{esc(text)}</a></li>' for url, text in items)
    if is_hash:
        links = f'<li><a href="{esc(source["url"])}">{esc(source["name"])}</a></li>'
    body = f'''<p class="tag">{esc(platform)} · Detecção automática, sem revisão editorial</p>
<h1>{esc(title)}</h1><p class="meta">Detectado em {esc(detected_on)}. Data original de publicação não confirmada.</p>
<section class="notice"><h2>Leitura pendente</h2><p>O monitor encontrou um link ou uma alteração na fonte oficial. Isso não confirma lançamento de recurso, mudança de regra nem disponibilidade no Brasil.</p></section>
<h2>Links encontrados</h2><ul>{links}</ul><h2>Antes de agir</h2><p>Leia a fonte, confira a data e verifique se o anúncio se aplica à sua conta e ao seu país. Este registro ainda não contém uma análise prática revisada.</p>
<p><a href="/blog/novidades-airbnb-booking.html">Ver os informativos revisados</a></p>'''
    return page(title, "Link de fonte oficial detectado automaticamente, ainda sem revisão editorial ou confirmação de disponibilidade no Brasil.", body, filename)


def index_html(articles, editorial=None, sources=None):
    editorial = editorial or load_editorial()
    reviewed = editorial["articles"]
    reviewed_files = {a["file"] for a in reviewed}
    cards, archive = [], []
    for a in reviewed:
        item = f'<span class="tag">{esc(a["platform"])}</span><span class="tag">{esc(a["category"])}</span><h3><a href="/blog/{esc(a["file"])}">{esc(a["title"])}</a></h3><p>{esc(a["summary"])}</p><p class="meta">Fonte: {human_date(a["source_published"])} · Revisado: {human_date(editorial["reviewed_on"])}</p>'
        if a.get("featured"):
            cards.append(f'<article class="card">{item}</article>')
        else:
            archive.append(f'<li><a href="/blog/{esc(a["file"])}">{esc(a["title"])}</a> · {esc(a["category"])} · fonte: {human_date(a["source_published"])}</li>')
    pending = ''.join(f'<li><a href="/blog/{esc(a["file"])}">{esc(a["title"])}</a> · detecção: {esc(a["date"])}</li>' for a in reversed(articles) if a["file"] not in reviewed_files)
    pending_section = f'<ul>{pending}</ul>' if pending else '<p>Nenhum outro link está listado como pendente nesta edição. Isso não significa que todas as novidades das plataformas foram cobertas.</p>'
    coverage = []
    for source in (sources or {}).values():
        available = source.get("status") == 200 and not source.get("unavailable")
        status = 'Página acessível na última coleta; isso não comprova revisão do conteúdo.' if available else 'Conteúdo não pôde ser validado na última coleta.'
        checked = f' Coleta: {esc(source["checked_at"])}.' if source.get("checked_at") else ' O estado anterior não registra o horário da coleta.'
        coverage.append(f'<li><a href="{esc(source["url"])}">{esc(source["name"])}</a>: {status}{checked}</li>')
    body = f'''<p class="tag">Para anfitriões e gestores de temporada</p><h1>Novidades Airbnb e Booking</h1>
<p>O que foi anunciado, onde está disponível e o que vale conferir no seu anúncio. Informativos com fontes oficiais, datas e sugestões práticas para o litoral paulista.</p>
<p class="meta">Revisão editorial desta edição: <time datetime="{editorial["reviewed_on"]}">{human_date(editorial["reviewed_on"])}</time>. Publicação no site; <a href="/newsletter/assinatura.html">assinatura por e-mail ainda não ativa</a>.</p>
<nav class="links" aria-label="Seções dos informativos"><a href="#revisados">Informativos revisados</a><a href="#arquivo">Outros assuntos</a><a href="#monitoramento">Monitoramento e limites</a></nav>
<section id="revisados"><h2>Informativos revisados</h2><div class="grid">{''.join(cards)}</div></section>
<section id="arquivo"><h2>Outros assuntos revisados</h2><p>Notícias institucionais, parcerias e medidas sazonais são identificadas separadamente dos recursos da plataforma.</p><ul>{''.join(archive)}</ul></section>
<section id="monitoramento"><h2>Monitoramento e limites</h2><p>A Sentinela tem coleta programada a cada 6 horas. Ela detecta links para conferência, mas não garante atualização em tempo real, cobertura completa ou funcionamento de todas as fontes.</p>
<p>Os informativos revisados ficam separados das detecções automáticas. Alterar uma página não prova uma novidade. Data de detecção, publicação da fonte e revisão editorial são informações diferentes.</p>
<h3>Links detectados ainda sem revisão</h3>{pending_section}<h3>Estado das fontes monitoradas</h3><ul>{''.join(coverage)}</ul>
<p>Booking: o Partner Hub pode limitar consultas públicas. A cobertura revisada desta edição usa comunicados oficiais acessíveis e identifica pesquisas de tendências, sem tratá-las como novas regras operacionais.</p></section>
<p><a href="/anfitrioes/central-airbnb.html">Central Airbnb</a> · <a href="/anfitrioes/central-booking.html">Central Booking</a> · <a href="/docs/inteligencia/boletim-diario.html">Boletim de inteligência do litoral</a></p>'''
    return page("Novidades Airbnb e Booking", "Informativos revisados sobre Airbnb e Booking: fontes oficiais, datas, disponibilidade no Brasil e sugestões práticas para anfitriões.", body, "novidades-airbnb-booking.html")


def render_publication(state, outdir, editorial=None):
    editorial = editorial or load_editorial()
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    detected = {a["file"]: a["date"] for a in state.get("articles", [])}
    for article in editorial["articles"]:
        (outdir / article["file"]).write_text(article_html(article, editorial["reviewed_on"], detected.get(article["file"])), encoding="utf-8")
    (outdir / "novidades-airbnb-booking.html").write_text(index_html(state.get("articles", []), editorial, state.get("sources", {})), encoding="utf-8")
