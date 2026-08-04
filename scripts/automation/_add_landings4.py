import csv
from pathlib import Path

repo = Path('.').resolve()
csv_path = repo / 'imoveis' / 'landings.csv'

with open(csv_path, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    existing = list(reader)

updates = {r['slug']: r for r in existing if r.get('slug')}

new_rows = [
    {
        'title': 'Flat centro Santos',
        'description': 'Flat centro Santos: compacto, bem localizado, ideal para profissionais e temporada.',
        'city': 'santos',
        'type': 'flat',
        'slug': 'flat-centro-santos',
        'price': 'R$ 220.000–380.000',
        'price_raw': '300000',
        'bedrooms': '1',
        'area': '28–45 m²',
        'image': 'https://praia.digital/img/santos-apartamento-vista-mar.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Flat%20centro%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Flat centro Guarujá',
        'description': 'Flat centro Guarujá: prático, próximo à praia e fácil de alugar.',
        'city': 'guaruja',
        'type': 'flat',
        'slug': 'flat-centro-guaruja',
        'price': 'R$ 200.000–350.000',
        'price_raw': '270000',
        'bedrooms': '1',
        'area': '25–42 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Flat%20centro%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Chalé pé na areia Peruíbe',
        'description': 'Chalé pé na areia Peruíbe: charme, tranquilidade e acesso direto ao mar.',
        'city': 'peruibe',
        'type': 'chale',
        'slug': 'chale-pe-na-areia-peruibe',
        'price': 'R$ 350.000–580.000',
        'price_raw': '460000',
        'bedrooms': '2–3',
        'area': '60–100 m²',
        'image': 'https://praia.digital/img/per-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Chal%C3%A9%20p%C3%A9%20na%20areia%20Peru%C3%ADbe&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Chalé centro Bertioga',
        'description': 'Chalé centro Bertioga: aconchego, lazer e proximidade com a natureza.',
        'city': 'bertioga',
        'type': 'chale',
        'slug': 'chale-centro-bertioga',
        'price': 'R$ 280.000–450.000',
        'price_raw': '360000',
        'bedrooms': '2',
        'area': '55–90 m²',
        'image': 'https://praia.digital/img/berta-alto-padrao.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Chal%C3%A9%20centro%20Bertioga&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento garden Santos',
        'description': 'Apartamento garden Santos: quintal privativo, lazer completo e acesso à praia.',
        'city': 'santos',
        'type': 'apartamento',
        'slug': 'apartamento-garden-santos',
        'price': 'R$ 650.000–950.000',
        'price_raw': '800000',
        'bedrooms': '2–3',
        'area': '85–120 m²',
        'image': 'https://praia.digital/img/santos-apartamento-vista-mar.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20garden%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento mobiliado Guarujá',
        'description': 'Apartamento mobiliado Guarujá: pronto para morar ou alugar por temporada.',
        'city': 'guaruja',
        'type': 'apartamento',
        'slug': 'apartamento-mobiliado-guaruja',
        'price': 'R$ 420.000–680.000',
        'price_raw': '550000',
        'bedrooms': '2–3',
        'area': '70–110 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20mobiliado%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Casa térrea Itanhaém',
        'description': 'Casa térrea Itanhaém: acessibilidade, quintal e lazer para a família toda.',
        'city': 'itanhaem',
        'type': 'casa',
        'slug': 'casa-terrea-itanhaem',
        'price': 'R$ 380.000–620.000',
        'price_raw': '500000',
        'bedrooms': '3',
        'area': '100–150 m²',
        'image': 'https://praia.digital/img/it-casa-terrea.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20t%C3%A9rrea%20Itanha%C3%A9m&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Casa térrea Peruíbe',
        'description': 'Casa térrea Peruíbe: tranquilidade, quintal e fácil acesso à praia.',
        'city': 'peruibe',
        'type': 'casa',
        'slug': 'casa-terrea-peruibe',
        'price': 'R$ 320.000–520.000',
        'price_raw': '420000',
        'bedrooms': '2–3',
        'area': '90–140 m²',
        'image': 'https://praia.digital/img/per-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20t%C3%A9rrea%20Peru%C3%ADbe&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Sobrado 3 quartos Santos',
        'description': 'Sobrado 3 quartos Santos: garagem coberta, churrasqueira e ótima localização.',
        'city': 'santos',
        'type': 'sobrado',
        'slug': 'sobrado-3-quartos-santos',
        'price': 'R$ 650.000–950.000',
        'price_raw': '800000',
        'bedrooms': '3–4',
        'area': '120–170 m²',
        'image': 'https://praia.digital/img/santos-apartamento-vista-mar.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%203%20quartos%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Sobrado 3 quartos Guarujá',
        'description': 'Sobrado 3 quartos Guarujá: lazer, segurança e proximidade com a orla.',
        'city': 'guaruja',
        'type': 'sobrado',
        'slug': 'sobrado-3-quartos-guaruja',
        'price': 'R$ 680.000–1.000.000',
        'price_raw': '840000',
        'bedrooms': '3–4',
        'area': '130–190 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%203%20quartos%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Cobertura vista mar Praia Grande',
        'description': 'Cobertura vista mar Praia Grande: terraço panorâmico, piscina e lazer completo.',
        'city': 'praia-grande',
        'type': 'cobertura',
        'slug': 'cobertura-vista-mar-praia-grande',
        'price': 'R$ 780.000–1.200.000',
        'price_raw': '980000',
        'bedrooms': '3–4',
        'area': '160–220 m²',
        'image': 'https://praia.digital/img/pg-studio-moderno.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20vista%20mar%20Praia%20Grande&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Terreno plano Santos',
        'description': 'Terreno plano Santos: documentação regular, topografia plana, excelente para construir.',
        'city': 'santos',
        'type': 'terreno',
        'slug': 'terreno-plano-santos',
        'price': 'R$ 250.000–420.000',
        'price_raw': '340000',
        'bedrooms': '',
        'area': '180–350 m²',
        'image': 'https://praia.digital/img/santos-apartamento-vista-mar.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Terreno%20plano%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
]

merged = {r['slug']: r for r in existing}
new_count = 0
for r in new_rows:
    slug = r['slug']
    if slug not in merged:
        merged[slug] = r
        new_count += 1
    else:
        merged[slug].update(r)

with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in merged.values():
        writer.writerow(r)

print('new_count', new_count)
print('csv_rows_now', len(merged))
