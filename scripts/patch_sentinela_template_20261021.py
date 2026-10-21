#!/usr/bin/env python3
"""Patch idempotente do template da Sentinela (2026-10-21, v2 CSS fix). Hub e posts futuros interligam Apps, servico de anuncios e Central, com rodape padrao. No arquivo gerador, a CSS fica dentro de f-string, por isso as chaves sao duplas {{ }}."""
import pathlib, sys
P = pathlib.Path('scripts/sentinela_airbnb_booking.py')

def main():
    t = P.read_text(encoding='utf-8')
    orig = t
    t = t.replace('Central Booking.com</a> · <a href="/">Home</a>', 'Central Booking.com</a> · <a href="/apps/">Apps gratuitos</a> · <a href="/servicos/anuncios-airbnb-booking.html">Anuncios Airbnb/Booking</a> · <a href="/">Home</a>')
    if 'def index_html(articles):' in t:
        head, tail = t.split('def index_html(articles):', 1)
        if '.card{{' not in tail:
            tail = tail.replace('li{{margin:12px 0}}</style>', 'li{{margin:12px 0}}.card{{background:#f7f4ee;border:1px solid #e3e9ef;border-radius:14px;padding:18px 20px;margin:24px 0}}footer{{background:#081c30;color:#9db4c6;padding:26px 0;font-size:.9rem}}footer a{{color:#7fd1cf}}</style>')
        if 'Continue explorando a Praia Digital' not in tail:
            promo = '<section class="card"><h2 style="margin-top:0">Continue explorando a Praia Digital</h2><p>Ferramentas gratuitas e servicos para anfitrioes e proprietarios no litoral:</p><ul><li><a href="/#central-airbnb-booking">Central Airbnb + Booking</a></li><li><a href="/apps/">Apps gratuitos Praia Digital</a></li><li><a href="/apps/simulador-roi-temporada/">Simulador de ROI de temporada</a></li><li><a href="/servicos/anuncios-airbnb-booking.html">Criacao e edicao de anuncios Airbnb e Booking</a></li></ul></section>\n'
            tail = tail.replace('</div></main>\n</body>', promo + '</div></main>\n<footer><div class="wrap">Praia Digital — <a href="/">Home</a> · <a href="/apps/">Apps</a> · <a href="/#central-airbnb-booking">Central Airbnb + Booking</a></div></footer>\n</body>', 1)
        t = head + 'def index_html(articles):' + tail
    if 'Continue explorando a Praia Digital' not in t or '.card{{' not in t:
        print('ERRO: patch nao aplicado', file=sys.stderr); return 1
    if t != orig:
        P.write_text(t, encoding='utf-8'); print('sentinela_airbnb_booking.py atualizado')
    else:
        print('sentinela ja atualizado')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
