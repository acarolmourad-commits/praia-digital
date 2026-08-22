import os
import re
import json
from sqlalchemy.orm import Session
from academy.core.models_proprietarios import Proprietario, ProprietarioFoto
from academy.core.models import TrackingEvent

PUBLIC_DIR = os.path.abspath("proprietarios")

os.makedirs(PUBLIC_DIR, exist_ok=True)


def _sanitize_slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "imovel"


def generate_public_page(proprietario: Proprietario, db: Session = None) -> str:
    fotos = []
    if db is not None:
        fotos = db.query(ProprietarioFoto).filter(ProprietarioFoto.proprietario_id == proprietario.id, ProprietarioFoto.aprovada == True).order_by(ProprietarioFoto.ordem).all()
    slug = f"{_sanitize_slug(proprietario.cidade or '')}-{_sanitize_slug(proprietario.tipo_imovel or '')}-{proprietario.codigo.lower()}"
    url = f"https://praia.digital/proprietarios/{slug}.html"
    path = os.path.join(PUBLIC_DIR, f"{slug}.html")
    valor = f"R$ {proprietario.valor_anunciado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if proprietario.valor_anunciado else "Consulte"
    fotos_html = ""
    for foto in fotos[:10]:
        src = foto.caminho_publico.replace("\\", "/")
        fotos_html += f'<img src="/{src}" alt="{proprietario.titulo or proprietario.cidade or "Imóvel"}" loading="lazy">\n'
    titulo = proprietario.titulo or f"{proprietario.tipo_imovel or 'Imóvel'} em {proprietario.cidade or 'Litoral'} — {proprietario.codigo}"
    html = f"""<!DOCTYPE html>
<html lang=\"pt-BR\">
<head>
<meta charset=\"UTF-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
<title>{titulo} | Praia Digital</title>
<meta name=\"description\" content=\"{proprietario.meta_description or proprietario.descricao or 'Anúncio de imóvel no litoral de SP.'}\">
<link rel=\"canonical\" href=\"{url}\">
</head>
<body>
<h1>{titulo}</h1>
<p>{proprietario.descricao or ''}</p>
<p><strong>Valor:</strong> {valor}</p>
<div class=\"fotos\">{fotos_html}</div>
</body>
</html>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    if db is not None:
        db.add(TrackingEvent(event="property.published", payload=json.dumps({"codigo": proprietario.codigo, "url": url}, ensure_ascii=False)))
        db.commit()
    return url


def update_sitemap(new_urls: list[str]) -> str:
    sitemap_path = os.path.abspath("sitemap.xml")
    if not os.path.exists(sitemap_path):
        return ""
    with open(sitemap_path, "r", encoding="utf-8") as f:
        current = f.read()
    additions = "\n".join([f"<url><loc>{u}</loc></url>" for u in new_urls if u not in current])
    if additions:
        updated = current.replace("</urlset>", additions + "\n</urlset>", 1)
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(updated)
        return sitemap_path
    return sitemap_path
