#!/usr/bin/env python3
"""Sentinela Airbnb + Booking - Praia Digital.
Monitora apenas fontes oficiais. Publica post automatico SOMENTE com
manchetes/links oficiais extraidos (items) ou deteccao de alteracao de
pagina oficial (hash). Nunca inventa funcionalidade nao citada na fonte.
"""
import hashlib, html, json, os, re, sys, urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "automation", "marketplaces", "sentinela-estado.json")
OUTDIR = os.path.join(ROOT, "blog")
REPORT = os.path.join(ROOT, "automation", "marketplaces", "sentinela-ultimo-relatorio.md")

SOURCES = [
    {"id": "airbnb-releases", "platform": "Airbnb", "name": "Airbnb Product Releases (oficial)",
     "url": "https://news.airbnb.com/product-releases/", "base": "https://news.airbnb.com",
     "pattern": r"/product-releases/airbnb-", "kind": "items"},
    {"id": "airbnb-news", "platform": "Airbnb", "name": "Airbnb Newsroom (oficial)",
     "url": "https://news.airbnb.com/", "base": "https://news.airbnb.com",
     "pattern": r"^/[a-z0-9][a-z0-9\-]{20,}$", "kind": "items"},
    {"id": "airbnb-resources", "platform": "Airbnb", "name": "Airbnb Resource Center - Anfitrioes (oficial)",
     "url": "https://www.airbnb.com/resources/hosting-homes", "base": "https://www.airbnb.com",
     "pattern": r"/resources/hosting-homes/a/", "kind": "items"},
    {"id": "booking-partner", "platform": "Booking.com", "name": "Booking Partner Hub (oficial)",
     "url": "https://partner.booking.com/en-us", "base": "https://partner.booking.com", "kind": "hash"},
    {"id": "booking-join", "platform": "Booking.com", "name": "Booking - pagina oficial para parceiros",
     "url": "https://join.booking.com/", "base": "https://join.booking.com", "kind": "hash"},
]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; PraiaDigitalSentinela/1.0; +https://praia.digital/)"})
    try:
        r = urllib.request.urlopen(req, timeout=30)
        return r.status, r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return None, f"ERROR: {e}"

def clean_text(x):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))).strip()

def extract_items(body, src):
    out = {}
    for href, inner in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', body, re.S | re.I):
        if not re.search(src["pattern"], href):
            continue
        txt = clean_text(inner)
        if len(txt) < 12:
            txt = href.rstrip("/").split("/")[-1].replace("-", " ").title()
        if txt.lower() in ("espanol (america latina)", "francais (belgique)", "francais (canada)"):
            continue
        url = href if href.startswith("http") else src["base"] + href
        if url not in out or len(txt) > len(out[url]):
            out[url] = txt
    return out

def page_hash(body):
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", body, flags=re.S | re.I)
    return hashlib.sha256(clean_text(body).encode("utf-8")).hexdigest()

def esc(s):
    return html.escape(s, quote=True)

