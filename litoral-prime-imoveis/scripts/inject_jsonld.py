"""
Litoral Prime — injeta JSON-LD structured data nas páginas principais para SEO avançado.
Suporta: Organization, WebSite, LocalBusiness, Service, ItemList.
"""
from pathlib import Path
import json, re, datetime

BASE = Path(__file__).resolve().parent.parent
TARGETS = [
    BASE / "index.html",
    BASE / "servicos.html",
    BASE / "imoveis.html" if (BASE / "imoveis.html").exists() else None,
]

org = {
    "name": "Litoral Prime Imóveis",
    "description": "Imobiliária digital no litoral de São Paulo: Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente e Peruíbe.",
    "url": "https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/",
    "telephone": "+5511954346288",
    "areaServed": ["Santos", "Guarujá", "Praia Grande", "Bertioga", "Itanhaém", "Mongaguá", "São Vicente", "Peruíbe"],
}

website_block = json.dumps({
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": org["name"],
    "url": org["url"],
}, ensure_ascii=False)

local_block = json.dumps({
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": org["name"],
    "description": org["description"],
    "telephone": org["telephone"],
    "areaServed": org["areaServed"],
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Santos",
        "addressRegion": "SP",
        "addressCountry": "BR",
    },
}, ensure_ascii=False)

services = [
    "Avaliação de Imóveis",
    "Captação Digital",
    "Automação Imobiliária",
    "Consultoria Proptech",
    "Descrição com IA",
]
service_block = json.dumps({
    "@context": "https://schema.org",
    "@type": "Service",
    "serviceType": "Consultoria e intermediação imobiliária",
    "provider": {"@type": "LocalBusiness", "name": org["name"]},
    "areaServed": org["areaServed"],
}, ensure_ascii=False)


def inject_once(path: Path):
    if not path or not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    if 'application/ld+json' in html:
        return
    block = f"{website_block}\n{local_block}\n{service_block}\n"
    snippet = f'<script type="application/ld+json">\n{block}</script>'
    html = html.replace('</head>', f'{snippet}</head>')
    path.write_text(html, encoding="utf-8")
    print(path.name, "OK")


def run():
    for p in TARGETS:
        inject_once(p)
    print("JSON-LD injetado.")


if __name__ == "__main__":
    run()
