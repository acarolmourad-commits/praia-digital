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
        'title': 'Casa vila Mongaguá',
        'description': 'Casa vila Mongaguá: tranquilidade, segurança e ótima localização.',
        'city': 'mongagua',
        'type': 'casa',
        'slug': 'casa-vila-mongagua',
        'price': 'R$ 320.000–520.000',
        'price_raw': '420000',
        'bedrooms': '2–3',
        'area': '90–135 m²',
        'image': 'https://praia.digital/img/mon-ap-compacto.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20vila%20Mongagu%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Casa vila Peruíbe',
        'description': 'Casa vila Peruíbe: sossego, segurança e acesso fácil à praia.',
        'city': 'peruibe',
        'type': 'casa',
        'slug': 'casa-vila-peruibe',
        'price': 'R$ 280.000–460.000',
        'price_raw': '370000',
        'bedrooms': '2–3',
        'area': '85–130 m²',
        'image': 'https://praia.digital/img/per-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20vila%20Peru%C3%ADbe&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Casa vila Caraguatatuba',
        'description': 'Casa vila Caraguatatuba: lazer, tranquilidade e contato com a natureza.',
        'city': 'caraguatatuba',
        'type': 'casa',
        'slug': 'casa-vila-caraguatatuba',
        'price': 'R$ 380.000–620.000',
        'price_raw': '500000',
        'bedrooms': '3',
        'area': '100–150 m²',
        'image': 'https://praia.digital/img/cara-cobertura.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20vila%20Caraguatatuba&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Casa vila Ubatuba',
        'description': 'Casa vila Ubatuba: sossego, lazer e proximidade com a orla.',
        'city': 'ubatuba',
        'type': 'casa',
        'slug': 'casa-vila-ubatuba',
        'price': 'R$ 420.000–680.000',
        'price_raw': '550000',
        'bedrooms': '3',
        'area': '110–160 m²',
        'image': 'https://praia.digital/img/ubatuba-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20vila%20Ubatuba&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento duplex Bertioga',
        'description': 'Apartamento duplex Bertioga: amplo, com terraço e vista mar.',
        'city': 'bertioga',
        'type': 'apartamento',
        'slug': 'apartamento-duplex-bertioga',
        'price': 'R$ 620.000–920.000',
        'price_raw': '770000',
        'bedrooms': '3',
        'area': '120–170 m²',
        'image': 'https://praia.digital/img/berta-alto-padrao.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20duplex%20Bertioga&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento duplex Mongaguá',
        'description': 'Apartamento duplex Mongaguá: espaço amplo, lazer e fácil acesso à praia.',
        'city': 'mongagua',
        'type': 'apartamento',
        'slug': 'apartamento-duplex-mongagua',
        'price': 'R$ 380.000–580.000',
        'price_raw': '480000',
        'bedrooms': '2–3',
        'area': '100–150 m²',
        'image': 'https://praia.digital/img/mon-ap-compacto.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20duplex%20Mongagu%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento duplex Caraguatatuba',
        'description': 'Apartamento duplex Caraguatatuba: amplo, lazer e vista mar.',
        'city': 'caraguatatuba',
        'type': 'apartamento',
        'slug': 'apartamento-duplex-caraguatatuba',
        'price': 'R$ 450.000–680.000',
        'price_raw': '560000',
        'bedrooms': '2–3',
        'area': '105–155 m²',
        'image': 'https://praia.digital/img/cara-cobertura.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20duplex%20Caraguatatuba&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento frente mar Peruíbe',
        'description': 'Apartamento frente mar Peruíbe: varanda, lazer e tranquilidade.',
        'city': 'peruibe',
        'type': 'apartamento',
        'slug': 'apartamento-frente-mar-peruibe',
        'price': 'R$ 360.000–550.000',
        'price_raw': '460000',
        'bedrooms': '2–3',
        'area': '75–110 m²',
        'image': 'https://praia.digital/img/per-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20frente%20mar%20Peru%C3%ADbe&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento frente mar Caraguatatuba',
        'description': 'Apartamento frente mar Caraguatatuba: vista definitiva, lazer e fácil acesso.',
        'city': 'caraguatatuba',
        'type': 'apartamento',
        'slug': 'apartamento-frente-mar-caraguatatuba',
        'price': 'R$ 420.000–660.000',
        'price_raw': '540000',
        'bedrooms': '2–3',
        'area': '80–115 m²',
        'image': 'https://praia.digital/img/cara-cobertura.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20frente%20mar%20Caraguatatuba&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Cobertura duplex Guarujá',
        'description': 'Cobertura duplex Guarujá: terraço panorâmico, piscina e lazer completo.',
        'city': 'guaruja',
        'type': 'cobertura',
        'slug': 'cobertura-duplex-guaruja',
        'price': 'R$ 980.000–1.450.000',
        'price_raw': '1200000',
        'bedrooms': '3–4',
        'area': '175–240 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20duplex%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Cobertura duplex Ubatuba',
        'description': 'Cobertura duplex Ubatuba: vista mar, terraço e lazer completo.',
        'city': 'ubatuba',
        'type': 'cobertura',
        'slug': 'cobertura-duplex-ubatuba',
        'price': 'R$ 920.000–1.380.000',
        'price_raw': '1150000',
        'bedrooms': '3–4',
        'area': '170–230 m²',
        'image': 'https://praia.digital/img/ubatuba-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20duplex%20Ubatuba&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
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
