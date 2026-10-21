#!/usr/bin/env python3
"""Atualiza a home (index.html) para destacar Anuncios Airbnb/Booking por R$ 499.
Resolucao do PR #54 contra a main atual: a home ja evoluiu para a Central
Airbnb + Booking com card a R$ 499, entao este script apenas aprimora esse
card (criacao ou edicao, beneficios), preservando o restante da home atual.
Idempotente: se o texto novo ja existir, nao altera. Falha se o card
esperado nao for encontrado.
Uso: python3 scripts/apply_anuncios_499_home_20261021.py
"""
from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
if 'Anúncios Airbnb e Booking — R$ 499,00' in s:
    print('Home ja esta em R$ 499,00 - nada a fazer')
    raise SystemExit(0)

old = '<a class="card" href="/servicos/anuncios-airbnb-booking.html"><span class="tag">Anúncios · temporada</span><h3>Anúncios Airbnb e Booking — R$ 499</h3><p>Criação e otimização de anúncios de temporada, por anúncio, por plataforma: fotos, descrição, diagnóstico e precificação dinâmica para gerar reservas de hóspedes. Produto independente — não é propaganda de venda ou locação.</p>'
new = '<a class="card" href="/servicos/anuncios-airbnb-booking.html"><span class="tag">Temporada · fácil de contratar</span><h3>Anúncios Airbnb e Booking — R$ 499,00</h3><p>Criação ou edição de anúncio de temporada, por anúncio, por plataforma: título e descrição que vendem, fotos organizadas, comodidades completas, calendários sincronizados e precificação inicial. Um anúncio excelente gera mais cliques, mais confiança e mais reservas. Produto independente — não é propaganda de venda ou locação.</p>'
if old not in s:
    raise SystemExit('Card Airbnb/Booking esperado nao encontrado na home atual')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('Home atualizada: card Airbnb/Booking R$ 499,00 em destaque (demais conteudos da home preservados)')
