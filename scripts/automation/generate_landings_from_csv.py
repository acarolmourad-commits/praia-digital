from pathlib import Path
import csv, urllib.parse

REPO = Path('.').resolve()
OUT_DIR = REPO / 'imoveis'
OUT_DIR.mkdir(exist_ok=True)
TEMPLATE = (REPO / 'imoveis' / 'template-landing.html').read_text(encoding='utf-8')
CSV_PATH = REPO / 'imoveis' / 'landings.csv'

created = []
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
        if not related:
            related = f'<a class="servico-card" href="apartamento-{city.lower()}.html"><h3>Apartamento - {city}</h3><p>{city} • Venda</p><p>R$ 520.000</p></a><a class="servico-card" href="casa-{city.lower()}.html"><h3>Casa - {city}</h3><p>{city} • Venda</p><p>R$ 680.000</p></a><a class="servico-card" href="studio-{city.lower()}.html"><h3>Studio - {city}</h3><p>{city} • Venda</p><p>R$ 240.000</p></a>'
        whatsapp_link = row.get('whatsapp_link')
        if not whatsapp_link:
            safe = urllib.parse.quote(title)
            whatsapp_link = f'https://wa.me/5511954346288?text=Ol%C3%A1!%20Tenho%20interesse%20no%20{safe}&utm_source=site&utm_medium=whatsapp&utm_campaign=geral'

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
            skipped.append(out.name)
            continue
        out.write_text(html, encoding='utf-8')
        created.append(out.name)

print('LANDINGS_CREATED', len(created))
for p in created:
    print('-', p)
print('LANDINGS_SKIPPED', len(skipped))
