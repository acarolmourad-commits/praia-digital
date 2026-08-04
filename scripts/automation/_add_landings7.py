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
        'title': 'Casa condomínio fechado Caraguatatuba',
        'description': 'Casa condomínio fechado Caraguatatuba: segurança, lazer e contato com a natureza.',
        'city': 'caraguatatuba',
        'type': 'casa',
        'slug': 'casa-condominio-fechado-caraguatatuba',
        'price': 'R$ 580.000–850.000',
        'price_raw': '720000',
        'bedrooms': '3–4',
        'area': '130–190 m²',
        'image': 'https://praia.digital/img/cara-cobertura.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20condom%C3%ADnio%20fechado%20Caraguatatuba&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Sobrado condomínio Ubatuba',
        'description': 'Sobrado condomínio Ubatuba: lazer, segurança e proximidade com a praia.',
        'city': 'ubatuba',
        'type': 'sobrado',
        'slug': 'sobrado-condominio-ubatuba',
        'price': 'R$ 650.000–950.000',
        'price_raw': '800000',
        'bedrooms': '3–4',
        'area': '130–190 m²',
        'image': 'https://praia.digital/img/ubatuba-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%20condom%C3%ADnio%20Ubatuba&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Sobrado condomínio Ilhabela',
        'description': 'Sobrado condomínio Ilhabela: natureza, lazer e segurança em uma ilha paradisíaca.',
        'city': 'ilhabela',
        'type': 'sobrado',
        'slug': 'sobrado-condominio-ilhabela',
        'price': 'R$ 720.000–1.100.000',
        'price_raw': '900000',
        'bedrooms': '3–4',
        'area': '140–200 m²',
        'image': 'https://praia.digital/img/ilha-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%20condom%C3%ADnio%20Ilhabela&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento temporada Bertioga',
        'description': 'Apartamento temporada Bertioga: estrutura completa para locação curta e alta procura.',
        'city': 'bertioga',
        'type': 'apartamento',
        'slug': 'apartamento-temporada-bertioga',
        'price': 'R$ 280.000–450.000',
        'price_raw': '360000',
        'bedrooms': '2–3',
        'area': '65–100 m²',
        'image': 'https://praia.digital/img/berta-alto-padrao.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20temporada%20Bertioga&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento temporada Caraguatatuba',
        'description': 'Apartamento temporada Caraguatatuba: conforto, lazer e fácil acesso às praias.',
        'city': 'caraguatatuba',
        'type': 'apartamento',
        'slug': 'apartamento-temporada-caraguatatuba',
        'price': 'R$ 260.000–420.000',
        'price_raw': '340000',
        'bedrooms': '2–3',
        'area': '60–95 m²',
        'image': 'https://praia.digital/img/cara-cobertura.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20temporada%20Caraguatatuba&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento temporada Ubatuba',
        'description': 'Apartamento temporada Ubatuba: vista mar, lazer e experiência única no litoral norte.',
        'city': 'ubatuba',
        'type': 'apartamento',
        'slug': 'apartamento-temporada-ubatuba',
        'price': 'R$ 240.000–400.000',
        'price_raw': '320000',
        'bedrooms': '2–3',
        'area': '60–95 m²',
        'image': 'https://praia.digital/img/ubatuba-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20temporada%20Ubatuba&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Casa térrea Mongaguá',
        'description': 'Casa térrea Mongaguá: acessibilidade, quintal e lazer para a família toda.',
        'city': 'mongagua',
        'type': 'casa',
        'slug': 'casa-terrea-mongagua',
        'price': 'R$ 340.000–520.000',
        'price_raw': '430000',
        'bedrooms': '2–3',
        'area': '90–135 m²',
        'image': 'https://praia.digital/img/mon-ap-compacto.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20t%C3%A9rrea%20Mongagu%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Casa térrea São Vicente',
        'description': 'Casa térrea São Vicente: acessibilidade, quintal e ótima localização.',
        'city': 'sao-vicente',
        'type': 'casa',
        'slug': 'casa-terrea-sao-vicente',
        'price': 'R$ 420.000–650.000',
        'price_raw': '540000',
        'bedrooms': '2–3',
        'area': '95–140 m²',
        'image': 'https://praia.digital/img/sv-cobertura-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20t%C3%A9rrea%20S%C3%A3o%20Vicente&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Terreno loteamento Peruíbe',
        'description': 'Terreno loteamento Peruíbe: plano, documentação regular e potencial.',
        'city': 'peruibe',
        'type': 'terreno',
        'slug': 'terreno-loteamento-peruibe',
        'price': 'R$ 140.000–240.000',
        'price_raw': '190000',
        'bedrooms': '',
        'area': '200–400 m²',
        'image': 'https://praia.digital/img/per-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Terreno%20loteamento%20Peru%C3%ADbe&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Terreno loteamento Caraguatatuba',
        'description': 'Terreno loteamento Caraguatatuba: infraestrutura pronta e excelente potencial.',
        'city': 'caraguatatuba',
        'type': 'terreno',
        'slug': 'terreno-loteamento-caraguatatuba',
        'price': 'R$ 180.000–320.000',
        'price_raw': '250000',
        'bedrooms': '',
        'area': '250–500 m²',
        'image': 'https://praia.digital/img/cara-cobertura.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Terreno%20loteamento%20Caraguatatuba&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Terreno loteamento Ilhabela',
        'description': 'Terreno loteamento Ilhabela: natureza preservada e alto potencial de valorização.',
        'city': 'ilhabela',
        'type': 'terreno',
        'slug': 'terreno-loteamento-ilhabela',
        'price': 'R$ 220.000–400.000',
        'price_raw': '300000',
        'bedrooms': '',
        'area': '300–600 m²',
        'image': 'https://praia.digital/img/ilha-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Terreno%20loteamento%20Ilhabela&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Chalé pé na areia Guarujá',
        'description': 'Chalé pé na areia Guarujá: charme, conforto e acesso direto à praia.',
        'city': 'guaruja',
        'type': 'chale',
        'slug': 'chale-pe-na-areia-guaruja',
        'price': 'R$ 380.000–620.000',
        'price_raw': '500000',
        'bedrooms': '2–3',
        'area': '55–90 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Chal%C3%A9%20p%C3%A9%20na%20areia%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Chalé centro Ilhabela',
        'description': 'Chalé centro Ilhabela: aconchego, lazer e proximidade com a natureza.',
        'city': 'ilhabela',
        'type': 'chale',
        'slug': 'chale-centro-ilhabela',
        'price': 'R$ 320.000–520.000',
        'price_raw': '420000',
        'bedrooms': '2',
        'area': '50–80 m²',
        'image': 'https://praia.digital/img/ilha-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Chal%C3%A9%20centro%20Ilhabela&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
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
