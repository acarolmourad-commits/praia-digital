from pathlib import Path

PAIRS = [
    ("blog/compra-imovel-heranca-inventario-litoral-2026.html", "/blog/inventario-imovel-litoral-passo-a-passo-custos-prazo.html", "Inventario de imovel: passo a passo, custos, prazo e como regularizar para vender"),
    ("blog/analise-seo-imobiliarias-litoral-oportunidades-2026.html", "/blog/marketing-digital-imobiliarias-litoral-plano-30-dias.html", "Marketing digital para imobiliarias do litoral: plano pratico de 30 dias"),
    ("blog/contrato-aluguel-temporada-litoral-clausulas-2026.html", "/blog/rescisao-contrato-aluguel-temporada-multa-distrato.html", "Rescisao de contrato de aluguel de temporada: multa, prazos e distrato"),
    ("blog/como-usar-fgts-2026.html", "/blog/comprar-imovel-litoral-com-fgts-regras.html", "Comprar imovel no litoral com FGTS: regras e passo a passo"),
    ("blog/como-morar-enseada-guaruja-2026.html", "/blog/enseada-ou-pitangueiras-guaruja-onde-ficar-comprar.html", "Enseada ou Pitangueiras, no Guaruja: onde ficar e onde comprar"),
]

for source, href, title in PAIRS:
    path = Path(source)
    target = Path("blog") / href.rsplit("/", 1)[-1]
    if not path.exists():
        raise SystemExit(f"source missing: {source}")
    if not target.exists():
        raise SystemExit(f"target missing: {target}")
    html = path.read_text(encoding="utf-8")
    if href in html:
        print(f"skip (already linked): {source}")
        continue
    block = (
        '<aside class="pd-lote2-links" style="margin:2rem 0;padding:1rem 1.25rem;'
        'border:1px solid #e5e7eb;border-radius:12px;background:#f8fafc">'
        f'<p style="margin:0"><strong>Leia tambem:</strong> <a href="{href}">{title}</a></p></aside>\n'
    )
    for anchor in ("</main>", "</article>", "</body>"):
        if anchor in html:
            html = html.replace(anchor, block + anchor, 1)
            break
    else:
        raise SystemExit(f"no insertion anchor in {source}")
    path.write_text(html, encoding="utf-8")
    print(f"linked: {source} -> {href}")
