#!/usr/bin/env python3
"""One-shot (2026-10-20): eliminate Propaganda x temporada duplication.

- servicos.html: Propaganda card was duplicated temporada copy at R$ 497 PIX.
  It becomes the sale/rental ad-creation product at R$ 500 per ad, with FAQ
  and a differentiated Stripe CTA (new Propaganda payment link).
- servicos/propaganda-imobiliaria.html: this is the sale/rental product.
  Add BRL 500 Offer to JSON-LD, price/payment section and Stripe CTA;
  remove the duplicated 'O que voce ganha' block (duplicate of 'O que inclui').
- servicos/anuncios-airbnb-booking.html: temporada description stays inside
  the temporada service (no link out to Propaganda); add a clear crosslink
  for sale/rental instead.

Stripe (created 2026-10-20, distinct from the Airbnb/Booking product):
  product prod_VTjFfiQeSyVcWn, price price_1USlmoJRA2AketBhBnlPvXX1,
  payment link plink_1USln5JRA2AketBhcS58FvgX.
Fails closed if any expected snippet is not found exactly once.
"""
from pathlib import Path

NEW = "https://buy.stripe.com/dRm9AUc08eO3adFf044ZR1W"
OLD_SEASONAL = "https://buy.stripe.com/fZu00k6FO49padFg484ZR1V"


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 occurrence, found {count}")
    return text.replace(old, new)


def edit(path, transform):
    target = Path(path)
    original = target.read_text(encoding="utf-8")
    updated = transform(original)
    if updated == original:
        raise SystemExit(f"{path}: no changes produced")
    target.write_text(updated, encoding="utf-8")
    print(f"updated {path}")


def edit_servicos(text):
    text = replace_once(
        text,
        '<span class="info"><b>Propaganda imobiliária</b><small>Descrição otimizada e copywriting de alta conversão para Airbnb, Booking e VRBO.</small><span class="price">R$ 497,00 no PIX</span><span class="cta">Ver como funciona ',
        '<span class="info"><b>Propaganda imobiliária</b><small>Criação de anúncio para venda ou locação: copy, estrutura e roteiro de distribuição em portais, redes sociais e WhatsApp.</small><span class="price">R$ 500 por anúncio</span><span class="cta">Ver o serviço e pagar ',
        "servicos propaganda card",
    )
    text = replace_once(
        text,
        """        <details>
        <summary>Os serviços são para temporada?</summary>""",
        """      <details>
        <summary>Quanto custa criar um anúncio para vender ou alugar um imóvel?</summary>
        <p>R$ 500 por anúncio, por imóvel, na Propaganda imobiliária (venda ou locação). Para temporada no Airbnb ou Booking, também são R$ 500 por anúncio, por plataforma; o mesmo imóvel nas duas plataformas soma R$ 1.000.</p>
      </details>
        <details>
        <summary>Os serviços são para temporada?</summary>""",
        "servicos faq propaganda price",
    )
    text = replace_once(
        text,
        f'<a class="btn-ghost" href="{OLD_SEASONAL}" target="_blank" rel="noopener">Pagar An&uacute;ncios R$ 500 no Stripe</a>',
        f'<a class="btn-ghost" href="{OLD_SEASONAL}" target="_blank" rel="noopener">Pagar anúncio de temporada R$ 500 no Stripe</a>\n        <a class="btn-ghost" href="{NEW}" target="_blank" rel="noopener">Pagar anúncio de venda/locação R$ 500 no Stripe</a>',
        "servicos final stripe ctas",
    )
    return text


