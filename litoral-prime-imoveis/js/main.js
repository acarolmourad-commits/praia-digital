/* Litoral Prime Imóveis — dataset inicial + busca + CTA WhatsApp */
(function () {
  const WHATSAPP_NUMBER = '5511954346288';

  function waLink(message) {
    return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message || '')}`;
  }

  propertyCardTemplate = (p) => `
    <article class="property-card" itemscope itemtype="https://schema.org/Product">
      <meta itemprop="name" content="${escapeHtml(p.title)}">
      <div class="property-media">
        <img src="${p.image}" alt="${escapeHtml(p.title)}" loading="lazy" itemprop="image">
      </div>
      <div class="property-info">
        <h3 class="property-title" itemprop="name">${escapeHtml(p.title)} <span style="margin-left:8px;font-size:12px;color:#64748b">#${p.score||0}</span></h3>
        <p class="property-meta">${escapeHtml(p.city)} · ${escapeHtml(p.type)}</p>
        <p class="property-price" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
          <meta itemprop="priceCurrency" content="BRL">
          <span itemprop="price">${escapeHtml(p.price)}</span>
        </p>
        <p class="property-meta">${escapeHtml(p.bedrooms)} quartos · ${escapeHtml(p.area)}</p>
        <p class="property-meta">${escapeHtml((p.tags||[]).join(', '))}</p>
        <a class="btn-whatsapp" href="${waLink(`Olá! Tenho interesse no imóvel: ${escapeHtml(p.title)} — ${escapeHtml(p.city)}. Pode me enviar mais detalhes?`)}" target="_blank" rel="noopener">Conversar no WhatsApp</a>
        <a class="btn-secondary" href="imoveis/${p.slug}.html" target="_blank" rel="noopener">Ver detalhes</a>
      </div>
    </article>
  `;
  

      const properties = [
    {
        "id": 1,
        "title": "Venda em Vila Nova - Santos",
        "slug": "santos-vila-nova-venda",
        "city": "Santos",
        "bairro": "Vila Nova",
        "type": "Venda",
        "price": "R$ 685.000",
        "bedrooms": "1",
        "area": "35m²",
        "score": 50,
        "image": "https://images.unsplash.com/photo-1500100000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Vista mar",
            "Varanda gourmet",
            "Condomínio fechado"
        ],
        "description": "Imóvel venda em Vila Nova, Santos. 35m², 1 quartos. Vista mar, Varanda gourmet. Oportunidade no litoral paulista."
    },
    {
        "id": 2,
        "title": "Aluguel em Gonzaga - Santos",
        "slug": "santos-gonzaga-aluguel",
        "city": "Santos",
        "bairro": "Gonzaga",
        "type": "Aluguel",
        "price": "R$ 1.155.000",
        "bedrooms": "2",
        "area": "45m²",
        "score": 57,
        "image": "https://images.unsplash.com/photo-1500200000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Varanda gourmet",
            "Condomínio fechado",
            "Piscina"
        ],
        "description": "Imóvel aluguel em Gonzaga, Santos. 45m², 2 quartos. Varanda gourmet, Condomínio fechado. Oportunidade no litoral paulista."
    },
    {
        "id": 3,
        "title": "Lançamento em Ponta da Praia - Santos",
        "slug": "santos-ponta-da-praia-lançamento",
        "city": "Santos",
        "bairro": "Ponta da Praia",
        "type": "Lançamento",
        "price": "R$ 1.625.000",
        "bedrooms": "3",
        "area": "60m²",
        "score": 64,
        "image": "https://images.unsplash.com/photo-1500300000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Condomínio fechado",
            "Piscina",
            "Churrasqueira"
        ],
        "description": "Imóvel lançamento em Ponta da Praia, Santos. 60m², 3 quartos. Condomínio fechado, Piscina. Oportunidade no litoral paulista."
    },
    {
        "id": 4,
        "title": "Venda em Embaré - Santos",
        "slug": "santos-embare-venda",
        "city": "Santos",
        "bairro": "Embaré",
        "type": "Venda",
        "price": "R$ 2.095.000",
        "bedrooms": "4",
        "area": "80m²",
        "score": 71,
        "image": "https://images.unsplash.com/photo-1500400000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Piscina",
            "Churrasqueira",
            "Quintal"
        ],
        "description": "Imóvel venda em Embaré, Santos. 80m², 4 quartos. Piscina, Churrasqueira. Oportunidade no litoral paulista."
    },
    {
        "id": 5,
        "title": "Aluguel em Aparecida - Santos",
        "slug": "santos-aparecida-aluguel",
        "city": "Santos",
        "bairro": "Aparecida",
        "type": "Aluguel",
        "price": "R$ 2.565.000",
        "bedrooms": "5",
        "area": "100m²",
        "score": 78,
        "image": "https://images.unsplash.com/photo-1500500000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Churrasqueira",
            "Quintal",
            "Garagem"
        ],
        "description": "Imóvel aluguel em Aparecida, Santos. 100m², 5 quartos. Churrasqueira, Quintal. Oportunidade no litoral paulista."
    },
    {
        "id": 6,
        "title": "Venda em Jardim Acapulco - Guaruja",
        "slug": "guaruja-jardim-acapulco-venda",
        "city": "Guaruja",
        "bairro": "Jardim Acapulco",
        "type": "Venda",
        "price": "R$ 478.000",
        "bedrooms": "1",
        "area": "35m²",
        "score": 50,
        "image": "https://images.unsplash.com/photo-1500600000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Vista mar",
            "Varanda gourmet",
            "Condomínio fechado"
        ],
        "description": "Imóvel venda em Jardim Acapulco, Guaruja. 35m², 1 quartos. Vista mar, Varanda gourmet. Oportunidade no litoral paulista."
    },
    {
        "id": 7,
        "title": "Aluguel em Vila Julia - Guaruja",
        "slug": "guaruja-vila-julia-aluguel",
        "city": "Guaruja",
        "bairro": "Vila Julia",
        "type": "Aluguel",
        "price": "R$ 794.000",
        "bedrooms": "2",
        "area": "45m²",
        "score": 57,
        "image": "https://images.unsplash.com/photo-1500700000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Varanda gourmet",
            "Condomínio fechado",
            "Piscina"
        ],
        "description": "Imóvel aluguel em Vila Julia, Guaruja. 45m², 2 quartos. Varanda gourmet, Condomínio fechado. Oportunidade no litoral paulista."
    },
    {
        "id": 8,
        "title": "Lançamento em Enseada - Guaruja",
        "slug": "guaruja-enseada-lançamento",
        "city": "Guaruja",
        "bairro": "Enseada",
        "type": "Lançamento",
        "price": "R$ 1.110.000",
        "bedrooms": "3",
        "area": "60m²",
        "score": 64,
        "image": "https://images.unsplash.com/photo-1500800000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Condomínio fechado",
            "Piscina",
            "Churrasqueira"
        ],
        "description": "Imóvel lançamento em Enseada, Guaruja. 60m², 3 quartos. Condomínio fechado, Piscina. Oportunidade no litoral paulista."
    },
    {
        "id": 9,
        "title": "Venda em Pernambuco - Guaruja",
        "slug": "guaruja-pernambuco-venda",
        "city": "Guaruja",
        "bairro": "Pernambuco",
        "type": "Venda",
        "price": "R$ 1.426.000",
        "bedrooms": "4",
        "area": "80m²",
        "score": 71,
        "image": "https://images.unsplash.com/photo-1500900000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Piscina",
            "Churrasqueira",
            "Quintal"
        ],
        "description": "Imóvel venda em Pernambuco, Guaruja. 80m², 4 quartos. Piscina, Churrasqueira. Oportunidade no litoral paulista."
    },
    {
        "id": 10,
        "title": "Aluguel em Guaruja - Guaruja",
        "slug": "guaruja-guaruja-aluguel",
        "city": "Guaruja",
        "bairro": "Guaruja",
        "type": "Aluguel",
        "price": "R$ 1.742.000",
        "bedrooms": "5",
        "area": "100m²",
        "score": 78,
        "image": "https://images.unsplash.com/photo-1501000000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Churrasqueira",
            "Quintal",
            "Garagem"
        ],
        "description": "Imóvel aluguel em Guaruja, Guaruja. 100m², 5 quartos. Churrasqueira, Quintal. Oportunidade no litoral paulista."
    },
    {
        "id": 11,
        "title": "Venda em Boqueirão - Praia Grande",
        "slug": "praia grande-boqueirao-venda",
        "city": "Praia Grande",
        "bairro": "Boqueirão",
        "type": "Venda",
        "price": "R$ 257.000",
        "bedrooms": "1",
        "area": "35m²",
        "score": 50,
        "image": "https://images.unsplash.com/photo-1501100000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Vista mar",
            "Varanda gourmet",
            "Condomínio fechado"
        ],
        "description": "Imóvel venda em Boqueirão, Praia Grande. 35m², 1 quartos. Vista mar, Varanda gourmet. Oportunidade no litoral paulista."
    },
    {
        "id": 12,
        "title": "Aluguel em Vila Tupi - Praia Grande",
        "slug": "praia grande-vila-tupi-aluguel",
        "city": "Praia Grande",
        "bairro": "Vila Tupi",
        "type": "Aluguel",
        "price": "R$ 411.000",
        "bedrooms": "2",
        "area": "45m²",
        "score": 57,
        "image": "https://images.unsplash.com/photo-1501200000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Varanda gourmet",
            "Condomínio fechado",
            "Piscina"
        ],
        "description": "Imóvel aluguel em Vila Tupi, Praia Grande. 45m², 2 quartos. Varanda gourmet, Condomínio fechado. Oportunidade no litoral paulista."
    },
    {
        "id": 13,
        "title": "Lançamento em Caiçara - Praia Grande",
        "slug": "praia grande-caiçara-lançamento",
        "city": "Praia Grande",
        "bairro": "Caiçara",
        "type": "Lançamento",
        "price": "R$ 565.000",
        "bedrooms": "3",
        "area": "60m²",
        "score": 64,
        "image": "https://images.unsplash.com/photo-1501300000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Condomínio fechado",
            "Piscina",
            "Churrasqueira"
        ],
        "description": "Imóvel lançamento em Caiçara, Praia Grande. 60m², 3 quartos. Condomínio fechado, Piscina. Oportunidade no litoral paulista."
    },
    {
        "id": 14,
        "title": "Venda em Ocian - Praia Grande",
        "slug": "praia grande-ocian-venda",
        "city": "Praia Grande",
        "bairro": "Ocian",
        "type": "Venda",
        "price": "R$ 719.000",
        "bedrooms": "4",
        "area": "80m²",
        "score": 71,
        "image": "https://images.unsplash.com/photo-1501400000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Piscina",
            "Churrasqueira",
            "Quintal"
        ],
        "description": "Imóvel venda em Ocian, Praia Grande. 80m², 4 quartos. Piscina, Churrasqueira. Oportunidade no litoral paulista."
    },
    {
        "id": 15,
        "title": "Aluguel em Real - Praia Grande",
        "slug": "praia grande-real-aluguel",
        "city": "Praia Grande",
        "bairro": "Real",
        "type": "Aluguel",
        "price": "R$ 873.000",
        "bedrooms": "5",
        "area": "100m²",
        "score": 78,
        "image": "https://images.unsplash.com/photo-1501500000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Churrasqueira",
            "Quintal",
            "Garagem"
        ],
        "description": "Imóvel aluguel em Real, Praia Grande. 100m², 5 quartos. Churrasqueira, Quintal. Oportunidade no litoral paulista."
    },
    {
        "id": 16,
        "title": "Venda em Riviera - Bertioga",
        "slug": "bertioga-riviera-venda",
        "city": "Bertioga",
        "bairro": "Riviera",
        "type": "Venda",
        "price": "R$ 662.000",
        "bedrooms": "1",
        "area": "35m²",
        "score": 50,
        "image": "https://images.unsplash.com/photo-1501600000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Vista mar",
            "Varanda gourmet",
            "Condomínio fechado"
        ],
        "description": "Imóvel venda em Riviera, Bertioga. 35m², 1 quartos. Vista mar, Varanda gourmet. Oportunidade no litoral paulista."
    },
    {
        "id": 17,
        "title": "Aluguel em São Lourenço - Bertioga",
        "slug": "bertioga-sao-lourenço-aluguel",
        "city": "Bertioga",
        "bairro": "São Lourenço",
        "type": "Aluguel",
        "price": "R$ 1.226.000",
        "bedrooms": "2",
        "area": "45m²",
        "score": 57,
        "image": "https://images.unsplash.com/photo-1501700000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Varanda gourmet",
            "Condomínio fechado",
            "Piscina"
        ],
        "description": "Imóvel aluguel em São Lourenço, Bertioga. 45m², 2 quartos. Varanda gourmet, Condomínio fechado. Oportunidade no litoral paulista."
    },
    {
        "id": 18,
        "title": "Lançamento em Centro - Bertioga",
        "slug": "bertioga-centro-lançamento",
        "city": "Bertioga",
        "bairro": "Centro",
        "type": "Lançamento",
        "price": "R$ 1.790.000",
        "bedrooms": "3",
        "area": "60m²",
        "score": 64,
        "image": "https://images.unsplash.com/photo-1501800000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Condomínio fechado",
            "Piscina",
            "Churrasqueira"
        ],
        "description": "Imóvel lançamento em Centro, Bertioga. 60m², 3 quartos. Condomínio fechado, Piscina. Oportunidade no litoral paulista."
    },
    {
        "id": 19,
        "title": "Venda em Mata Atlântica - Bertioga",
        "slug": "bertioga-mata-atlântica-venda",
        "city": "Bertioga",
        "bairro": "Mata Atlântica",
        "type": "Venda",
        "price": "R$ 2.354.000",
        "bedrooms": "4",
        "area": "80m²",
        "score": 71,
        "image": "https://images.unsplash.com/photo-1501900000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Piscina",
            "Churrasqueira",
            "Quintal"
        ],
        "description": "Imóvel venda em Mata Atlântica, Bertioga. 80m², 4 quartos. Piscina, Churrasqueira. Oportunidade no litoral paulista."
    },
    {
        "id": 20,
        "title": "Aluguel em Bertioga - Bertioga",
        "slug": "bertioga-bertioga-aluguel",
        "city": "Bertioga",
        "bairro": "Bertioga",
        "type": "Aluguel",
        "price": "R$ 2.918.000",
        "bedrooms": "5",
        "area": "100m²",
        "score": 78,
        "image": "https://images.unsplash.com/photo-1502000000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Churrasqueira",
            "Quintal",
            "Garagem"
        ],
        "description": "Imóvel aluguel em Bertioga, Bertioga. 100m², 5 quartos. Churrasqueira, Quintal. Oportunidade no litoral paulista."
    },
    {
        "id": 21,
        "title": "Venda em Centro - Itanhaém",
        "slug": "itanhaem-centro-venda",
        "city": "Itanhaém",
        "bairro": "Centro",
        "type": "Venda",
        "price": "R$ 290.000",
        "bedrooms": "1",
        "area": "35m²",
        "score": 50,
        "image": "https://images.unsplash.com/photo-1502100000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Vista mar",
            "Varanda gourmet",
            "Condomínio fechado"
        ],
        "description": "Imóvel venda em Centro, Itanhaém. 35m², 1 quartos. Vista mar, Varanda gourmet. Oportunidade no litoral paulista."
    },
    {
        "id": 22,
        "title": "Aluguel em Cibratel - Itanhaém",
        "slug": "itanhaem-cibratel-aluguel",
        "city": "Itanhaém",
        "bairro": "Cibratel",
        "type": "Aluguel",
        "price": "R$ 470.000",
        "bedrooms": "2",
        "area": "45m²",
        "score": 57,
        "image": "https://images.unsplash.com/photo-1502200000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Varanda gourmet",
            "Condomínio fechado",
            "Piscina"
        ],
        "description": "Imóvel aluguel em Cibratel, Itanhaém. 45m², 2 quartos. Varanda gourmet, Condomínio fechado. Oportunidade no litoral paulista."
    },
    {
        "id": 23,
        "title": "Lançamento em Jardim Grandesp - Itanhaém",
        "slug": "itanhaem-jardim-grandesp-lançamento",
        "city": "Itanhaém",
        "bairro": "Jardim Grandesp",
        "type": "Lançamento",
        "price": "R$ 650.000",
        "bedrooms": "3",
        "area": "60m²",
        "score": 64,
        "image": "https://images.unsplash.com/photo-1502300000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Condomínio fechado",
            "Piscina",
            "Churrasqueira"
        ],
        "description": "Imóvel lançamento em Jardim Grandesp, Itanhaém. 60m², 3 quartos. Condomínio fechado, Piscina. Oportunidade no litoral paulista."
    },
    {
        "id": 24,
        "title": "Venda em Gaivota - Itanhaém",
        "slug": "itanhaem-gaivota-venda",
        "city": "Itanhaém",
        "bairro": "Gaivota",
        "type": "Venda",
        "price": "R$ 830.000",
        "bedrooms": "4",
        "area": "80m²",
        "score": 71,
        "image": "https://images.unsplash.com/photo-1502400000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Piscina",
            "Churrasqueira",
            "Quintal"
        ],
        "description": "Imóvel venda em Gaivota, Itanhaém. 80m², 4 quartos. Piscina, Churrasqueira. Oportunidade no litoral paulista."
    },
    {
        "id": 25,
        "title": "Aluguel em Itanhaém - Itanhaém",
        "slug": "itanhaem-itanhaem-aluguel",
        "city": "Itanhaém",
        "bairro": "Itanhaém",
        "type": "Aluguel",
        "price": "R$ 1.010.000",
        "bedrooms": "5",
        "area": "100m²",
        "score": 78,
        "image": "https://images.unsplash.com/photo-1502500000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Churrasqueira",
            "Quintal",
            "Garagem"
        ],
        "description": "Imóvel aluguel em Itanhaém, Itanhaém. 100m², 5 quartos. Churrasqueira, Quintal. Oportunidade no litoral paulista."
    },
    {
        "id": 26,
        "title": "Venda em Vila Virginia - Mongagua",
        "slug": "mongagua-vila-virginia-venda",
        "city": "Mongagua",
        "bairro": "Vila Virginia",
        "type": "Venda",
        "price": "R$ 210.000",
        "bedrooms": "1",
        "area": "35m²",
        "score": 50,
        "image": "https://images.unsplash.com/photo-1502600000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Vista mar",
            "Varanda gourmet",
            "Condomínio fechado"
        ],
        "description": "Imóvel venda em Vila Virginia, Mongagua. 35m², 1 quartos. Vista mar, Varanda gourmet. Oportunidade no litoral paulista."
    },
    {
        "id": 27,
        "title": "Aluguel em Centro - Mongagua",
        "slug": "mongagua-centro-aluguel",
        "city": "Mongagua",
        "bairro": "Centro",
        "type": "Aluguel",
        "price": "R$ 330.000",
        "bedrooms": "2",
        "area": "45m²",
        "score": 57,
        "image": "https://images.unsplash.com/photo-1502700000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Varanda gourmet",
            "Condomínio fechado",
            "Piscina"
        ],
        "description": "Imóvel aluguel em Centro, Mongagua. 45m², 2 quartos. Varanda gourmet, Condomínio fechado. Oportunidade no litoral paulista."
    },
    {
        "id": 28,
        "title": "Lançamento em Balneário - Mongagua",
        "slug": "mongagua-balneario-lançamento",
        "city": "Mongagua",
        "bairro": "Balneário",
        "type": "Lançamento",
        "price": "R$ 450.000",
        "bedrooms": "3",
        "area": "60m²",
        "score": 64,
        "image": "https://images.unsplash.com/photo-1502800000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Condomínio fechado",
            "Piscina",
            "Churrasqueira"
        ],
        "description": "Imóvel lançamento em Balneário, Mongagua. 60m², 3 quartos. Condomínio fechado, Piscina. Oportunidade no litoral paulista."
    },
    {
        "id": 29,
        "title": "Venda em Mongaguá - Mongagua",
        "slug": "mongagua-mongagua-venda",
        "city": "Mongagua",
        "bairro": "Mongaguá",
        "type": "Venda",
        "price": "R$ 570.000",
        "bedrooms": "4",
        "area": "80m²",
        "score": 71,
        "image": "https://images.unsplash.com/photo-1502900000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Piscina",
            "Churrasqueira",
            "Quintal"
        ],
        "description": "Imóvel venda em Mongaguá, Mongagua. 80m², 4 quartos. Piscina, Churrasqueira. Oportunidade no litoral paulista."
    },
    {
        "id": 30,
        "title": "Aluguel em Parque Turístico - Mongagua",
        "slug": "mongagua-parque-turistico-aluguel",
        "city": "Mongagua",
        "bairro": "Parque Turístico",
        "type": "Aluguel",
        "price": "R$ 690.000",
        "bedrooms": "5",
        "area": "100m²",
        "score": 78,
        "image": "https://images.unsplash.com/photo-1503000000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Churrasqueira",
            "Quintal",
            "Garagem"
        ],
        "description": "Imóvel aluguel em Parque Turístico, Mongagua. 100m², 5 quartos. Churrasqueira, Quintal. Oportunidade no litoral paulista."
    },
    {
        "id": 31,
        "title": "Venda em Itararé - Sao Vicente",
        "slug": "sao vicente-itarare-venda",
        "city": "Sao Vicente",
        "bairro": "Itararé",
        "type": "Venda",
        "price": "R$ 328.000",
        "bedrooms": "1",
        "area": "35m²",
        "score": 50,
        "image": "https://images.unsplash.com/photo-1503100000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Vista mar",
            "Varanda gourmet",
            "Condomínio fechado"
        ],
        "description": "Imóvel venda em Itararé, Sao Vicente. 35m², 1 quartos. Vista mar, Varanda gourmet. Oportunidade no litoral paulista."
    },
    {
        "id": 32,
        "title": "Aluguel em Vila Margarida - Sao Vicente",
        "slug": "sao vicente-vila-margarida-aluguel",
        "city": "Sao Vicente",
        "bairro": "Vila Margarida",
        "type": "Aluguel",
        "price": "R$ 544.000",
        "bedrooms": "2",
        "area": "45m²",
        "score": 57,
        "image": "https://images.unsplash.com/photo-1503200000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Varanda gourmet",
            "Condomínio fechado",
            "Piscina"
        ],
        "description": "Imóvel aluguel em Vila Margarida, Sao Vicente. 45m², 2 quartos. Varanda gourmet, Condomínio fechado. Oportunidade no litoral paulista."
    },
    {
        "id": 33,
        "title": "Lançamento em Centro - Sao Vicente",
        "slug": "sao vicente-centro-lançamento",
        "city": "Sao Vicente",
        "bairro": "Centro",
        "type": "Lançamento",
        "price": "R$ 760.000",
        "bedrooms": "3",
        "area": "60m²",
        "score": 64,
        "image": "https://images.unsplash.com/photo-1503300000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Condomínio fechado",
            "Piscina",
            "Churrasqueira"
        ],
        "description": "Imóvel lançamento em Centro, Sao Vicente. 60m², 3 quartos. Condomínio fechado, Piscina. Oportunidade no litoral paulista."
    },
    {
        "id": 34,
        "title": "Venda em Gonzaguinha - Sao Vicente",
        "slug": "sao vicente-gonzaguinha-venda",
        "city": "Sao Vicente",
        "bairro": "Gonzaguinha",
        "type": "Venda",
        "price": "R$ 976.000",
        "bedrooms": "4",
        "area": "80m²",
        "score": 71,
        "image": "https://images.unsplash.com/photo-1503400000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Piscina",
            "Churrasqueira",
            "Quintal"
        ],
        "description": "Imóvel venda em Gonzaguinha, Sao Vicente. 80m², 4 quartos. Piscina, Churrasqueira. Oportunidade no litoral paulista."
    },
    {
        "id": 35,
        "title": "Aluguel em São Vicente - Sao Vicente",
        "slug": "sao vicente-sao-vicente-aluguel",
        "city": "Sao Vicente",
        "bairro": "São Vicente",
        "type": "Aluguel",
        "price": "R$ 1.192.000",
        "bedrooms": "5",
        "area": "100m²",
        "score": 78,
        "image": "https://images.unsplash.com/photo-1503500000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Churrasqueira",
            "Quintal",
            "Garagem"
        ],
        "description": "Imóvel aluguel em São Vicente, Sao Vicente. 100m², 5 quartos. Churrasqueira, Quintal. Oportunidade no litoral paulista."
    },
    {
        "id": 36,
        "title": "Venda em Centro - Peruibe",
        "slug": "peruibe-centro-venda",
        "city": "Peruibe",
        "bairro": "Centro",
        "type": "Venda",
        "price": "R$ 242.000",
        "bedrooms": "1",
        "area": "35m²",
        "score": 50,
        "image": "https://images.unsplash.com/photo-1503600000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Vista mar",
            "Varanda gourmet",
            "Condomínio fechado"
        ],
        "description": "Imóvel venda em Centro, Peruibe. 35m², 1 quartos. Vista mar, Varanda gourmet. Oportunidade no litoral paulista."
    },
    {
        "id": 37,
        "title": "Aluguel em Vila São Paulo - Peruibe",
        "slug": "peruibe-vila-sao-paulo-aluguel",
        "city": "Peruibe",
        "bairro": "Vila São Paulo",
        "type": "Aluguel",
        "price": "R$ 386.000",
        "bedrooms": "2",
        "area": "45m²",
        "score": 57,
        "image": "https://images.unsplash.com/photo-1503700000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Varanda gourmet",
            "Condomínio fechado",
            "Piscina"
        ],
        "description": "Imóvel aluguel em Vila São Paulo, Peruibe. 45m², 2 quartos. Varanda gourmet, Condomínio fechado. Oportunidade no litoral paulista."
    },
    {
        "id": 38,
        "title": "Lançamento em Peruíbe - Peruibe",
        "slug": "peruibe-peruibe-lançamento",
        "city": "Peruibe",
        "bairro": "Peruíbe",
        "type": "Lançamento",
        "price": "R$ 530.000",
        "bedrooms": "3",
        "area": "60m²",
        "score": 64,
        "image": "https://images.unsplash.com/photo-1503800000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Condomínio fechado",
            "Piscina",
            "Churrasqueira"
        ],
        "description": "Imóvel lançamento em Peruíbe, Peruibe. 60m², 3 quartos. Condomínio fechado, Piscina. Oportunidade no litoral paulista."
    },
    {
        "id": 39,
        "title": "Venda em Rio Preto - Peruibe",
        "slug": "peruibe-rio-preto-venda",
        "city": "Peruibe",
        "bairro": "Rio Preto",
        "type": "Venda",
        "price": "R$ 674.000",
        "bedrooms": "4",
        "area": "80m²",
        "score": 71,
        "image": "https://images.unsplash.com/photo-1503900000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Piscina",
            "Churrasqueira",
            "Quintal"
        ],
        "description": "Imóvel venda em Rio Preto, Peruibe. 80m², 4 quartos. Piscina, Churrasqueira. Oportunidade no litoral paulista."
    },
    {
        "id": 40,
        "title": "Aluguel em Costão - Peruibe",
        "slug": "peruibe-costao-aluguel",
        "city": "Peruibe",
        "bairro": "Costão",
        "type": "Aluguel",
        "price": "R$ 818.000",
        "bedrooms": "5",
        "area": "100m²",
        "score": 78,
        "image": "https://images.unsplash.com/photo-1504000000000?auto=format&fit=crop&w=900&q=60",
        "tags": [
            "Churrasqueira",
            "Quintal",
            "Garagem"
        ],
        "description": "Imóvel aluguel em Costão, Peruibe. 100m², 5 quartos. Churrasqueira, Quintal. Oportunidade no litoral paulista."
    }
];

  function escapeHtml(text) {
    if (text === null || text === undefined) return '';
    return String(text)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function render(list) {
    const grid = document.getElementById('lista-imoveis');
    if (!grid) return;
    grid.innerHTML = list.map((item) => propertyCardTemplate(item)).join('');
  }

  function filterProperties() {
    const query = (document.getElementById('busca')?.value || '').trim().toLowerCase();
    const typeFilter = document.getElementById('tipo-filtro')?.value || '';
    const cityFilter = document.getElementById('cidade-filtro')?.value || '';

    const filtered = properties.filter((p) => {
      const matchesQuery =
        !query ||
        [p.title, p.city, p.type, p.tags.join(' ')].some((v) => String(v).toLowerCase().includes(query));

      const matchesType = !typeFilter || p.type === typeFilter || p.type.toLowerCase() === typeFilter.toLowerCase();
      const matchesCity = !cityFilter || p.city === cityFilter || p.city.toLowerCase() === cityFilter.toLowerCase();

      return matchesQuery && matchesType && matchesCity;
    });

    render(filtered);
  }

  function initFilters() {
    const cities = Array.from(new Set(properties.map((p) => p.city))).sort();

    const citySelect = document.getElementById('cidade-filtro');
    if (citySelect) {
      citySelect.innerHTML = '<option value="">Todas as cidades</option>' + cities.map((c) => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('');
    }

    const typeSelect = document.getElementById('tipo-filtro');
    if (typeSelect) {
      typeSelect.innerHTML = '<option value="">Todos os tipos</option>' +
        ['Venda', 'Aluguel', 'Lançamento']
        .map((t) => `<option value="${escapeHtml(t)}">${escapeHtml(t)}</option>`)
        .join('');
    }
  }

  function buscarImoveis() {
    const q = (document.getElementById('busca')?.value || '').trim().toLowerCase();
    const typeFilter = document.getElementById('tipo-filtro')?.value || '';
    const cityFilter = document.getElementById('cidade-filtro')?.value || '';

    let filtered = properties.filter((p) => {
      const text = [p.title, p.city, p.type, p.description, (p.tags||[]).join(' ')].join(' ');
      const matchesQuery = !q || String(text).toLowerCase().includes(q);
      const matchesType = !typeFilter || p.type === typeFilter || p.type.toLowerCase() === typeFilter.toLowerCase();
      const matchesCity = !cityFilter || p.city === cityFilter || p.city.toLowerCase() === cityFilter.toLowerCase();
      return matchesQuery && matchesType && matchesCity;
    });

    filtered = filtered.slice().sort((a,b)=> (parseInt(b.score||0,10)-parseInt(a.score||0,10)));
    render(filtered);
  }

  function onFormSubmit(e) {
    e.preventDefault();
    const nome = (document.getElementById('nome')?.value || '').trim();
    const email = (document.getElementById('email')?.value || '').trim();
    const telefone = (document.getElementById('telefone')?.value || '').trim();
    const interesse = (document.getElementById('interesse')?.value || '').trim();
    const mensagem = (document.getElementById('mensagem')?.value || '').trim();

    if (!nome || !email || !interesse) {
      alert('Preencha os campos obrigatórios: nome, e-mail e interesse.');
      return;
    }

    const body = encodeURIComponent(`Nome: ${nome}\nE-mail: ${email}\nTelefone: ${telefone}\nInteresse: ${interesse}\nMensagem: ${mensagem}`);
    const url = `mailto:comercial@praia.digital?subject=Contato%20Litoral%20Prime%20Imóveis&body=${body}`;

    const img = new Image();
    img.src = `/scripts/captura_lead.py?nome=${encodeURIComponent(nome)}&email=${encodeURIComponent(email)}&telefone=${encodeURIComponent(telefone)}&interesse=${encodeURIComponent(interesse)}&mensagem=${encodeURIComponent(mensagem)}`;
    window.location.href = url;
  }

  document.addEventListener('DOMContentLoaded', () => {
    initFilters();
    render(properties);

    const buscaInput = document.getElementById('busca');
    if (buscaInput) {
      buscaInput.addEventListener('input', buscarImoveis);
      buscaInput.addEventListener('search', buscarImoveis);
    }
    const tipo = document.getElementById('tipo-filtro');
    if (tipo) tipo.addEventListener('change', buscarImoveis);
    const cidade = document.getElementById('cidade-filtro');
    if (cidade) cidade.addEventListener('change', buscarImoveis);

    const contatoForm = document.getElementById('contato-form');
    if (contatoForm) contatoForm.addEventListener('submit', onFormSubmit);
  });
})();
