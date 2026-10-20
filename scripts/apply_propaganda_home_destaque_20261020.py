#!/usr/bin/env python3
"""One-shot (2026-10-20): home highlight for ad-creation services.

- index.html: add a featured section right before #imoveis with the two
  R$ 500 ad-creation services (Propaganda imobiliaria for sale/rental and
  Anuncios Airbnb/Booking for seasonal, per platform), linking to their
  service/payment pages.
- servicos.html: Propaganda card price becomes 'R$ 500 por anuncio, por
  imovel' (already R$ 500; this only clarifies the per-property unit,
  matching servicos/propaganda-imobiliaria.html and the FAQ).
Fails closed if an expected snippet is not found exactly once.
Idempotent: re-running after a successful apply is a no-op.
"""
from pathlib import Path


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 occurrence, found {count}")
    return text.replace(old, new)


def edit(path, transform):
    target = Path(path)
    original = target.read_text(encoding="utf-8")
    updated = transform(original)
    if updated != original:
        target.write_text(updated, encoding="utf-8")
        print(f"updated {path}")
    else:
        print(f"no change {path}")


HIGHLIGHT = '''<section id="servicos-destaque">
<div class="wrap">
  <p class="kicker">Serviços em destaque</p>
  <h2>Criação de anúncios por R$ 500</h2>
  <p class="lead">Anúncio profissional pronto para publicar — escolha a finalidade do seu imóvel:</p>
  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr));margin-top:16px">
    <a class="card" href="/servicos/propaganda-imobiliaria.html"><span class="tag">Venda ou locação</span><h3>Propaganda imobiliária — R$ 500</h3><p>Criação de anúncio para venda ou locação de imóveis, por imóvel: copy, estrutura e roteiro de distribuição em portais, redes sociais e WhatsApp.</p><p><strong>Ver o serviço e pagar →</strong></p></a>
    <a class="card" href="/servicos/anuncios-airbnb-booking.html"><span class="tag">Temporada</span><h3>Anúncios Airbnb e Booking — R$ 500</h3><p>Criação e otimização de anúncios de temporada, por anúncio, por plataforma: fotos, descrição, diagnóstico e precificação dinâmica.</p><p><strong>Ver o serviço e pagar →</strong></p></a>
  </div>
  <p style="margin-top:20px"><a class="btn" href="/servicos.html">Ver todos os serviços</a></p>
</div>
</section>
'''


def edit_home(text):
    if 'id="servicos-destaque"' in text:
        return text
    return replace_once(
        text,
        '\n<section id="imoveis">',
        '\n' + HIGHLIGHT + '\n<section id="imoveis">',
        "home destaque anchor",
    )


def edit_servicos(text):
    if 'R$ 500 por anúncio, por imóvel</span>' in text:
        return text
    return replace_once(
        text,
        '<span class="price">R$ 500 por anúncio</span>',
        '<span class="price">R$ 500 por anúncio, por imóvel</span>',
        "servicos propaganda price",
    )


def main():
    edit("index.html", edit_home)
    edit("servicos.html", edit_servicos)
    print("OK: home highlight applied; Propaganda is R$ 500 per property")


if __name__ == "__main__":
    main()
