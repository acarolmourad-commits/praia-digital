#!/usr/bin/env python3
"""Praia Digital - rede de apps (2026-10-21). Idempotente: remove cartao externo ASF de apps/index.html (foco exclusivo Praia Digital), corrige ancora morta /#jornadas-apps para /#apps e interliga Novidades Airbnb+Booking, Central e servico de anuncios."""
import pathlib, re, sys
TARGET = pathlib.Path('apps/index.html')

def main() -> int:
    text = TARGET.read_text(encoding='utf-8')
    original = text
    text = text.replace('/#jornadas-apps', '/#apps')
    text = re.sub(r'\n  <a class="card" href="https://acarolmourad-commits\.github\.io/asf-app/apps/".*?</a>', '', text, flags=re.S)
    if '/blog/novidades-airbnb-booking.html' not in text:
        promo = '<p class="pd-network-note">Acompanhe: <a href="/blog/novidades-airbnb-booking.html">Novidades Airbnb e Booking</a> (fontes oficiais a cada 6 horas) \u00b7 <a href="/#central-airbnb-booking">Central Airbnb + Booking</a> \u00b7 <a href="/servicos/anuncios-airbnb-booking.html">Criacao/edicao de anuncios Airbnb e Booking</a></p>\n'
        text = text.replace('<footer>', promo + '<footer>', 1) if '<footer>' in text else text + promo
    if 'asf-app' in text.lower() or 'jornadas-apps' in text.lower():
        print('ERRO: link ASF ou ancora jornadas-apps ainda presente', file=sys.stderr)
        return 1
    if text != original:
        TARGET.write_text(text, encoding='utf-8')
        print('apps/index.html atualizado')
    else:
        print('apps/index.html ja atualizado (idempotente)')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
