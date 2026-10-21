#!/usr/bin/env python3
"""Patch idempotente do template da Sentinela (2026-10-21): interliga Apps e Servicos no hub gerado a cada 6h e no rodape dos posts, mantendo fontes/modelo editorial inalterados."""
import pathlib, sys
T = pathlib.Path('scripts/sentinela_airbnb_booking.py')
s = T.read_text(encoding='utf-8')
orig = s
old_hub = '<p>Veja tambem: <a href="/#central-airbnb-booking">Central Airbnb + Booking</a>'
new_hub = '<p>Veja tambem: <a href="/#central-airbnb-booking">Central Airbnb + Booking</a>'
# Expand hub footer/navigation in index_html() only via unique closing sequence
old_close = 'Central Booking.com</a></p>\n</div></main>\n</body>\n</html>\n\"\"\"'
new_close = 'Central Booking.com</a></p>\n<section class="card"><h2 style="margin-top:0">Continue explorando a Praia Digital</h2><p>Ferramentas gratuitas e servicos para anfitrioes e proprietarios no litoral:</p><ul><li><a href="/#central-airbnb-booking">Central Airbnb + Booking</a> &mdash; hub completo na pagina inicial</li><li><a href="/apps/">Apps gratuitos Praia Digital</a></li><li><a href="/apps/simulador-roi-temporada/">Simulador de ROI de temporada</a></li><li><a href="/servicos/anuncios-airbnb-booking.html">Criacao e edicao de anuncios Airbnb e Booking</a></li></ul></section>\n</div></main>\n<footer><div class="wrap">Praia Digital &mdash; <a href="/">Home</a> &middot; <a href="/apps/">Apps</a> &middot; <a href="/#central-airbnb-booking">Central Airbnb + Booking</a></div></footer>\n</body>\n</html>\n\"\"\"'
if old_close in s:
    s = s.replace(old_close, new_close, 1)
old_footer = 'Central Booking.com</a> \u00b7 <a href="/">Home</a></div></footer>'
new_footer = 'Central Booking.com</a> \u00b7 <a href="/apps/">Apps gratuitos</a> \u00b7 <a href="/servicos/anuncios-airbnb-booking.html">Anuncios Airbnb/Booking</a> \u00b7 <a href="/">Home</a></div></footer>'
if old_footer in s:
    s = s.replace(old_footer, new_footer, 1)
if '/apps/' not in s or '/servicos/anuncios-airbnb-booking.html' not in s:
    print('ERRO: patch da Sentinela nao aplicado', file=sys.stderr); return_code = 1
else:
    return_code = 0
    if s != orig:
        T.write_text(s, encoding='utf-8'); print('sentinela template atualizado')
    else:
        print('sentinela template ja atualizado (idempotente)')
raise SystemExit(return_code)
