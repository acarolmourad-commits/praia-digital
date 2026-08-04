"""Orquestrador único da Litoral Prime: executa todas as operações do site num só passo."""
import glob
import json
import os
from datetime import date
from pathlib import Path
import importlib.util
import sys

REPO = Path(r"C:\Users\Carolina\praia-digital\litoral-prime-imoveis")
DOMAIN = "https://praia.digital/litoral-prime-imoveis"


def refresh_sitemap():
    rels = sorted(
        str(Path(p).relative_to(REPO)).replace("\\", "/")
        for p in glob.glob(str(REPO / "**/*.html"), recursive=True)
        if "template" not in p and str(Path(p).relative_to(REPO)).replace("\\", "/") != "sitemap.html"
    )
    sm_path = REPO / "sitemap.xml"
    text = sm_path.read_text(encoding="utf-8") if sm_path.exists() else ""
    if "<url>" in text:
        prefix = text.split("<url>")[0]
        suffix = text.split("</url>")[-1].split("</urlset>")
        suffix = suffix[-1].split("</urlset>")[0] if len(suffix) > 1 else ""
    else:
        prefix = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        suffix = "</urlset>"
    today = date.today().isoformat()
    url_blocks = []
    # Always include sitemap.html
    url_blocks.append(
        f"  <url>\n    <loc>{DOMAIN}/sitemap.html</loc>\n    <lastmod>{today}</lastmod>\n"
        f"    <priority>0.5</priority>\n  <changefreq>weekly</changefreq>\n  </url>"
    )
    for rel in rels:
        loc = f"{DOMAIN}/{rel}"
        url_blocks.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n"
            f"    <priority>0.8</priority>\n  <changefreq>weekly</changefreq>\n  </url>"
        )
    new_sm = prefix + "\n".join(url_blocks) + "\n" + suffix
    sm_path.write_text(new_sm, encoding="utf-8")
    print(f"[OK] Sitemap sincronizado: {len(rels)} URLs")


def patch_whatsapp_links():
    ctx = {
        "outreach/materiais.html": "Olá! Li os materiais de divulgação e quero ajuda com os textos/CTAs.",
        "outreach/posts-redes-sociais.html": "Olá! Li os posts para redes sociais e quero ajuda com a divulgação.",
        "outreach/posts-redes-sociais-servicos.html": "Olá! Li os posts para redes sociais de serviços e quero ajuda com a divulgação.",
        "docs/duvidas-frequentes.html": "Olá! Li as dúvidas frequentes e quero falar com um especialista.",
        "servicos/captura-rapida.html": "Olá! Quero vender meu imóvel no litoral.",
        "servicos/checklist-leads.html": "Olá! Quero usar o checklist de leads.",
        "servicos/consulta-rapida.html": "Olá! Quero uma consulta rápida sobre imóveis.",
        "servicos/guia-aluguel-temporada.html": "Olá! Li o guia de aluguel de temporada e quero ajuda.",
        "servicos/quero-vender-imovel-litoral.html": "Olá! Quero vender meu imóvel no litoral.",
        "index.html": "Olá! Encontrei a Litoral Prime e quero falar sobre imóveis no litoral.",
        "encontrar-imovel.html": "Olá! Quero encontrar um imóvel no litoral de SP.",
    }
    try:
        if (REPO / "imoveis/properties.json").exists():
            for prop in json.loads((REPO / "imoveis/properties.json").read_text(encoding="utf-8")):
                slug = prop.get("slug")
                title = (prop.get("title") or slug or "").strip()
                if not slug or not title:
                    continue
                ctx[f"imoveis/{slug}.html"] = f"Olá! Tenho interesse no {title}."
        if (REPO / "cidades").exists():
            for p in sorted((REPO / "cidades").glob("*.html")):
                name = p.name.lower()
                if "-" in name:
                    city = name.split("-", 1)[1].replace(".html", "").replace("-", " ").title()
                else:
                    city = name.replace(".html", "").title()
                ctx[f"cidades/{p.name}"] = f"Olá! Quero imóveis em {city.title()}."
    except Exception:
        pass
    updated = []
    for rel, msg in ctx.items():
        p = REPO / rel
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        target = 'href="https://wa.me/5511954346288"'
        if target not in html:
            continue
        encoded = msg.replace(" ", "%20").replace("?", "%3F").replace("!", "%21").replace("á", "%C3%A1").replace("ã", "%C3%A3").replace("â", "%C3%A2").replace("é", "%C3%A9").replace("ê", "%C3%AA").replace("í", "%C3%AD").replace("ó", "%C3%B3").replace("õ", "%C3%B5").replace("ô", "%C3%B4").replace("ú", "%C3%BA").replace("ü", "%C3%BC").replace("ç", "%C3%A7").replace(",", "%2C").replace(":", "%3A").replace("/", "%2F").replace("'", "%27")
        replacement = f'href="https://wa.me/5511954346288?text={encoded}"'
        new_html = html.replace(target, replacement)
        if new_html != html:
            p.write_text(new_html, encoding="utf-8")
            updated.append(rel)
    print(f"[OK] WhatsApp contextualizado: {len(updated)} páginas")


