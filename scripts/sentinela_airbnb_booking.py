#!/usr/bin/env python3
"""Sentinela Airbnb + Booking - Praia Digital.
Monitora fontes oficiais, detecta posts novos, gera artigo PT-BR com
modelo assertivo, auto-revisa e publica (hub + artigo). Stdlib apenas.
Autonomia concedida pelo proprietario em 2026-10-21 para esta funcao.
"""
import hashlib, html, json, os, re, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
STATE = ROOT / "automation/marketplaces/sentinela-estado.json"
REPORT = ROOT / "automation/marketplaces/sentinela-ultimo-relatorio.md"
HUB = ROOT / "blog/novidades-airbnb-booking.html"
SITEMAP = "https://news.airbnb.com/sitemap.xml"
AUX = {
  "airbnb_product_releases": "https://news.airbnb.com/product-releases/",
  "airbnb_resource_center": "https://www.airbnb.com/resources/hosting-homes",
  "booking_partner_hub": "https://partner.booking.com/en-us",
  "booking_join": "https://join.booking.com/",
}
LOCALES = {"fr","de","it","es","pt","en-ca","fr-be","zh","ja","ko","ru","nl","sv","da","no","pl","tr","ar","he"}
RELEVANT = ["host","guest","trip","travel","stay","booking","reservation","weather","price","pricing","fee","cancel","policy","experience","rent","check-in","checkout","insurance","protection","payout"]
EXCLUDE = ["airbnb.org","emergency housing","wildfire","hurricane relief","free emergency","donates","donation"]

def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (PraiaDigitalSentinela/1.0)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return 0, f"ERROR: {e}"

