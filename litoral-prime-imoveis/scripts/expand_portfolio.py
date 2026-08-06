import json
from pathlib import Path

base = Path('litoral-prime-imoveis')
imoveis_dir = base / 'imoveis'
imoveis_dir.mkdir(parents=True, exist_ok=True)

cities = {
    'Santos': ['Vila Nova', 'Gonzaga', 'Ponta da Praia', 'Embaré', 'Aparecida'],
    'Guaruja': ['Jardim Acapulco', 'Vila Julia', 'Enseada', 'Pernambuco', 'Guaruja'],
    'Praia Grande': ['Boqueirão', 'Vila Tupi', 'Caiçara', 'Ocian', 'Real'],
    'Bertioga': ['Riviera', 'São Lourenço', 'Centro', 'Mata Atlântica', 'Bertioga'],
    'Itanhaém': ['Centro', 'Cibratel', 'Jardim Grandesp', 'Gaivota', 'Itanhaém'],
    'Mongagua': ['Vila Virginia', 'Centro', 'Balneário', 'Mongaguá', 'Parque Turístico'],
    'Sao Vicente': ['Itararé', 'Vila Margarida', 'Centro', 'Gonzaguinha', 'São Vicente'],
    'Peruibe': ['Centro', 'Vila São Paulo', 'Peruíbe', 'Rio Preto', 'Costão']
}

types = ['Venda', 'Aluguel', 'Lançamento']
price_ranges = {
    'Santos': (450000, 2800000),
    'Guaruja': (320000, 1900000),
    'Praia Grande': (180000, 950000),
    'Bertioga': (380000, 3200000),
    'Itanhaém': (200000, 1100000),
    'Mongagua': (150000, 750000),
    'Sao Vicente': (220000, 1300000),
    'Peruibe': (170000, 890000)
}

bedrooms_pool = ['1', '2', '3', '4', '5']
areas_pool = ['35m²', '45m²', '60m²', '80m²', '100m²', '120m²', '150m²', '180m²', '220m²', '260m²']
tags_pool = ['Vista mar', 'Varanda gourmet', 'Condomínio fechado', 'Piscina', 'Churrasqueira', 'Quintal', 'Garagem', 'Mobiliado', 'Novo', 'Alto padrão', 'Investimento', 'Baixa manutenção', 'Aceita FGTS', 'Perto da praia', 'Lazer completo', 'Segurança 24h', 'Temporada', 'Renda extra', 'Apartamento', 'Casa', 'Cobertura', 'Studio', 'Sobrado', 'Terreno']

properties = []
idx = 1
for city, bairros in cities.items():
    min_val, max_val = price_ranges[city]
    for i, bairro in enumerate(bairros):
        tipo = types[i % 3]
        price_val = min_val + (max_val - min_val) // 5 * i + (max_val - min_val) // 10
        price = f"R$ {price_val:,}".replace(',', '.')
        bedrooms = bedrooms_pool[i % 5]
        area = areas_pool[i % 10]
        slug = f"{city.lower()}-{bairro.lower().replace(' ', '-')}-{tipo.lower().replace(' ', '-')}"
        slug = slug.replace('á', 'a').replace('ã', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        
        tags = [tags_pool[(i + j) % len(tags_pool)] for j in range(3)]
        seed = 1500000000000 + idx * 100000000
        image = f"https://images.unsplash.com/photo-{seed}?auto=format&fit=crop&w=900&q=60"
        
        properties.append({
            "id": idx,
            "title": f"{tipo} em {bairro} - {city}",
            "slug": slug,
            "city": city,
            "bairro": bairro,
            "type": tipo,
            "price": price,
            "bedrooms": bedrooms,
            "area": area,
            "score": 50 + (i * 7) % 50,
            "image": image,
            "tags": tags,
            "description": f"Imóvel {tipo.lower()} em {bairro}, {city}. {area}, {bedrooms} quartos. {tags[0]}, {tags[1]}. Oportunidade no litoral paulista."
        })
        idx += 1

final_properties = properties[:40]
(imoveis_dir / 'properties.json').write_text(json.dumps(final_properties, ensure_ascii=False, indent=2), encoding='utf-8')

main_js = (base / 'js' / 'main.js').read_text(encoding='utf-8')
start = main_js.index('  const properties = [')
end = main_js.index('  function escapeHtml(text) {')
new_js = main_js[:start] + '  const properties = ' + json.dumps(final_properties, ensure_ascii=False, indent=4) + ';\n\n' + main_js[end:]
(base / 'js' / 'main.js').write_text(new_js, encoding='utf-8')

print('Portfolio expandido para', len(final_properties), 'imoveis.')
