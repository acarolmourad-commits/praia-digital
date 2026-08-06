import json
from pathlib import Path
from datetime import date
import random

base = Path('C:/Users/Carolina/praia-digital/litoral-prime-imoveis')
imoveis_dir = base / 'imoveis'
imoveis_dir.mkdir(parents=True, exist_ok=True)

properties_path = base / 'imoveis' / 'properties.json'
properties = json.loads(properties_path.read_text(encoding='utf-8'))
existing_ids = {p['id'] for p in properties}
next_id = max(existing_ids) + 1 if existing_ids else 1

cities = {
    'Santos': ['Vila Nova', 'Gonzaga', 'Ponta da Praia', 'Embaré', 'Aparecida', 'Jose Menino', 'Campo Grande', 'Macuco', 'Valongo', 'Centro'],
    'Guarujá': ['Jardim Acapulco', 'Vila Julia', 'Enseada', 'Pernambuco', 'Guarujá', 'Santo Amaro', 'Cachoeira', 'Tortuga', 'Barra Seca', 'Marina'],
    'Praia Grande': ['Boqueirão', 'Vila Tupi', 'Caiçara', 'Ocian', 'Real', 'Guilhermina', 'Aviação', 'Ocian', 'Mirim', 'Solemar'],
    'Bertioga': ['Riviera', 'São Lourenço', 'Centro', 'Mata Atlântica', 'Bertioga', 'Costa do Sol', 'Boraceia', 'Guaratuba', 'Indaiá', 'Itatinga'],
    'Itanhaém': ['Centro', 'Cibratel', 'Jardim Grandesp', 'Gaivota', 'Itanhaém', 'Guaratuba', 'Savoy', 'Campos Elíseos', 'Baixio', 'Cajati'],
    'Mongaguá': ['Vila Virginia', 'Centro', 'Balneário', 'Mongaguá', 'Parque Turístico', 'Araca', 'São Pedro', 'Jardim Santos', 'Vila Lauro', 'Pontal'],
    'São Vicente': ['Centro', 'Gonzaguinha', 'Itararé', 'São Vicente', 'Vila Margarida', 'Parque Bitaru', 'Esplanada', 'Catuaí', 'Jockey', 'Jardim Rio Branco'],
    'Peruíbe': ['Centro', 'Vila São Paulo', 'Peruíbe', 'Rio Preto', 'Costão', 'Aricanduva', 'Jardim São Fernando', 'Nova Peruíbe', 'São Luís', 'Jardim do Trevo']
}

tags_pool = [
    'Vista mar', 'Varanda gourmet', 'Piscina', 'Churrasqueira', 'Academia', 'Elevador',
    'Segurança 24h', 'Condomínio fechado', 'Pet friendly', 'Ar-condicionado', 'Lareira',
    'Home office', 'Quintal', 'Horta', 'Vaga para embarcação', 'Acesso à praia', 'Mobiliado'
]

type_pool = ['Apartamento', 'Casa', 'Cobertura', 'Studio', 'Duplex', 'Garden', 'Loft']
status_pool = ['venda', 'aluguel', 'lançamento']
city_weights = {
    'Santos': 1.2,
    'Guarujá': 1.1,
    'Praia Grande': 1.0,
    'Bertioga': 0.9,
    'Itanhaém': 0.8,
    'Mongaguá': 0.7,
    'São Vicente': 0.9,
    'Peruíbe': 0.7
}

random.seed(42)
expanded = []
while len(expanded) < 20:
    city = random.choices(list(cities.keys()), weights=list(city_weights.values()), k=1)[0]
    bairro = random.choice(cities[city])
    bairro_slug = bairro.lower().replace(' ', '-').replace('ã', 'a').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ç', 'c')
    ptype = random.choice(type_pool)
    status = random.choice(status_pool)
    area = random.randint(28, 140)
    bedrooms = random.choices([1, 2, 3, 4], weights=[0.25, 0.35, 0.3, 0.1])[0]
    bathrooms = random.randint(1, 4)
    price_map = {'venda': (320000, 1850000), 'aluguel': (1800, 8500), 'lançamento': (450000, 2100000)}
    price = random.randint(*price_map[status])
    price_str = f"R$ {price:,.0f}".replace(',', '.')
    tags = random.sample(tags_pool, k=random.randint(3, 6))
    ptype_slug = ptype.lower().replace(' ', '-')
    slug = f"{ptype_slug}-{bairro_slug}-{city.lower().replace(' ', '-')}-{status}"
    title = f"{ptype} em {bairro} - {city}"
    description = f"{ptype} {status} em {bairro}, {city}. {area}m², {bedrooms} quartos, {bathrooms} banheiros. {', '.join(tags[:3])}. Oportunidade no litoral de SP."
    image = f"https://images.unsplash.com/photo-1500100000000?auto=format&fit=crop&w=900&q=60"
    id_ = next_id
    next_id += 1

    expanded.append({
        'id': id_,
        'slug': slug,
        'title': title,
        'type': ptype,
        'status': status,
        'city': city,
        'bairro': bairro,
        'price': price_str,
        'area': f"{area}m²",
        'bedrooms': str(bedrooms),
        'bathrooms': str(bathrooms),
        'tags': tags,
        'image': image,
        'description': description,
        'phone': '+5511954346288',
        'created_at': date.today().isoformat()
    })

combined = properties + expanded
properties_path.write_text(json.dumps(combined, ensure_ascii=False, indent=4), encoding='utf-8')
print('Propriedades expandidas para:', len(combined))
print('Novas adicionadas:', len(expanded))
