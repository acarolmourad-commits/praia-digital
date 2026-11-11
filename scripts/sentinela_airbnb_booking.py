#!/usr/bin/env python3
"""Sentinela Airbnb + Booking - Praia Digital.
Monitora fontes oficiais e separa links detectados de informativos revisados.
Mudancas de hash ficam no relatorio, sem virar noticia. A revisao editorial
versionada e preservada em toda coleta. Nao envia mensagens aos usuarios.
"""
import hashlib, html, json, os, re, sys, urllib.request
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

from marketplaces_editorial import automatic_html, index_html, render_publication

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
    {"id": "booking-news", "platform": "Booking.com", "name": "Booking Newsroom (oficial)",
     "url": "https://news.booking.com/", "base": "https://news.booking.com",
     "pattern": r"^/[a-z0-9][a-z0-9\-]{20,}/?$", "kind": "items"},
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
        url = urljoin(src["base"] + "/", html.unescape(href))
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.hostname != urlparse(src["base"]).hostname:
            continue
        if not re.search(src["pattern"], parsed.path):
            continue
        url = parsed._replace(query="", fragment="").geturl().rstrip("/")
        txt = clean_text(inner)
        if len(txt) < 12:
            txt = href.rstrip("/").split("/")[-1].replace("-", " ").title()
        if txt.lower() in ("espanol (america latina)", "francais (belgique)", "francais (canada)"):
            continue
        if url not in out or len(txt) > len(out[url]):
            out[url] = txt
    return out

def page_hash(body):
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", body, flags=re.S | re.I)
    return hashlib.sha256(clean_text(body).encode("utf-8")).hexdigest()

def esc(s):
    return html.escape(s, quote=True)

def article_html(platform, title, date_str, items, src, is_hash, filename="novidades-airbnb-booking.html"):
    return automatic_html(platform, title, date_str, items, src, is_hash, filename)


def main():
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d %H:%M UTC")
    stamp = now.strftime("%Y%m%d-%H%M%S")
    state = {"version": 1, "sources": {}, "articles": []}
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as f:
            state = json.load(f)
    os.makedirs(OUTDIR, exist_ok=True)
    if "--render-only" in sys.argv:
        render_publication(state, OUTDIR)
        print("Informativos revisados renderizados sem consultar fontes ou alterar o estado.")
        return
    new_posts = []
    baseline_created = not os.path.exists(STATE)
    report = []
    for src in SOURCES:
        prev = state["sources"].get(src["id"], {})
        status, body = fetch(src["url"])
        entry = {"name": src["name"], "url": src["url"], "status": status, "checked_at": now.isoformat(timespec="seconds")}
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
                title = f"Link detectado {src['platform']}: {new_items[0][1]}"
                fname = f"novidades-{stamp}-{src['id']}.html"
                with open(os.path.join(OUTDIR, fname), "w", encoding="utf-8") as f:
                    f.write(article_html(src["platform"], title, date_str, new_items, src, False, fname))
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
                report.append(f"- {src['name']}: alteracao tecnica de pagina; requer revisao do tema. Nenhum post publicado.")
            elif not prev.get("hash"):
                baseline_created = True
                report.append(f"- {src['name']}: baseline de hash criado; nenhum post.")
            else:
                report.append(f"- {src['name']}: sem alteracao.")
        state["sources"][src["id"]] = entry
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    render_publication(state, OUTDIR)
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
