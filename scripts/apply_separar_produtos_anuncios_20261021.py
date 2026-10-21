#!/usr/bin/env python3
"""Separa Propaganda Imobiliaria (venda/locacao) de Anuncios Airbnb/Booking (temporada).
Sao produtos independentes: nao sao etapas, pacotes nem alternativas um do outro.
Versao v2 (2026-10-21): adaptada a main atual, onde a home ja tem a secao
'Central Airbnb + Booking' separada da secao de destaque da Propaganda.
Idempotente. Falha se algum trecho esperado nao for encontrado.
Uso: python3 scripts/apply_separar_produtos_anuncios_20261021.py
"""
from pathlib import Path

EDITS = {
    'index.html': [
        ('<h2>Criação de anúncios por R$ 499</h2>',
         '<h2>Propaganda Imobiliária — anúncio para vender ou alugar (R$ 499)</h2>'),
        ('<p class="lead">Anúncio profissional pronto para publicar — escolha a finalidade do seu imóvel:</p>',
         '<p class="lead">Produto independente para <strong>venda ou locação</strong> do imóvel. Não é anúncio de temporada, não é Airbnb nem Booking e não vende diárias.</p>'),
        ('<span class="tag">Venda ou locação</span><h3>Propaganda imobiliária — R$ 499</h3><p>Criação de anúncio para venda ou locação de imóveis, por imóvel: copy, estrutura e roteiro de distribuição em portais, redes sociais e WhatsApp.</p>',
         '<span class="tag">Venda ou locação · produto independente</span><h3>Propaganda imobiliária — R$ 499</h3><p>Para vender ou alugar o imóvel: anúncio por imóvel, com copy, estrutura e roteiro de distribuição em portais imobiliários, redes sociais e WhatsApp, para gerar compradores e locatários interessados. Não é anúncio de temporada.</p>'),
        ('<p class="lead">Todos os serviços de Airbnb, Booking e marketplaces de temporada da Praia Digital, reunidos nesta seção: criação e gestão de anúncios, centrais do anfitrião, precificação, suporte e ferramentas de rentabilidade.</p>',
         '<p class="lead">Todos os serviços de Airbnb, Booking e marketplaces de temporada da Praia Digital, reunidos nesta seção: criação e gestão de anúncios, centrais do anfitrião, precificação, suporte e ferramentas de rentabilidade. <strong>Produto independente de temporada/hospedagem — não é propaganda para venda ou locação do imóvel.</strong></p>'),
        ('<a class="card" href="/servicos/anuncios-airbnb-booking.html"><span class="tag">Anúncios</span><h3>Anúncios Airbnb e Booking</h3><p>Criação e otimização de anúncios de temporada: fotos, descrição, diagnóstico e precificação dinâmica.</p><p><strong>Ver o serviço →</strong></p></a>',
         '<a class="card" href="/servicos/anuncios-airbnb-booking.html"><span class="tag">Anúncios · temporada</span><h3>Anúncios Airbnb e Booking — R$ 499</h3><p>Criação e otimização de anúncios de temporada, por anúncio, por plataforma: fotos, descrição, diagnóstico e precificação dinâmica para gerar reservas de hóspedes. Produto independente — não é propaganda de venda ou locação.</p><p><strong>Ver o serviço e pagar →</strong></p></a>'),
    ],
    'servicos.html': [
        ('<b>Propaganda imobiliária</b><small>Criação de anúncio para venda ou locação: copy, estrutura e roteiro de distribuição em portais, redes sociais e WhatsApp.</small>',
         '<b>Propaganda imobiliária</b><small>Produto independente para vender ou alugar: copy, estrutura e roteiro de distribuição em portais, redes sociais e WhatsApp. Não é anúncio de temporada nem publicação no Airbnb/Booking.</small>'),
        ('<b>Anúncios Airbnb e Booking</b><small>Criação e otimização profissional de anúncios de temporada: fotos, descrição, diagnóstico e precificação dinâmica.</small>',
         '<b>Anúncios Airbnb e Booking</b><small>Produto independente para hospedagem de temporada: fotos, descrição, diagnóstico, calendário e precificação dinâmica para gerar reservas. Não é propaganda para venda ou locação.</small>'),
        ('<summary>Quanto custa criar um anúncio para vender ou alugar um imóvel?</summary>',
         '<summary>Quanto custa a Propaganda imobiliária (venda ou locação)?</summary>'),
        ('<p>R$ 499 por anúncio, por imóvel, na Propaganda imobiliária (venda ou locação). Para temporada no Airbnb ou Booking, também são R$ 499 por anúncio, por plataforma; o mesmo imóvel nas duas plataformas soma R$ 998.</p>',
         '<p>R$ 499 por anúncio, por imóvel. Produto exclusivo de venda/locação, com distribuição em portais, redes sociais e WhatsApp — não inclui temporada, Airbnb nem Booking.</p>\n      </details>\n      <details>\n        <summary>Quanto custa um anúncio no Airbnb ou Booking (temporada)?</summary>\n        <p>R$ 499 por anúncio, por plataforma. Produto exclusivo de hospedagem/temporada, contratado separadamente da Propaganda imobiliária; o mesmo imóvel nas duas plataformas soma R$ 998 (2 anúncios).</p>'),
        ('>Pagar anúncio de temporada R$ 499 no Stripe</a>',
         '>Pagar Anúncios Airbnb/Booking (temporada) — R$ 499 no Stripe</a>'),
        ('>Pagar anúncio de venda/locação R$ 499 no Stripe</a>',
         '>Pagar Propaganda imobiliária (venda/locação) — R$ 499 no Stripe</a>'),
    ],
    'servicos/anuncios-airbnb-booking.html': [
        ('<p style="margin-top:12px">Vai <strong>vender ou alugar</strong> o imóvel (não é temporada)? Veja <a href="https://praia.digital/servicos/propaganda-imobiliaria.html">Propaganda imobiliária — R$ 499 por anúncio</a>.</p>',
         '<p style="margin-top:12px"><strong>Escopo deste produto:</strong> exclusivamente hospedagem de temporada no Airbnb e no Booking. Não é venda, não é locação anual e não inclui distribuição em portais imobiliários.</p>'),
    ],
    'servicos/propaganda-imobiliaria.html': [
        ('<h2>Venda ou locação — e temporada?</h2>',
         '<h2>O que este produto não é</h2>'),
        ('<p>Este serviço cria o anúncio de <strong>venda ou locação</strong> do imóvel. Para aluguel de temporada, o serviço específico é <a href="https://praia.digital/servicos/anuncios-airbnb-booking.html">Anúncios Airbnb e Booking</a> (R$ 499 por anúncio, por plataforma).</p>',
         '<p><strong>Propaganda Imobiliária não tem relação com Airbnb nem Booking.</strong> Este serviço é exclusivamente para <strong>venda ou locação</strong> do imóvel. Não cria nem publica anúncio de temporada, não gerencia hóspedes, reservas, calendário nem precificação de diárias.</p>'),
    ],
}

changed = []
for fname, subs in EDITS.items():
    p = Path(fname)
    s = p.read_text(encoding='utf-8')
    original = s
    for old, new in subs:
        if new in s:
            continue
        if old not in s:
            raise SystemExit(f'Trecho esperado nao encontrado em {fname}: {old[:90]}')
        s = s.replace(old, new, 1)
    if s != original:
        p.write_text(s, encoding='utf-8')
        changed.append(fname)
print('Arquivos atualizados:', ', '.join(changed) if changed else 'nenhum (ja aplicado)')
