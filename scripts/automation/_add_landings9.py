import csv
from pathlib import Path

repo = Path('.').resolve()
csv_path = repo / 'imoveis' / 'landings.csv'

with open(csv_path, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    existing = list(reader)

updates = {r['slug']: r for r in existing if r.get('slug')}

cities = {
    'bertioga': 'https://praia.digital/img/berta-alto-padrao.jpg',
    'caraguatatuba': 'https://praia.digital/img/cara-cobertura.jpg',
    'guaruja': 'https://praia.digital/img/gua-casa-duplex.jpg',
    'ilhabela': 'https://praia.digital/img/ilha-sobrado.jpg',
    'itanhaem': 'https://praia.digital/img/it-casa-terrea.jpg',
    'mongagua': 'https://praia.digital/img/mon-ap-compacto.jpg',
    'peruibe': 'https://praia.digital/img/per-sobrado.jpg',
    'praia-grande': 'https://praia.digital/img/pg-studio-moderno.jpg',
    'santos': 'https://praia.digital/img/santos-apartamento-vista-mar.jpg',
    'sao-vicente': 'https://praia.digital/img/sv-cobertura-duplex.jpg',
    'ubatuba': 'https://praia.digital/img/ubatuba-sobrado.jpg',
}

def slug(t, city):
    return f'{t}-{city}'

def price(t):
    if t == 'flat':
        return 'R$ 190.000–330.000', '260000', '1', '24–42 m²'
    if t == 'chale':
        return 'R$ 260.000–450.000', '360000', '2', '50–80 m²'
    return '', '', '', ''

def title(t, city):
    if t == 'flat':
        return f'Flat centro {city.title()}'
    if t == 'chale':
        return f'Chalé centro {city.title()}'
    return ''

def desc(t, city):
    if t == 'flat':
        return f'Flat centro {city.title()}: compacto, prático e ideal para temporada ou investimento.'
    if t == 'chale':
        return f'Chalé centro {city.title()}: aconchego, lazer e tranquilidade no litoral.'
    return ''

new_rows = []
for city in cities:
    for t in ['flat', 'chale']:
        sl = slug(t, city)
        if sl not in updates:
            price_str, price_raw, beds, area = price(t)
            new_rows.append({
                'title': title(t, city),
                'description': desc(t, city),
                'city': city,
                'type': t,
                'slug': sl,
                'price': price_str,
                'price_raw': price_raw,
                'bedrooms': beds,
                'area': area,
                'image': cities[city],
                'tags': '',
                'related': '',
                'whatsapp_link': f'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20{title(t,city).replace(" ", "%20")}&utm_source=site&utm_medium=whatsapp&utm_campaign=geral',
            })

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
