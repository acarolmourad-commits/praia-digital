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
        'title': 'Apartamento 3 quartos Guarujá',
        'description': 'Apartamento 3 quartos Guarujá: lazer completo, fácil acesso à praia e áreas de entretenimento.',
        'city': 'guaruja',
        'type': 'apartamento',
        'slug': 'apartamento-3-quartos-guaruja',
        'price': 'R$ 620.000–950.000',
        'price_raw': '780000',
        'bedrooms': '3–4',
        'area': '100–150 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%203%20quartos%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento frente mar Santos',
        'description': 'Apartamento frente mar Santos: vista definitiva, sacada gourmet e lazer completo na orla.',
        'city': 'santos',
        'type': 'apartamento',
        'slug': 'apartamento-frente-mar-santos',
        'price': 'R$ 800.000–1.200.000',
        'price_raw': '950000',
        'bedrooms': '2–3',
        'area': '95–140 m²',
        'image': 'https://praia.digital/img/santos-apartamento-vista-mar.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20frente%20mar%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento suíte vista mar Guarujá',
        'description': 'Apartamento suíte vista mar Guarujá: sacada gourmet, piscina e 2 vagas de garagem.',
        'city': 'guaruja',
        'type': 'apartamento',
        'slug': 'apartamento-suite-vista-mar-guaruja',
        'price': 'R$ 720.000–1.050.000',
        'price_raw': '880000',
        'bedrooms': '2–3',
        'area': '90–135 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20su%C3%ADte%20vista%20mar%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento temporada Praia Grande',
        'description': 'Apartamento temporada Praia Grande: estrutura completa para locação curta e alta procura.',
        'city': 'praia-grande',
        'type': 'apartamento',
        'slug': 'apartamento-temporada-praia-grande',
        'price': 'R$ 240.000–380.000',
        'price_raw': '310000',
        'bedrooms': '1–2',
        'area': '45–75 m²',
        'image': 'https://praia.digital/img/pg-studio-moderno.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20temporada%20Praia%20Grande&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Casa condomínio fechado Santos',
        'description': 'Casa condomínio fechado Santos: segurança 24h, área de lazer e localização tranquila.',
        'city': 'santos',
        'type': 'casa',
        'slug': 'casa-condominio-fechado-santos',
        'price': 'R$ 750.000–1.100.000',
        'price_raw': '900000',
        'bedrooms': '3–4',
        'area': '140–200 m²',
        'image': 'https://praia.digital/img/santos-apartamento-vista-mar.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20condom%C3%ADnio%20fechado%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Casa condomínio fechado Guarujá',
        'description': 'Casa condomínio fechado Guarujá: lazer completo, segurança e proximidade com a orla.',
        'city': 'guaruja',
        'type': 'casa',
        'slug': 'casa-condominio-fechado-guaruja',
        'price': 'R$ 680.000–980.000',
        'price_raw': '820000',
        'bedrooms': '3–4',
        'area': '130–190 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20condom%C3%ADnio%20fechado%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Casa pé na areia Guarujá',
        'description': 'Casa pé na areia Guarujá: acesso direto à praia, quintal e perfeita para temporada.',
        'city': 'guaruja',
        'type': 'casa',
        'slug': 'casa-pe-na-areia-guaruja',
        'price': 'R$ 580.000–860.000',
        'price_raw': '720000',
        'bedrooms': '2–4',
        'area': '110–180 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20p%C3%A9%20na%20areia%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Sobrado condomínio Santos',
        'description': 'Sobrado condomínio Santos: área de lazer, churrasqueira e espaço pet-friendly.',
        'city': 'santos',
        'type': 'sobrado',
        'slug': 'sobrado-condominio-santos',
        'price': 'R$ 720.000–1.050.000',
        'price_raw': '880000',
        'bedrooms': '3–4',
        'area': '140–200 m²',
        'image': 'https://praia.digital/img/santos-apartamento-vista-mar.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%20condom%C3%ADnio%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Sobrado condomínio Praia Grande',
        'description': 'Sobrado condomínio Praia Grande: lazer, segurança e fácil acesso às praias.',
        'city': 'praia-grande',
        'type': 'sobrado',
        'slug': 'sobrado-condominio-praia-grande',
        'price': 'R$ 480.000–720.000',
        'price_raw': '600000',
        'bedrooms': '3',
        'area': '120–170 m²',
        'image': 'https://praia.digital/img/pg-studio-moderno.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%20condom%C3%ADnio%20Praia%20Grande&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Terreno loteamento Bertioga',
        'description': 'Terreno loteamento Bertioga: documentação regular, topografia plana, boa valorização.',
        'city': 'bertioga',
        'type': 'terreno',
        'slug': 'terreno-loteamento-bertioga',
        'price': 'R$ 200.000–350.000',
        'price_raw': '270000',
        'bedrooms': '',
        'area': '200–400 m²',
        'image': 'https://praia.digital/img/berta-alto-padrao.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Terreno%20loteamento%20Bertioga&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Terreno loteamento Guarujá',
        'description': 'Terreno loteamento Guarujá: plano, infraestrutura pronta e excelente potencial.',
        'city': 'guaruja',
        'type': 'terreno',
        'slug': 'terreno-loteamento-guaruja',
        'price': 'R$ 220.000–380.000',
        'price_raw': '300000',
        'bedrooms': '',
        'area': '180–360 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Terreno%20loteamento%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Studio investimento Guarujá',
        'description': 'Studio investimento Guarujá: alta liquidez, fácil locação e ótima rentabilidade.',
        'city': 'guaruja',
        'type': 'studio',
        'slug': 'studio-investimento-guaruja',
        'price': 'R$ 240.000–400.000',
        'price_raw': '320000',
        'bedrooms': '1',
        'area': '30–48 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Studio%20investimento%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Cobertura duplex Guarujá',
        'description': 'Cobertura duplex Guarujá: terraço privativo, piscina e vista mar incrível.',
        'city': 'guaruja',
        'type': 'cobertura',
        'slug': 'cobertura-duplex-guaruja',
        'price': 'R$ 950.000–1.400.000',
        'price_raw': '1180000',
        'bedrooms': '3–4',
        'area': '170–240 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20duplex%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento suíte vista mar Bertioga',
        'description': 'Apartamento suíte vista mar Bertioga: lazer completo, varanda e fácil acesso à natureza.',
        'city': 'bertioga',
        'type': 'apartamento',
        'slug': 'apartamento-suite-vista-mar-bertioga',
        'price': 'R$ 550.000–820.000',
        'price_raw': '680000',
        'bedrooms': '2–3',
        'area': '85–130 m²',
        'image': 'https://praia.digital/img/berta-alto-padrao.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20su%C3%ADte%20vista%20mar%20Bertioga&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
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
