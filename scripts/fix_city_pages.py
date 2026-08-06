import re
from pathlib import Path

base = Path('cidades')
files = list(base.glob('*-*.html')) + list(base.glob('*-academia.html')) + list(base.glob('*-comercial.html')) + list(base.glob('*-compra-programada.html')) + list(base.glob('*-elevador.html')) + list(base.glob('*-gestao-de-imovel.html')) + list(base.glob('*-imoveis-venda.html')) + list(base.glob('*-midia-profissional.html')) + list(base.glob('*-pet-friendly.html')) + list(base.glob('*-propaganda-imobiliaria.html')) + list(base.glob('*-residencial.html')) + list(base.glob('*-sacada.html')) + list(base.glob('*-sauna.html')) + list(base.glob('*-seguranca.html')) + list(base.glob('*-varanda.html')) + list(base.glob('*-venda-rapida.html'))
# remove duplicates and exclude main city pages
files = sorted(set(files))

city_fixes = {
    'guaruja': 'Guarujá',
    'santos': 'Santos',
    'bertioga': 'Bertioga',
    'itanhaem': 'Itanhaém',
    'mongagua': 'Mongaguá',
    'sao-vicente': 'São Vicente',
    'peruibe': 'Peruíbe',
    'praia-grande': 'Praia Grande',
    'caraguatatuba': 'Caraguatatuba',
    'ubatuba': 'Ubatuba',
    'ilhabela': 'Ilhabela',
    'sao-sebastiao': 'São Sebastião',
}

for f in files:
    txt = f.read_text(encoding='utf-8', errors='ignore')
    original = txt

    # remove ||| artifacts
    txt = txt.replace('|||', '')

    # fix broken JSON-LD
    txt = txt.replace('"https://***@type"', '"@type"')

    # fix default-home.jpg to logo.png in og/twitter images
    txt = txt.replace('https://praia.digital/img/default-home.jpg', 'https://praia.digital/img/logo.png')

    # fix telephone mask
    txt = txt.replace('+551****6288', '+55-11-95434-6288')

    # fix missing pt-BR language tags
    txt = txt.replace('["Portuguese", "English"]', '["pt-BR", "en"]')

    # normalize city names in titles/meta
    for slug, name in city_fixes.items():
        txt = txt.replace(f' em {slug.title()}', f' em {name}')
        txt = txt.replace(f' em {slug.replace("-", " ").title()}', f' em {name}')

    if txt != original:
        f.write_text(txt, encoding='utf-8')
        print(f'fixed {f}')

print('done')