def article_html(platform, title, date_str, items, src, is_hash):
    lis = ""
    if is_hash:
        lis = f'<li><a href="{esc(src["url"])}">{esc(src["name"])}</a> — alteracao detectada no conteudo publico oficial em {date_str}. O tema especifico deve ser confirmado dentro do Partner Hub oficial.</li>'
    else:
        for u, t in items:
            lis += f'<li><a href="{esc(u)}">{esc(t)}</a> <span>(fonte oficial)</span></li>'
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Praia Digital</title>
<meta name="description" content="Novidade oficial {esc(platform)} detectada pela Sentinela Praia Digital: o que mudou, o que significa para anfitrioes e o que fazer agora.">
<style>
body{{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:#0a2540;line-height:1.65;margin:0}}
.wrap{{max-width:860px;margin:0 auto;padding:0 20px}}
header{{background:#0a2540;color:#fff;padding:18px 0}} header a{{color:#7fd1cf}}
main{{padding:36px 0 56px}} .tag{{display:inline-block;background:#eef6f6;color:#0a5f5e;padding:4px 12px;border-radius:99px;font-size:.8rem;font-weight:700}}
h1{{font-size:clamp(1.6rem,3.4vw,2.3rem);line-height:1.2}} h2{{margin-top:32px}}
.card{{background:#f7f4ee;border:1px solid #e3e9ef;border-radius:14px;padding:18px 20px}}
a{{color:#0e7c7b}} footer{{background:#081c30;color:#9db4c6;padding:26px 0;font-size:.9rem}}
</style>
</head>
<body>
<header><div class="wrap"><a href="/">Praia<strong>Digital</strong></a> · <a href="/blog/novidades-airbnb-booking.html">Novidades Airbnb + Booking</a></div></header>
<main><div class="wrap">
<p class="tag">{esc(platform)} · Detectado em {date_str}</p>
<h1>{esc(title)}</h1>
<p><strong>Resumo direto:</strong> nossa Sentinela monitora as fontes oficiais do {esc(platform)} a cada 6 horas. Na verificacao de {date_str}, identificamos o item abaixo. Publicamos apenas a manchete/link oficial — sem prometer recurso que a plataforma nao tenha anunciado.</p>
<div class="card"><h2 style="margin-top:0">O que mudou</h2><ul>{lis}</ul></div>
<h2>O que isso significa para anfitrioes</h2>
<p>Pode afetar anuncio, preco, calendario, regras da estadia ou conversao em reservas. O impacto real depende do seu tipo de imovel e das configuracoes atuais — por isso, confira o item oficial antes de mudar preco ou regra.</p>
<h2>O que fazer agora</h2>
<ol>
<li>Abra a fonte oficial acima e leia o anuncio completo.</li>
<li>Compare com seu anuncio atual (fotos, descricao, preco, calendario e regras).</li>
<li>Se precisar, ajuste com apoio da <a href="/#central-airbnb-booking">Central Airbnb + Booking da Praia Digital</a>.</li>
<li>Anote a data da sua revisao para acompanhar o proximo ciclo.</li>
</ol>
<p><em>Fonte oficial monitorada: <a href="{esc(src['url'])}">{esc(src['name'])}</a>. Post gerado automaticamente pela Sentinela Praia Digital a partir de fonte oficial, com modelo editorial fixo de verificacao.</em></p>
</div></main>
<footer><div class="wrap">Praia Digital — <a href="/anfitrioes/central-airbnb.html">Central Airbnb</a> · <a href="/anfitrioes/central-booking.html">Central Booking.com</a> · <a href="/apps/">Apps gratuitos</a> · <a href="/servicos/anuncios-airbnb-booking.html">Anuncios Airbnb/Booking</a> · <a href="/">Home</a></div></footer>
</body>
</html>
"""

def index_html(articles):
    rows = ""
    for a in reversed(articles):
        rows += f'<li><span class="tag">{esc(a["platform"])}</span> <a href="/blog/{esc(a["file"])}">{esc(a["title"])}</a> <small>({esc(a["date"])})</small></li>'
    if not rows:
        rows = "<li>O Sentinela está ativo e aguardando a próxima novidade oficial das plataformas.</li>"
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Novidades Airbnb e Booking | Praia Digital</title>
<meta name="description" content="Acompanhe novidades oficiais do Airbnb e da Booking.com para anfitrioes de temporada, detectadas a cada 6 horas pela Sentinela Praia Digital.">
<style>body{{font-family:system-ui,sans-serif;color:#0a2540;line-height:1.65;margin:0}}.wrap{{max-width:860px;margin:0 auto;padding:0 20px}}header{{background:#0a2540;color:#fff;padding:18px 0}}header a{{color:#7fd1cf}}main{{padding:36px 0 56px}}.tag{{background:#eef6f6;color:#0a5f5e;padding:3px 10px;border-radius:99px;font-size:.75rem;font-weight:700}}a{{color:#0e7c7b}}li{{margin:12px 0}}.card{{background:#f7f4ee;border:1px solid #e3e9ef;border-radius:14px;padding:18px 20px;margin:24px 0}}footer{{background:#081c30;color:#9db4c6;padding:26px 0;font-size:.9rem}}footer a{{color:#7fd1cf}}</style>
</head>
<body>
<header><div class="wrap"><a href="/">Praia<strong>Digital</strong></a> · Novidades Airbnb + Booking</div></header>
<main><div class="wrap">
<h1>Novidades Airbnb e Booking</h1>
<p>Posts automaticos, a partir de <strong>fontes oficiais</strong>, detectados a cada 6 horas pela Sentinela Praia Digital. Cada post traz: o que mudou, o que significa para anfitrioes e o que fazer agora.</p>
<ul>{rows}</ul>
<p>Veja tambem: <a href="/#central-airbnb-booking">Central Airbnb + Booking</a> · <a href="/anfitrioes/central-airbnb.html">Central Airbnb</a> · <a href="/anfitrioes/central-booking.html">Central Booking.com</a></p>
<section class="card"><h2 style="margin-top:0">Continue explorando a Praia Digital</h2><p>Ferramentas gratuitas e servicos para anfitrioes e proprietarios no litoral:</p><ul><li><a href="/#central-airbnb-booking">Central Airbnb + Booking</a></li><li><a href="/apps/">Apps gratuitos Praia Digital</a></li><li><a href="/apps/simulador-roi-temporada/">Simulador de ROI de temporada</a></li><li><a href="/servicos/anuncios-airbnb-booking.html">Criacao e edicao de anuncios Airbnb e Booking</a></li></ul></section>
</div></main>
<footer><div class="wrap">Praia Digital — <a href="/">Home</a> · <a href="/apps/">Apps</a> · <a href="/#central-airbnb-booking">Central Airbnb + Booking</a></div></footer>
</body>
</html>
"""

def main():
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d %H:%M UTC")
    stamp = now.strftime("%Y%m%d-%H%M%S")
    state = {"version": 1, "sources": {}, "articles": []}
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as f:
            state = json.load(f)
    os.makedirs(OUTDIR, exist_ok=True)
    new_posts = []
    baseline_created = not os.path.exists(STATE)
    report = []
    for src in SOURCES:
        prev = state["sources"].get(src["id"], {})
        status, body = fetch(src["url"])
        entry = {"name": src["name"], "url": src["url"], "status": status}
        if status != 200 or body.startswith("ERROR"):
            entry["seen"] = prev.get("seen", {})
            entry["hash"] = prev.get("hash")
            entry["unavailable"] = True
            state["sources"][src["id"]] = entry
            report.append(f"- {src['name']}: fonte indisponivel (status={status}); nenhum post publicado.")
            continue
        if src["kind"] == "items":
            items = extract_items(body, src)
            seen = prev.get("seen", {})
            new_items = [(u, t) for u, t in items.items() if u not in seen]
            entry["seen"] = {**seen, **items}
            entry["hash"] = page_hash(body)
            if not seen:
                baseline_created = True
                report.append(f"- {src['name']}: baseline criado com {len(items)} itens; nenhum post.")
            elif new_items:
                new_items = new_items[:5]
                title = f"Novidades {src['platform']}: {new_items[0][1]}"
                fname = f"novidades-{stamp}-{src['id']}.html"
                with open(os.path.join(OUTDIR, fname), "w", encoding="utf-8") as f:
                    f.write(article_html(src["platform"], title, date_str, new_items, src, False))
                state.setdefault("articles", []).append({"date": date_str, "platform": src["platform"], "title": title, "file": fname, "source": src["url"]})
                new_posts.append(title)
                report.append(f"- {src['name']}: {len(new_items)} item(ns) novo(s) -> post {fname}")
            else:
                report.append(f"- {src['name']}: sem novidades.")
        else:
            h = page_hash(body)
            entry["hash"] = h
            entry["seen"] = prev.get("seen", {})
            if prev.get("hash") and prev["hash"] != h:
                title = f"Atualizacao detectada: {src['name']}"
                fname = f"novidades-{stamp}-{src['id']}.html"
                with open(os.path.join(OUTDIR, fname), "w", encoding="utf-8") as f:
                    f.write(article_html(src["platform"], title, date_str, [], src, True))
                state.setdefault("articles", []).append({"date": date_str, "platform": src["platform"], "title": title, "file": fname, "source": src["url"]})
                new_posts.append(title)
                report.append(f"- {src['name']}: alteracao de pagina detectada -> post {fname}")
            elif not prev.get("hash"):
                baseline_created = True
                report.append(f"- {src['name']}: baseline de hash criado; nenhum post.")
            else:
                report.append(f"- {src['name']}: sem alteracao.")
        state["sources"][src["id"]] = entry
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUTDIR, "novidades-airbnb-booking.html"), "w", encoding="utf-8") as f:
        f.write(index_html(state.get("articles", [])))
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("# Sentinela Airbnb + Booking\n\n" + f"Verificacao: {date_str}\n\n" + "\n".join(report) + "\n")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(f"has_new={'true' if new_posts else 'false'}\n")
            f.write(f"new_posts={len(new_posts)}\n")
            f.write(f"published_count={len(new_posts)}\n")
            f.write(f"changed={'true' if (new_posts or baseline_created) else 'false'}\n")
    print("\n".join(report))
    print(f"NEW_POSTS={len(new_posts)}")

if __name__ == "__main__":
    main()
