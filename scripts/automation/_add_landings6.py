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
        'title': 'Apartamento frente mar São Vicente',
        'description': 'Apartamento frente mar São Vicente: varanda panorâmica, lazer completo e vista definitiva.',
        'city': 'sao-vicente',
        'type': 'apartamento',
        'slug': 'apartamento-frente-mar-sao-vicente',
        'price': 'R$ 480.000–720.000',
        'price_raw': '600000',
        'bedrooms': '2–3',
        'area': '75–110 m²',
        'image': 'https://praia.digital/img/sv-cobertura-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20frente%20mar%20S%C3%A3o%20Vicente&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento frente mar Praia Grande',
        'description': 'Apartamento frente mar Praia Grande: varanda gourmet, piscina e fácil acesso à orla.',
        'city': 'praia-grande',
        'type': 'apartamento',
        'slug': 'apartamento-frente-mar-praia-grande',
        'price': 'R$ 450.000–700.000',
        'price_raw': '580000',
        'bedrooms': '2–3',
        'area': '80–120 m²',
        'image': 'https://praia.digital/img/pg-studio-moderno.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20frente%20mar%20Praia%20Grande&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento frente mar Bertioga',
        'description': 'Apartamento frente mar Bertioga: varanda panorâmica, lazer e acesso direto à praia.',
        'city': 'bertioga',
        'type': 'apartamento',
        'slug': 'apartamento-frente-mar-bertioga',
        'price': 'R$ 520.000–780.000',
        'price_raw': '650000',
        'bedrooms': '2–3',
        'area': '85–125 m²',
        'image': 'https://praia.digital/img/berta-alto-padrao.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20frente%20mar%20Bertioga&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento suíte vista mar Praia Grande',
        'description': 'Apartamento suíte vista mar Praia Grande: sacada gourmet, lazer completo e vista panorâmica.',
        'city': 'praia-grande',
        'type': 'apartamento',
        'slug': 'apartamento-suite-vista-mar-praia-grande',
        'price': 'R$ 520.000–780.000',
        'price_raw': '650000',
        'bedrooms': '2–3',
        'area': '90–130 m²',
        'image': 'https://praia.digital/img/pg-studio-moderno.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20su%C3%ADte%20vista%20mar%20Praia%20Grande&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento suíte vista mar Itanhaém',
        'description': 'Apartamento suíte vista mar Itanhaém: sacada panorâmica, lazer e fácil acesso à praia.',
        'city': 'itanhaem',
        'type': 'apartamento',
        'slug': 'apartamento-suite-vista-mar-itanhaem',
        'price': 'R$ 420.000–680.000',
        'price_raw': '550000',
        'bedrooms': '2–3',
        'area': '85–125 m²',
        'image': 'https://praia.digital/img/it-casa-terrea.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20su%C3%ADte%20vista%20mar%20Itanha%C3%A9m&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento suíte vista mar Peruíbe',
        'description': 'Apartamento suíte vista mar Peruíbe: sacada gourmet, lazer completo e tranquilidade.',
        'city': 'peruibe',
        'type': 'apartamento',
        'slug': 'apartamento-suite-vista-mar-peruibe',
        'price': 'R$ 380.000–620.000',
        'price_raw': '500000',
        'bedrooms': '2–3',
        'area': '80–120 m²',
        'image': 'https://praia.digital/img/per-sobrado.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20su%C3%ADte%20vista%20mar%20Peru%C3%ADbe&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Cobertura vista mar Mongaguá',
        'description': 'Cobertura vista mar Mongaguá: terraço panorâmico, piscina e lazer completo.',
        'city': 'mongagua',
        'type': 'cobertura',
        'slug': 'cobertura-vista-mar-mongagua',
        'price': 'R$ 650.000–950.000',
        'price_raw': '800000',
        'bedrooms': '3–4',
        'area': '160–220 m²',
        'image': 'https://praia.digital/img/mon-ap-compacto.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20vista%20mar%20Mongagu%C3%A1&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Cobertura vista mar São Vicente',
        'description': 'Cobertura vista mar São Vicente: terraço panorâmico, lazer completo e 3 vagas.',
        'city': 'sao-vicente',
        'type': 'cobertura',
        'slug': 'cobertura-vista-mar-sao-vicente',
        'price': 'R$ 780.000–1.150.000',
        'price_raw': '960000',
        'bedrooms': '3–4',
        'area': '160–220 m²',
        'image': 'https://praia.digital/img/sv-cobertura-duplex.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20vista%20mar%20S%C3%A3o%20Vicente&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Cobertura vista mar Caraguatatuba',
        'description': 'Cobertura vista mar Caraguatatuba: terraço panorâmico, piscina e lazer completo.',
        'city': 'caraguatatuba',
        'type': 'cobertura',
        'slug': 'cobertura-vista-mar-caraguatatuba',
        'price': 'R$ 720.000–1.080.000',
        'price_raw': '900000',
        'bedrooms': '3–4',
        'area': '170–230 m²',
        'image': 'https://praia.digital/img/cara-cobertura.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20na%20Cobertura%20vista%20mar%20Caraguatatuba&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Sobrado 3 quartos Praia Grande',
        'description': 'Sobrado 3 quartos Praia Grande: garagem coberta, churrasqueira e fácil acesso à orla.',
        'city': 'praia-grande',
        'type': 'sobrado',
        'slug': 'sobrado-3-quartos-praia-grande',
        'price': 'R$ 580.000–850.000',
        'price_raw': '720000',
        'bedrooms': '3–4',
        'area': '120–170 m²',
        'image': 'https://praia.digital/img/pg-studio-moderno.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%203%20quartos%20Praia%20Grande&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Sobrado 3 quartos Bertioga',
        'description': 'Sobrado 3 quartos Bertioga: lazer, segurança e proximidade com a natureza.',
        'city': 'bertioga',
        'type': 'sobrado',
        'slug': 'sobrado-3-quartos-bertioga',
        'price': 'R$ 620.000–920.000',
        'price_raw': '770000',
        'bedrooms': '3–4',
        'area': '130–180 m²',
        'image': 'https://praia.digital/img/berta-alto-padrao.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Sobrado%203%20quartos%20Bertioga&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
    },
    {
        'title': 'Apartamento mobiliado Santos',
        'description': 'Apartamento mobiliado Santos: pronto para morar ou alugar por temporada.',
        'city': 'santos',
        'type': 'apartamento',
        'slug': 'apartamento-mobiliado-santos',
        'price': 'R$ 480.000–720.000',
        'price_raw': '600000',
        'bedrooms': '2–3',
        'area': '70–105 m²',
        'image': 'https://praia.digital/img/santos-apartamento-vista-mar.jpg',
        'tags': '',
        'related': '',
        'whatsapp_link': 'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20Apartamento%20mobiliado%20Santos&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
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
