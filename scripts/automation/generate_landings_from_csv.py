from pathlib import Path
import csv
import argparse
import urllib.parse

REPO = Path('.').resolve()
OUT_DIR = REPO / 'imoveis'
OUT_DIR.mkdir(exist_ok=True)
TEMPLATE = (REPO / 'imoveis' / 'template-landing.html').read_text(encoding='utf-8')
CSV_PATH = REPO / 'imoveis' / 'landings.csv'

parser = argparse.ArgumentParser()
parser.add_argument('--overwrite', action='store_true')
args = parser.parse_args()
overwrite = args.overwrite

city_prices = {
    'santos': ('R$ 520.000', 'R$ 1.200.000'),
    'guaruja': ('R$ 450.000', 'R$ 950.000'),
    'praia-grande': ('R$ 300.000', 'R$ 800.000'),
    'bertioga': ('R$ 400.000', 'R$ 1.100.000'),
    'itanhaem': ('R$ 280.000', 'R$ 750.000'),
    'mongagua': ('R$ 250.000', 'R$ 600.000'),
    'sao-vicente': ('R$ 320.000', 'R$ 850.000'),
    'peruibe': ('R$ 220.000', 'R$ 650.000'),
    'caraguatatuba': ('R$ 350.000', 'R$ 900.000'),
    'ilhabela': ('R$ 500.000', 'R$ 1.500.000'),
    'ubatuba': ('R$ 300.000', 'R$ 1.000.000'),
}
type_tags = {
    'apartamento': ['Vista mar', 'Lazer completo', 'Garagem'],
    'casa': ['Quintal', 'Churrasqueira', 'Segurança 24h'],
    'cobertura': ['Piscina privativa', 'Vista mar', 'Alto padrão'],
    'sobrado': ['Amplo espaço', 'Quintal', 'Churrasqueira'],
    'studio': ['Compacto', 'Investimento', 'Temporada'],
    'terreno': ['Plano', 'Infraestrutura pronta', 'Rua asfaltada'],
}

created = []
updated = []
skipped = []

with open(CSV_PATH, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        slug = row.get('slug') or row.get('file', '').replace('.html', '')
        if not slug:
            continue
        title = row.get('title', slug.replace('-', ' ').title())
        desc = row.get('description', f'{title}: oportunidade no litoral de São Paulo.')
        city = row.get('city', '')
        type_ = row.get('type', 'Venda')
        price = row.get('price', 'R$ 450.000–1.200.000')
        bedrooms = row.get('bedrooms', '2–3')
        area = row.get('area', '70–180 m²')
        image = row.get('image', 'https://praia.digital/img/default-home.jpg')
        tags = row.get('tags', '<article class="servico-card"><h3>✓</h3><p>Lazer completo</p></article><article class="servico-card"><h3>✓</h3><p>Segurança 24h</p></article><article class="servico-card"><h3>✓</h3><p>Fácil acesso</p></article>')
        related = row.get('related', '')
        whatsapp_link = row.get('whatsapp_link')
        if not whatsapp_link:
            safe = urllib.parse.quote(title)
            whatsapp_link = f'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20{safe}&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'

        if price in ['R$ 450.000–1.200.000', 'R$ 450.000 – 1.200.000', 'R$ 300.000–R$ 900.000']:
            low, high = city_prices.get(city.lower(), ('R$ 300.000', 'R$ 900.000'))
            price = f'{low}–{high}'
        if 'Lazer completo' in tags or 'Segurança 24h' in tags:
            tags = ''.join([f'<article class="servico-card"><h3>✓</h3><p>{tag}</p></article>' for tag in type_tags.get(type_.lower(), ['Lazer completo', 'Segurança 24h', 'Fácil acesso'])])
        if not related:
            related = ''.join([
                f'<a class="servico-card" href="apartamento-{city.lower()}.html"><h3>Apartamento - {city}</h3><p>{city} • Venda</p><p>{price.split("–")[0].strip()}</p></a>',
                f'<a class="servico-card" href="casa-{city.lower()}.html"><h3>Casa - {city}</h3><p>{city} • Venda</p><p>{price.split("–")[0].strip()}</p></a>',
                f'<a class="servico-card" href="studio-{city.lower()}.html"><h3>Studio - {city}</h3><p>{city} • Venda</p><p>{price.split("–")[0].strip()}</p></a>',
            ])

        html = TEMPLATE
        html = html.replace('{{title}}', title)
        html = html.replace('{{description}}', desc)
        html = html.replace('{{city}}', city)
        html = html.replace('{{type}}', type_)
        html = html.replace('{{price}}', price)
        html = html.replace('{{bedrooms}}', bedrooms)
        html = html.replace('{{area}}', area)
        html = html.replace('{{image}}', image)
        html = html.replace('{{tags}}', tags)
        html = html.replace('{{related}}', related)
        html = html.replace('{{whatsapp_link}}', whatsapp_link)
        html = html.replace('https://praia.digital/imoveis/template-landing.html', f'https://praia.digital/imoveis/{slug}.html')

        out = OUT_DIR / f'{slug}.html'
        if out.exists():
            if overwrite:
                out.write_text(html, encoding='utf-8')
                updated.append(out.name)
            else:
                skipped.append(out.name)
            continue
        out.write_text(html, encoding='utf-8')
        created.append(out.name)

print('LANDINGS_CREATED', len(created))
for p in created:
    print('-', p)
print('LANDINGS_UPDATED', len(updated))
for p in updated:
    print('-', p)
print('LANDINGS_SKIPPED', len(skipped))