def edit_propaganda(text):
    description = "Propaganda imobiliária para venda ou locação de imóveis no litoral paulista: criação de anúncio por R$ 500, com copy, estrutura e roteiro de distribuição em portais, redes sociais e WhatsApp."
    text = replace_once(
        text,
        '<meta name="description" content="Propaganda imobiliária com foco em conversão para imóveis no litoral paulista.">',
        f'<meta name="description" content="{description}">',
        "propaganda meta description",
    )
    text = text.replace(
        'content="Propaganda imobiliária com foco em conversão para imóveis no litoral paulista."',
        f'content="{description}"',
    )
    text = replace_once(
        text,
        '"url": "https://praia.digital/servicos/propaganda-imobiliaria.html"\n  }',
        '"url": "https://praia.digital/servicos/propaganda-imobiliaria.html",\n'
        '    "description": "Criação de anúncio imobiliário para venda ou locação no litoral paulista, com copy, estrutura e roteiro de distribuição em portais, redes sociais e WhatsApp.",\n'
        f'    "offers": {{ "@type": "Offer", "priceCurrency": "BRL", "price": "500", "availability": "https://schema.org/InStock", "url": "{NEW}" }}\n  }}',
        "propaganda json-ld offer",
    )
    text = replace_once(
        text,
        ".btn-whatsapp { display: inline-block; margin-top: 18px; padding: 10px 14px; border-radius: 12px; background: #1f6feb; color: #fff; text-decoration: none; font-weight: 600; }",
        ".btn-whatsapp { display: inline-block; margin-top: 18px; padding: 10px 14px; border-radius: 12px; background: #1f6feb; color: #fff; text-decoration: none; font-weight: 600; }\n    .btn-stripe { display: inline-block; margin-top: 18px; padding: 10px 14px; border-radius: 12px; background: #16a34a; color: #fff; text-decoration: none; font-weight: 700; }\n    main a { color: #7dd3fc; }",
        "propaganda stripe css",
    )
    text = replace_once(
        text,
        '<p class="lead">Anúncios com foco em conversão para imóveis no litoral paulista, com posicionamento digital alinhado à procura real.</p>',
        '<p class="lead">Criação de anúncio para <strong>vender ou alugar</strong> seu imóvel no litoral paulista: copy e estrutura pensadas para a procura real por cidade e bairro, com roteiro de distribuição em portais, redes sociais e WhatsApp.</p>',
        "propaganda lead",
    )
    start = text.find("<h2>O que inclui</h2>")
    end = text.find("<h2>Atendimento no litoral</h2>")
    if start == -1 or end == -1 or start >= end:
        raise SystemExit(f"propaganda duplicated sections not found: start={start} end={end}")
    block = f'''<h2>O que inclui a criação do anúncio</h2>
      <ul>
        <li>Copy e estrutura de anúncio para venda ou locação, por cidade e bairro</li>
        <li>Título, descrição e chamadas para ação pensadas para gerar contatos qualificados</li>
        <li>Roteiro de distribuição em portais, redes sociais e WhatsApp</li>
        <li>Texto final do anúncio pronto para publicação</li>
      </ul>

      <h2>Venda ou locação — e temporada?</h2>
<p>Este serviço cria o anúncio de <strong>venda ou locação</strong> do imóvel. Para aluguel de temporada, o serviço específico é <a href="https://praia.digital/servicos/anuncios-airbnb-booking.html">Anúncios Airbnb e Booking</a> (R$ 500 por anúncio, por plataforma).</p>

<h2>Para quem é</h2>
<p>Proprietários, corretores e imobiliárias que querem vender ou alugar um imóvel com um anúncio profissional e mais qualidade de leads.</p>

<h2>Investimento</h2>
<p><strong>R$ 500 por anúncio, por imóvel</strong> — para venda ou locação.</p>
<p><a class="btn-stripe" href="{NEW}" target="_blank" rel="noopener">Pagar R$ 500 no Stripe</a></p>
<p>Pagamento seguro via Stripe — cartão, Pix ou boleto. No checkout, ajuste a quantidade quando houver mais de um imóvel. Mídia paga (impulsionamento) e gestão contínua de campanha não estão incluídas nesse valor; quando necessárias, são combinadas por escrito antes de qualquer contratação.</p>

'''
    text = text[:start] + block + text[end:]
    text = replace_once(text, ">Quero propaganda que converte</a>", ">Falar com especialista no WhatsApp</a>", "propaganda whatsapp label")
    return text


def edit_anuncios(text):
    text = replace_once(
        text,
        '<div class="card"><h3>✍️ Descrição que vende</h3><p>Copywriting otimizado para Airbnb, Booking e VRBO, com palavras-chave e gatilhos de conversão.</p><a class="go" href="/servicos/propaganda-imobiliaria.html">Ver propaganda imobiliária →</a></div>',
        '<div class="card"><h3>✍️ Descrição que vende</h3><p>Copywriting otimizado para Airbnb, Booking e VRBO, com palavras-chave e gatilhos de conversão — parte deste serviço de temporada.</p><a class="go" href="/assets/servico-geracao-descricoes-anuncios-ia.html">Ver geração de descrições →</a></div>',
        "anuncios description card dedupe",
    )
    needle = "2</strong> = Airbnb + Booking para o mesmo im&oacute;vel (R$ 1.000).</p>"
    if text.count(needle) != 1:
        raise SystemExit(f"anuncios crosslink anchor: expected 1, found {text.count(needle)}")
    text = text.replace(
        needle,
        needle + '\n  <p style="margin-top:12px">Vai <strong>vender ou alugar</strong> o imóvel (não é temporada)? Veja <a href="https://praia.digital/servicos/propaganda-imobiliaria.html">Propaganda imobiliária — R$ 500 por anúncio</a>.</p>',
        1,
    )
    return text


def main():
    edit("servicos.html", edit_servicos)
    edit("servicos/propaganda-imobiliaria.html", edit_propaganda)
    edit("servicos/anuncios-airbnb-booking.html", edit_anuncios)
    print("OK: duplication removed; Propaganda is the R$ 500 sale/rental product")


if __name__ == "__main__":
    main()
