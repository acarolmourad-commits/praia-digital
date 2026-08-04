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
        'title': 'Apartamento 3 quartos Itanhaém',
        'description': 'Apartamento 3 quartos Itanhaém: lazer completo, fácil acesso à praia e ótimo custo-benefício.',
        'city': 'itanhaem',
        'type': 'apartamento',
        'slug': 'apartamento-3-quartos-itanhaem',
        'price': 'R$ 350.000–600.000',
        'price_raw': '480000',
        'bedrooms': '3–4',
        'area': '95–140 m²',
        'image': 'https://praia.digital/img/it-casa-terrea.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%203%20quartos%20Itanha%C3%A9m&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento 3 quartos Praia Grande',
        'description': 'Apartamento 3 quartos Praia Grande: conforto, lazer completo e fácil acesso à via Imigrantes.',
        'city': 'praia-grande',
        'type': 'apartamento',
        'slug': 'apartamento-3-quartos-praia-grande',
        'price': 'R$ 350.000–580.000',
        'price_raw': '460000',
        'bedrooms': '3–4',
        'area': '90–135 m²',
        'image': 'https://praia.digital/img/pg-studio-moderno.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%203%20quartos%20Praia%20Grande&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento 3 quartos São Vicente',
        'description': 'Apartamento 3 quartos São Vicente: sacada gourmet, lazer completo e vista mar parcial.',
        'city': 'sao-vicente',
        'type': 'apartamento',
        'slug': 'apartamento-3-quartos-sao-vicente',
        'price': 'R$ 380.000–620.000',
        'price_raw': '500000',
        'bedrooms': '3–4',
        'area': '95–140 m²',
        'image': 'https://praia.digital/img/sv-cobertura-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%203%20quartos%20S%C3%A3o%20Vicente&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento 3 quartos Peruíbe',
        'description': 'Apartamento 3 quartos Peruíbe: conforto, lazer e tranquilidade no extremo sul do litoral.',
        'city': 'peruibe',
        'type': 'apartamento',
        'slug': 'apartamento-3-quartos-peruibe',
        'price': 'R$ 280.000–480.000',
        'price_raw': '380000',
        'bedrooms': '3–4',
        'area': '90–135 m²',
        'image': 'https://praia.digital/img/per-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%203%20quartos%20Peru%C3%ADbe&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Casa condomínio fechado Praia Grande',
        'description': 'Casa condomínio fechado Praia Grande: segurança, lazer e fácil acesso às praias.',
        'city': 'praia-grande',
        'type': 'casa',
        'slug': 'casa-condominio-fechado-praia-grande',
        'price': 'R$ 580.000–850.000',
        'price_raw': '720000',
        'bedrooms': '3–4',
        'area': '130–190 m²',
        'image': 'https://praia.digital/img/pg-studio-moderno.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20condom%C3%ADnio%20fechado%20Praia%20Grande&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Casa condomínio fechado São Vicente',
        'description': 'Casa condomínio fechado São Vicente: área verde, segurança e ótima valorização.',
        'city': 'sao-vicente',
        'type': 'casa',
        'slug': 'casa-condominio-fechado-sao-vicente',
        'price': 'R$ 620.000–900.000',
        'price_raw': '760000',
        'bedrooms': '3–4',
        'area': '130–190 m²',
        'image': 'https://praia.digital/img/sv-cobertura-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Casa%20condom%C3%ADnio%20fechado%20S%C3%A3o%20Vicente&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Sobrado condomínio Guarujá',
        'description': 'Sobrado condomínio Guarujá: lazer, segurança e proximidade com a orla.',
        'city': 'guaruja',
        'type': 'sobrado',
        'slug': 'sobrado-condominio-guaruja',
        'price': 'R$ 720.000–1.050.000',
        'price_raw': '880000',
        'bedrooms': '3–4',
        'area': '140–200 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%20condom%C3%ADnio%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Sobrado condomínio Peruíbe',
        'description': 'Sobrado condomínio Peruíbe: área de lazer, churrasqueira e espaço pet-friendly.',
        'city': 'peruibe',
        'type': 'sobrado',
        'slug': 'sobrado-condominio-peruibe',
        'price': 'R$ 500.000–750.000',
        'price_raw': '620000',
        'bedrooms': '3–4',
        'area': '120–170 m²',
        'image': 'https://praia.digital/img/per-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%20condom%C3%ADnio%20Peru%C3%ADbe&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Studio investimento Praia Grande',
        'description': 'Studio investimento Praia Grande: alta liquidez, fácil locação e ótimo custo-benefício.',
        'city': 'praia-grande',
        'type': 'studio',
        'slug': 'studio-investimento-praia-grande',
        'price': 'R$ 200.000–340.000',
        'price_raw': '270000',
        'bedrooms': '1',
        'area': '28–45 m²',
        'image': 'https://praia.digital/img/pg-studio-moderno.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Studio%20investimento%20Praia%20Grande&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Cobertura vista mar Guarujá',
        'description': 'Cobertura vista mar Guarujá: terraço panorâmico, piscina privativa e lazer completo.',
        'city': 'guaruja',
        'type': 'cobertura',
        'slug': 'cobertura-vista-mar-guaruja',
        'price': 'R$ 1.050.000–1.500.000',
        'price_raw': '1280000',
        'bedrooms': '3–4',
        'area': '170–235 m²',
        'image': 'https://praia.digital/img/gua-casa-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20vista%20mar%20Guaruj%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Cobertura vista mar Bertioga',
        'description': 'Cobertura vista mar Bertioga: terraço gourmet, piscina e acabamento premium.',
        'city': 'bertioga',
        'type': 'cobertura',
        'slug': 'cobertura-vista-mar-bertioga',
        'price': 'R$ 980.000–1.420.000',
        'price_raw': '1200000',
        'bedrooms': '3–4',
        'area': '170–235 m²',
        'image': 'https://praia.digital/img/berta-alto-padrao.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20vista%20mar%20Bertioga&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Cobertura vista mar São Vicente',
        'description': 'Cobertura vista mar São Vicente: sacada panorâmica, lazer completo e 3 vagas.',
        'city': 'sao-vicente',
        'type': 'cobertura',
        'slug': 'cobertura-vista-mar-sao-vicente',
        'price': 'R$ 950.000–1.380.000',
        'price_raw': '1160000',
        'bedrooms': '3–4',
        'area': '170–230 m²',
        'image': 'https://praia.digital/img/sv-cobertura-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20vista%20mar%20S%C3%A3o%20Vicente&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Terreno loteamento Santos',
        'description': 'Terreno loteamento Santos: documentação regular, topografia plana, excelente para construção.',
        'city': 'santos',
        'type': 'terreno',
        'slug': 'terreno-loteamento-santos',
        'price': 'R$ 220.000–380.000',
        'price_raw': '300000',
        'bedrooms': '',
        'area': '180–360 m²',
        'image': 'https://praia.digital/img/santos-apartamento-vista-mar.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Terreno%20loteamento%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
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