def sync_item_lists():
    props_path = REPO / "imoveis/properties.json"
    imoveis_dir = REPO / "imoveis"
    if not props_path.exists() or not imoveis_dir.exists():
        return
    props = json.loads(props_path.read_text(encoding="utf-8"))
    pages_json = {p.stem: p for p in imoveis_dir.glob("*.html") if p.name != "template.html"}
    items = []
    for prop in props:
        slug = prop["slug"]
        if slug not in pages_json:
            continue
        items.append(
            f'{{"@type": "ListItem", "position": {len(items)+1}, '
            f'"url": "{DOMAIN}/imoveis/{slug}.html", "name": "' + (prop.get("title") or prop["slug"]) + '"}'
        )
    if not items:
        return
    block = ",\n    ".join(items)
    new_items = '{\n  "@context": "https://schema.org",\n  "@type": "ItemList",\n  "name": "Imóveis no litoral de SP",\n  "itemListElement": [\n  ' + block + '\n  ]\n}'
    for rel in ["imoveis.html", "index.html"]:
        p = REPO / rel
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        start = html.find('{"@context": "https://schema.org", "@type": "ItemList"')
        if start == -1:
            continue
        end = html.find("</script>", start) + len("</script>")
        if end < len("</script>"):
            continue
        new_html = html[:start] + new_items + "\n  " + html[end:]
        p.write_text(new_html, encoding="utf-8")
    print(f"[OK] ItemLists sincronizados: {len(items)} imóveis")


def run_script(name: str, args=None):
    module_path = REPO / "scripts" / name
    if not module_path.exists():
        print(f"[WARN] Script não encontrado: {module_path}")
        return
    old_argv = sys.argv[:]
    try:
        sys.argv = [str(module_path)] + (args or [])
        spec = importlib.util.spec_from_file_location(name.replace(".py", ""), module_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name.replace(".py", "")] = mod
        try:
            spec.loader.exec_module(mod)
        except SystemExit as e:
            if e.code != 0:
                print(f"[ERR] {name} exited with {e.code}")
        main_func = getattr(mod, "main", None)
        if callable(main_func):
            main_func()
    except Exception as e:
        print(f"[ERR] {name}: {e}")
    finally:
        sys.argv = old_argv


def refresh_latest_pages():
    run_script("gerar_ultimos_por_cidade.py")
    run_script("gerar_ultimos_index.py")
    run_script("patch_ultimos_dynamic.py")
    run_script("inject_ultimos_links.py")
    run_script("inject_servicos_imoveis_ultimos_links.py")


def refresh_outreach_daily():
    run_script("run_outreach_dia.py")


def refresh_batch_merge():
    run_script("merge_batches_into_master.py")
    csv = REPO / "imoveis/dados_expanded.csv"
    if csv.exists():
        run_script("gerar_buscas.py", args=[str(csv), "--out", "imoveis"])


def generate_city_faqs():
    run_script("gerar_cidades_faq.py")
    run_script("inject_cidades_faq_links.py")
    run_script("inject_cidades_faq_backlinks.py")
    run_script("gerar_cidades_faq_hub.py")
    run_script("inject_cidades_hub_links.py")


def generate_service_pages_by_city():
    run_script("gerar_servicos_cidade.py")


def generate_catalog():
    run_script("gerar_catalogo.py")


def main():
    refresh_sitemap()
    patch_whatsapp_links()
    sync_item_lists()
    # refresh_latest_pages()  # scripts removidos no estado atual
    # refresh_outreach_daily()  # substituído por run_dia.py
    # refresh_batch_merge()  # script removido no estado atual
    # generate_city_faqs()  # scripts removidos no estado atual
    # generate_service_pages_by_city()  # script removido no estado atual
    # generate_catalog()  # script removido no estado atual
    print("[OK] Orquestração concluída.")


if __name__ == "__main__":
    main()
