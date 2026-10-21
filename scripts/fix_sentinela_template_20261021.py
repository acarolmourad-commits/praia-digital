#!/usr/bin/env python3
"""Atualiza o template do hub/artigos da Sentinela (idempotente).
Garante navegacao/promocao consistente sem alterar fontes, editorial ou cron.
"""
import pathlib, sys
TARGET = pathlib.Path('scripts/sentinela_airbnb_booking.py')

def replace_once(text, old, new, label):
    if new in text:
        return text
    if old not in text:
        print(f'ERRO: trecho nao encontrado: {label}', file=sys.stderr)
        raise SystemExit(1)
    return text.replace(old, new, 1)

def main() -> int:
    text = TARGET.read_text(encoding='utf-8')
    original = text
    text = replace_once(text, 'li{{margin:12px 0}}</style>', 'li{{margin:12px 0}}.card{{background:#f7f4ee;border:1px solid #e3e9ef;border-radius:14px;padding:18px 20px;margin:24px 0}}footer{{background:#081c30;color:#9db4c6;padding:26px 0;font-size:.9rem}}footer a{{color:#7fd1cf}}</style>', 'css-hub')
    promo = '<section class="card"><h2 style="margin-top:0">Continue explorando a Praia Digital</h2><p>Ferramentas gratuitas e servicos para anfitrioes e proprietarios no litoral:</p><ul><li><a href="/#central-airbnb-booking">Central Airbnb + Booking</a> &mdash; hub completo na pagina inicial</li><li><a href="/apps/">Apps gratuitos Praia Digital</a> &mdash; ROI de temporada, precificacao, financiamento e mais</li><li><a href="/apps/simulador-roi-temporada/">Simulador de ROI de temporada</a></li><li><a href="/servicos/anuncios-airbnb-booking.html">Criacao e edicao de anuncios Airbnb e Booking</a></li><li><a href="/anfitrioes/central-airbnb.html">Central Airbnb</a> &middot; <a href="/anfitrioes/central-booking.html">Central Booking.com</a></li></ul></section>'
    text = replace_once(text, 'Central Booking.com</a></p>\n</div></main>', 'Central Booking.com</a></p>\n' + promo + '\n</div></main>', 'promo-hub')
    text = replace_once(text, '</div></main>\n</body>', '</div></main>\n<footer><div class="wrap">Praia Digital &mdash; <a href="/">Home</a> &middot; <a href="/apps/">Apps</a> &middot; <a href="/#central-airbnb-booking">Central Airbnb + Booking</a></div></footer>\n</body>', 'footer-hub')
    text = replace_once(text, 'Central Booking.com</a> \u00b7 <a href="/">Home</a></div></footer>', 'Central Booking.com</a> \u00b7 <a href="/apps/">Apps gratuitos</a> \u00b7 <a href="/servicos/anuncios-airbnb-booking.html">Anuncios Airbnb/Booking</a> \u00b7 <a href="/">Home</a></div></footer>', 'footer-artigo')
    if text != original:
        TARGET.write_text(text, encoding='utf-8')
        print('sentinela template atualizado')
    else:
        print('sentinela template ja atualizado')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