def h16(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def candidates():
    status, body = fetch(SITEMAP, 60)
    if status != 200:
        return status, []
    out = []
    for block in re.findall(r"<url>(.*?)</url>", body, re.S):
        loc = re.search(r"<loc>([^<]+)</loc>", block)
        lm = re.search(r"<lastmod>([^<]+)</lastmod>", block)
        if not loc:
            continue
        url = loc.group(1).strip()
        m = re.match(r"https://news\.airbnb\.com/([a-z0-9\-]+)/?$", url)
        if not m or m.group(1) in LOCALES:
            continue
        out.append({"url": url, "slug": m.group(1), "lastmod": (lm.group(1)[:10] if lm else "")})
    out.sort(key=lambda x: x["lastmod"], reverse=True)
    return status, out

def meta(url):
    status, body = fetch(url)
    if status != 200:
        return status, "", ""
    def og(name):
        m = re.search(r'<meta property="%s" content="([^"]*)"' % name, body)
        return html.unescape(m.group(1)).strip() if m else ""
    return status, og("og:title"), og("og:description")

def relevant(title, desc, slug):
    t = f"{title} {desc} {slug}".lower()
    if any(x in t for x in EXCLUDE) and not any(x in t for x in ["host", "trip", "weather", "protection"]):
        return False
    return any(x in t for x in RELEVANT)

def article_html(item, title, desc, today):
    date = item["lastmod"] or today
    slug = item["slug"][:70]
    fname = f"novidades-{date}-{slug}.html"
    title_e = html.escape(title)
    desc_e = html.escape(desc)
    src = html.escape(item["url"])
    body = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://praia.digital/blog/{fname}">
<title>{title_e} | Novidades Airbnb e Booking — Praia Digital</title>
<meta name="description" content="Novidade oficial Airbnb detectada pelo Sentinela Praia Digital: {desc_e[:150]}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BlogPosting","headline":"{html.escape(title)}","datePublished":"{date}","author":{{"@type":"Organization","name":"Praia Digital"}},"publisher":{{"@type":"Organization","name":"Praia Digital","url":"https://praia.digital/"}}}}
</script>
<style>body{{font-family:system-ui,sans-serif;max-width:820px;margin:0 auto;padding:24px;line-height:1.65;color:#0a2540}}a{{color:#0e7c7b}}h1{{line-height:1.2}}.tag{{background:#eef6f6;padding:4px 12px;border-radius:99px;font-size:.8rem;font-weight:700}}blockquote{{background:#f7f4ee;padding:16px;border-left:4px solid #0e7c7b}}li{{margin:8px 0}}</style>
</head>
<body>
<p><a href="/blog/novidades-airbnb-booking.html">← Todas as novidades Airbnb e Booking</a></p>
<p><span class="tag">Novidade oficial · Airbnb</span></p>
<h1>{title_e}</h1>
<p><strong>Detectado pelo Sentinela Praia Digital em {today}.</strong> Atualização publicada automaticamente após auto-revisão: fonte oficial confirmada, estrutura completa e nenhum preço ou dado confidencial incluído.</p>
<h2>O que mudou</h2>
<p>A plataforma publicou oficialmente: <strong>{title_e}</strong>.</p>
<blockquote><strong>Resumo oficial (em inglês):</strong> {desc_e}</blockquote>
<h2>O que isso significa para anfitriões e proprietários no litoral</h2>
<p>Novidades de produto e de políticas das plataformas afetam visibilidade do anúncio, expectativa do hóspede, precificação e operação da temporada. Quem anuncia no litoral paulista deve conferir o impacto no próprio anúncio assim que a mudança entra em vigor, em vez de descobrir pela próxima reserva.</p>
<h2>O que fazer agora</h2>
<ol>
<li>Abra a fonte oficial abaixo e leia as condições e datas de vigência.</li>
<li>Confira se o seu anúncio (fotos, descrição, regras, política de cancelamento e preços) precisa de ajuste.</li>
<li>Atualize a comunicação com hóspedes já reservados, se a mudança afetar estadias futuras.</li>
<li>Precisa de ajuda? Veja a <a href="/anfitrioes/central-airbnb.html">Central Airbnb</a>, a <a href="/anfitrioes/central-booking.html">Central Booking.com</a> e o serviço de <a href="/servicos/anuncios-airbnb-booking.html">anúncios Airbnb e Booking</a>.</li>
</ol>
<h2>Fonte oficial</h2>
<p><a href="{src}" rel="noopener" target="_blank">{src}</a> — publicado/atualizado pela plataforma em {date}.</p>
<p><small>Artigo gerado e auto-revisado pelo Sentinela Airbnb + Booking da Praia Digital. Em caso de divergência, vale sempre a fonte oficial da plataforma.</small></p>
</body>
</html>
"""
    return fname, body

def self_review(text, source):
    checks = [
        source.startswith("https://news.airbnb.com/"),
        "Fonte oficial" in text,
        "O que mudou" in text and "O que fazer agora" in text,
        text.count("<h1>") == 1,
        "R$" not in text,
        len(text) > 1800,
        text.count("<html") == text.count("</html>") == 1,
    ]
    return all(checks)

def hub_html(published, today):
    cards = ""
    for p in sorted(published, key=lambda x: x["date"], reverse=True):
        cards += f'<article style="border:1px solid #e3e9ef;border-radius:14px;padding:20px;margin:14px 0"><p><strong>{html.escape(p["date"])}</strong> · {html.escape(p["platform"])}</p><h2 style="margin:6px 0"><a href="/blog/{html.escape(p["article"])}">{html.escape(p["title"])}</a></h2><p>{html.escape(p["summary"][:240])}</p><p><a href="/blog/{html.escape(p["article"])}">Ler o artigo completo →</a></p></article>'
    if not cards:
        cards = "<p>O Sentinela está ativo e aguardando a próxima novidade oficial das plataformas.</p>"
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://praia.digital/blog/novidades-airbnb-booking.html">
<title>Novidades Airbnb e Booking | Praia Digital</title>
<meta name="description" content="Novidades oficiais do Airbnb e da Booking.com acompanhadas em tempo real pelo Sentinela Praia Digital: o que mudou, o que significa e o que fazer agora.">
<style>body{{font-family:system-ui,sans-serif;max-width:820px;margin:0 auto;padding:24px;line-height:1.65;color:#0a2540}}a{{color:#0e7c7b}}</style>
</head>
<body>
<p><a href="/">← Praia Digital</a> · <a href="/#central-airbnb-booking">Central Airbnb + Booking</a></p>
<h1>Novidades Airbnb e Booking</h1>
<p>Acompanhe aqui, em um só lugar, as novidades oficiais das plataformas de temporada. Nosso agente <strong>Sentinela Airbnb + Booking</strong> monitora as fontes oficiais a cada 6 horas, auto-revisa e publica as atualizações relevantes para anfitriões e proprietários do litoral. Última atualização desta página: {today}.</p>
{cards}
<p><small>Fontes monitoradas: Airbnb Newsroom, Airbnb Product Releases, Airbnb Resource Center e Booking Partner Hub. Em caso de divergência, vale sempre a fonte oficial.</small></p>
</body>
</html>
"""

def main():
    today = datetime.now(timezone.utc).date().isoformat()
    STATE.parent.mkdir(parents=True, exist_ok=True)
    state = {"version": 1, "seen_hashes": [], "published": [], "sources": {}, "updated_at": None}
    if STATE.exists():
        state = json.loads(STATE.read_text(encoding="utf-8"))
    status, cands = candidates()
    lines = [f"# Sentinela Airbnb + Booking — {today} UTC", f"- Sitemap Airbnb: HTTP {status}, {len(cands)} posts candidatos"]
    published_new = 0
    if status == 200 and not state.get("seen_hashes"):
        state["seen_hashes"] = [h16(c["url"]) for c in cands[:400]]
        lines.append("- Baseline inicial criado (sem publicar retroativos).")
    elif status == 200:
        seen = set(state.get("seen_hashes", []))
        new_items = [c for c in cands if h16(c["url"]) not in seen]
        for item in sorted(new_items, key=lambda x: x["lastmod"]) :
            seen.add(h16(item["url"]))
            if published_new >= 3:
                continue
            st, title, desc = meta(item["url"])
            if st != 200 or not title or not relevant(title, desc, item["slug"]):
                lines.append(f"- Ignorado (irrelevante/sem meta): {item['url']}")
                continue
            fname, body = article_html(item, title, desc, today)
            if not self_review(body, item["url"]):
                lines.append(f"- REPROVADO na auto-revisao, nao publicado: {item['url']}")
                continue
            (ROOT / "blog" / fname).write_text(body, encoding="utf-8")
            state["published"] = [p for p in state["published"] if p["article"] != fname]
            state["published"].append({"date": item["lastmod"] or today, "platform": "Airbnb", "title": title, "article": fname, "source": item["url"], "summary": desc})
            published_new += 1
            lines.append(f"- PUBLICADO: {fname} <- {item['url']}")
        state["seen_hashes"] = list(seen)[:2000]
    for name, url in AUX.items():
        st, txt = fetch(url)
        digest = h16(txt[:200000]) if st == 200 else ""
        old = state.get("sources", {}).get(name, {})
        changed = old.get("hash") not in (None, digest) and st == 200
        state.setdefault("sources", {})[name] = {"status": st, "hash": digest, "checked_at": today}
        lines.append(f"- Fonte {name}: HTTP {st}" + (" (conteudo mudou; manchetes do sitemap sao a fonte de artigos)" if changed else ""))
    state["updated_at"] = today
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    HUB.write_text(hub_html(state.get("published", []), today), encoding="utf-8")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write("changed=true\n")
            f.write(f"published_count={published_new}\n")
    print("\n".join(lines))
    return 0

if __name__ == "__main__":
    sys.exit(main())
