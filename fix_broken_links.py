import os, re, sys

BASE = os.getcwd()

fixes = [
    ('guia-como-comprar-imovel-litoral.html', {'../encontrar-imovel.html': './encontrar-imovel.html'}),
    ('guia-como-comprar-imovel-temporada-litoral.html', {'../guia-como-comprar-imovel-litoral.html': './guia-como-comprar-imovel-litoral.html'}),
    ('guia-investidor-imovel-litoral.html', {
        '../guia-como-comprar-imovel-temporada-litoral.html': './guia-como-comprar-imovel-temporada-litoral.html',
        '../guia-como-comprar-imovel-litoral.html': './guia-como-comprar-imovel-litoral.html',
        '../servicos/consultoria-proptech.html': './servicos/consultoria-proptech.html',
    }),
    ('lgpd-imobiliarias-litoral-2026.html', {'../politica-privacidade.html': './politica-privacidade.html'}),
]

anfitrioes_map = {
    'tutoriais-airbnb.html': 'tutoriais-anfitrioes.html',
    'checklists-airbnb.html': 'checklists-anfitrioes.html',
    'diagnostico-airbnb.html': 'diagnosticos-anfitrioes.html',
    'dados-mercado-airbnb.html': 'diagnosticos-anfitrioes.html',
    'fotos-videos-booking.html': 'diagnosticos-anfitrioes.html',
    'descricao-booking.html': 'diagnosticos-anfitrioes.html',
    'diagnostico-booking.html': 'diagnosticos-anfitrioes.html',
    'integracoes-booking.html': 'diagnosticos-anfitrioes.html',
    'treinamentos-pricelabs.html': 'diagnosticos-anfitrioes.html',
    'testes-pricelabs.html': 'diagnosticos-anfitrioes.html',
    'checklist-pricelabs.html': 'diagnosticos-anfitrioes.html',
    'integracao-pricelabs.html': 'diagnosticos-anfitrioes.html',
    'templates-stays.html': 'diagnosticos-anfitrioes.html',
    'tutoriais-stays.html': 'tutoriais-anfitrioes.html',
}

imoveis_map = {
    'imoveis/studio-moderno-praia-grande.html': 'imoveis/apartamento-1-quartos-praia-grande.html',
    'imoveis/casa-duplex-guaruja.html': 'imoveis/apartamento-2-quartos-guaruja.html',
    'imoveis/cobertura-duplex-sao-vicente.html': 'imoveis/apartamento-3-quartos-sao-vicente.html',
    'imoveis/apartamento-compacto-mongagua.html': 'imoveis/apartamento-1-quartos-mongagua.html',
    'imoveis/sobrado-geminado-peruibe.html': 'imoveis/apartamento-2-quartos-peruibe.html',
    'imoveis/apartamento-alto-padrao-bertioga.html': 'imoveis/apartamento-3-quartos-bertioga.html',
}

def patch_file(rel_path, mapping):
    path = os.path.join(BASE, rel_path)
    if not os.path.exists(path):
        print('SKIP missing', rel_path)
        return 0
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    orig = content
    for old, new in mapping.items():
        if old in content:
            content = content.replace(old, new)
    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('PATCHED', rel_path, '->', list(mapping.values())[0])
        return 1
    print('NOCHANGE', rel_path)
    return 0

count = 0
for rel, mapping in fixes:
    count += patch_file(rel, mapping)

# anfitrioes
for fname in ['anfitrioes/central-airbnb.html','anfitrioes/central-booking.html','anfitrioes/central-priceplabs.html','anfitrioes/central-stays.html']:
    count += patch_file(fname, anfitrioes_map)

# imoveis.html
count += patch_file('imoveis.html', imoveis_map)

# investidores.html
count += patch_file('investidores.html', {'investidores/plano-7-dias.html': 'investidores/index.html'})

print('Total arquivos alterados:', count)
