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
        'title': 'Apartamento 3 quartos Mongaguá',
        'description': 'Apartamento 3 quartos Mongaguá: lazer completo, fácil acesso à orla e ótimo custo-benefício.',
        'city': 'mongagua',
        'type': 'apartamento',
        'slug': 'apartamento-3-quartos-mongagua',
        'price': 'R$ 300.000–520.000',
        'price_raw': '410000',
        'bedrooms': '3–4',
        'area': '95–140 m²',
        'image': 'https://praia.digital/img/mon-ap-compacto.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%203%20quartos%20Mongagu%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Casa condomínio fechado Peruíbe',
        'description': 'Casa condomínio fechado Peruíbe: segurança, lazer e tranquilidade no extremo sul.',
        'city': 'peruibe',
        'type': 'casa',
        'slug': 'casa-condominio-fechado-peruibe',
        'price': 'R$ 520.000–780.000',
        'price_raw': '650000',
        'bedrooms': '3–4',
        'area': '120–170 m²',
        'image': 'https://praia.digital/img/per-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20condom%C3%ADnio%20fechado%20Peru%C3%ADbe&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Sobrado condomínio Mongaguá',
        'description': 'Sobrado condomínio Mongaguá: lazer completo, segurança e fácil acesso à praia.',
        'city': 'mongagua',
        'type': 'sobrado',
        'slug': 'sobrado-condominio-mongagua',
        'price': 'R$ 450.000–680.000',
        'price_raw': '560000',
        'bedrooms': '3–4',
        'area': '110–160 m²',
        'image': 'https://praia.digital/img/mon-ap-compacto.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%20condom%C3%ADnio%20Mongagu%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Sobrado condomínio São Vicente',
        'description': 'Sobrado condomínio São Vicente: área de lazer, segurança e ótima valorização.',
        'city': 'sao-vicente',
        'type': 'sobrado',
        'slug': 'sobrado-condominio-sao-vicente',
        'price': 'R$ 580.000–880.000',
        'price_raw': '720000',
        'bedrooms': '3–4',
        'area': '120–170 m²',
        'image': 'https://praia.digital/img/sv-cobertura-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%20condom%C3%ADnio%20S%C3%A3o%20Vicente&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Cobertura vista mar Peruíbe',
        'description': 'Cobertura vista mar Peruíbe: terraço panorâmico, piscina e lazer completo.',
        'city': 'peruibe',
        'type': 'cobertura',
        'slug': 'cobertura-vista-mar-peruibe',
        'price': 'R$ 780.000–1.150.000',
        'price_raw': '960000',
        'bedrooms': '3–4',
        'area': '160–220 m²',
        'image': 'https://praia.digital/img/per-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20vista%20mar%20Peru%C3%ADbe&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Cobertura vista mar Itanhaém',
        'description': 'Cobertura vista mar Itanhaém: sacada panorâmica, piscina e fácil acesso à praia.',
        'city': 'itanhaem',
        'type': 'cobertura',
        'slug': 'cobertura-vista-mar-itanhaem',
        'price': 'R$ 650.000–950.000',
        'price_raw': '800000',
        'bedrooms': '3–4',
        'area': '150–210 m²',
        'image': 'https://praia.digital/img/it-casa-terrea.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20vista%20mar%20Itanha%C3%A9m&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Terreno loteamento Mongaguá',
        'description': 'Terreno loteamento Mongaguá: plano, documentação regular e boa valorização.',
        'city': 'mongagua',
        'type': 'terreno',
        'slug': 'terreno-loteamento-mongagua',
        'price': 'R$ 160.000–280.000',
        'price_raw': '220000',
        'bedrooms': '',
        'area': '180–350 m²',
        'image': 'https://praia.digital/img/mon-ap-compacto.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Terreno%20loteamento%20Mongagu%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Terreno loteamento Itanhaém',
        'description': 'Terreno loteamento Itanhaém: infraestrutura pronta, topografia plana e potencial.',
        'city': 'itanhaem',
        'type': 'terreno',
        'slug': 'terreno-loteamento-itanhaem',
        'price': 'R$ 180.000–320.000',
        'price_raw': '250000',
        'bedrooms': '',
        'area': '200–400 m²',
        'image': 'https://praia.digital/img/it-casa-terrea.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Terreno%20loteamento%20Itanha%C3%A9m&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Studio investimento Bertioga',
        'description': 'Studio investimento Bertioga: alta liquidez, fácil locação e contato com natureza.',
        'city': 'bertioga',
        'type': 'studio',
        'slug': 'studio-investimento-bertioga',
        'price': 'R$ 180.000–320.000',
        'price_raw': '250000',
        'bedrooms': '1',
        'area': '25–42 m²',
        'image': 'https://praia.digital/img/berta-alto-padrao.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Studio%20investimento%20Bertioga&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Studio investimento Mongaguá',
        'description': 'Studio investimento Mongaguá: fácil locação, alta procura e ótimo retorno.',
        'city': 'mongagua',
        'type': 'studio',
        'slug': 'studio-investimento-mongagua',
        'price': 'R$ 170.000–300.000',
        'price_raw': '235000',
        'bedrooms': '1',
        'area': '24–40 m²',
        'image': 'https://praia.digital/img/mon-ap-compacto.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Studio%20investimento%20Mongagu%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Flat centro Bertioga',
        'description': 'Flat centro Bertioga: compacto, bem localizado e ideal para temporada.',
        'city': 'bertioga',
        'type': 'flat',
        'slug': 'flat-centro-bertioga',
        'price': 'R$ 190.000–320.000',
        'price_raw': '255000',
        'bedrooms': '1',
        'area': '24–40 m²',
        'image': 'https://praia.digital/img/berta-alto-padrao.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Flat%20centro%20Bertioga&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Chalé pé na areia Bertioga',
        'description': 'Chalé pé na areia Bertioga: charme, tranquilidade e contato direto com a natureza.',
        'city': 'bertioga',
        'type': 'chale',
        'slug': 'chale-pe-na-areia-bertioga',
        'price': 'R$ 380.000–620.000',
        'price_raw': '500000',
        'bedrooms': '2–3',
        'area': '60–100 m²',
        'image': 'https://praia.digital/img/berta-alto-padrao.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Chal%C3%A9%20p%C3%A9%20na%20areia%20Bertioga&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
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
