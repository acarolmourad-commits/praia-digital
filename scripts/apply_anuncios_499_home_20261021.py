#!/usr/bin/env python3
"""Atualiza a home (index.html) para destacar Anuncios Airbnb/Booking por R$ 499.
Idempotente: se o texto novo ja existir, nao altera. Falha se o texto esperado nao for encontrado.
Uso: python3 scripts/apply_anuncios_499_home_20261021.py
"""
from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
if 'Anúncios Airbnb e Booking — R$ 499,00' in s:
    print('Home ja esta em R$ 499 - nada a fazer')
    raise SystemExit(0)

subs = [
    ('<h2>Criação de anúncios por R$ 500</h2>',
     '<h2>Criação de anúncios a partir de R$ 499 — destaque: Airbnb e Booking</h2>'),
    ('<p class="lead">Anúncio profissional pronto para publicar — escolha a finalidade do seu imóvel:</p>',
     '<p class="lead">Produto fácil de vender e de entregar: seu anúncio de temporada criado ou editado, pronto para gerar mais cliques, confiança e reservas. Escolha a finalidade do seu imóvel:</p>'),
    ('<span class="tag">Temporada</span><h3>Anúncios Airbnb e Booking — R$ 500</h3><p>Criação e otimização de anúncios de temporada, por anúncio, por plataforma: fotos, descrição, diagnóstico e precificação dinâmica.</p>',
     '<span class="tag">Temporada · fácil de contratar</span><h3>Anúncios Airbnb e Booking — R$ 499,00</h3><p>Criação ou edição de anúncio de temporada, por anúncio, por plataforma: título e descrição que vendem, fotos organizadas, comodidades completas, calendários sincronizados e precificação inicial. Um anúncio excelente gera mais cliques, mais confiança e mais reservas.</p>'),
]
for old, new in subs:
    if old not in s:
        raise SystemExit(f'Trecho esperado nao encontrado na home: {old[:80]}')
    s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('Home atualizada: Airbnb/Booking R$ 499 em destaque (Propaganda venda/locacao mantida em R$ 500)')
