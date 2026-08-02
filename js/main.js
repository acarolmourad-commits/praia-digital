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
        "title": "Apartamento vista mar - Santos",
        "slug": "apartamento-vista-mar-santos",
        "city": "Santos",
        "type": "Venda",
        "price": "R$ 720.000",
        "bedrooms": "3",
        "area": "120m²",
        "score": 84,
        "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=900&q=60",
        "tags": ["Vista mar", "Varanda", "Condomínio fechado"],
        "description": "Apartamento com vista mar parcial, varanda gourmet e lazer completo no bairro mais valorizado de Santos."
      },
      {
        "id": 2,
        "title": "Casa duplex - Guarujá",
        "slug": "casa-duplex-guaruja",
        "city": "Guarujá",
        "type": "Aluguel",
        "price": "R$ 4.500/mês",
        "bedrooms": "4",
        "area": "220m²",
        "score": 64,
        "image": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=900&q=60",
        "tags": ["Piscina", "Churrasqueira", "Quintal"],
        "description": "Casa duplex com piscina, churrasqueira e quintal amplo. Ideal para temporada ou moradia."
      },
      {
        "id": 3,
        "title": "Studio moderno - Praia Grande",
        "slug": "studio-moderno-praia-grande",
        "city": "Praia Grande",
        "type": "Venda",
        "price": "R$ 280.000",
        "bedrooms": "1",
        "area": "45m²",
        "score": 72,
        "image": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=900&q=60",
        "tags": ["Investimento", "Baixa manutenção", "Mobiliado"],
        "description": "Studio moderno em lançamento com entrada facilitada. Ótimo para investimento ou início de vida."
      },
      {
        "id": 4,
        "title": "Cobertura duplex - São Vicente",
        "slug": "cobertura-duplex-sao-vicente",
        "city": "São Vicente",
        "type": "Venda",
        "price": "R$ 1.250.000",
        "bedrooms": "3",
        "area": "180m²",
        "score": 57,
        "image": "https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=900&q=60",
        "tags": ["Varanda gourmet", "Piscina privativa", "Garagem"],
        "description": "Cobertura duplex com vista deslumbrante, piscina privativa e acabamento alto padrão."
      },
      {
        "id": 5,
        "title": "Casa térrea - Itanhaém",
        "slug": "casa-terrea-itanhaem",
        "city": "Itanhaém",
        "type": "Aluguel",
        "price": "R$ 3.200/mês",
        "bedrooms": "3",
        "area": "150m²",
        "score": 66,
        "image": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=900&q=60",
        "tags": ["Quieto", "Quintal", "Perto da praia"],
        "description": "Casa térrea em rua calma, com quintal e acesso rápido à praia. Perfeita para famílias."
      },
      {
        "id": 6,
        "title": "Apartamento compacto - Mongaguá",
        "slug": "apartamento-compacto-mongagua",
        "city": "Mongaguá",
        "type": "Venda",
        "price": "R$ 210.000",
        "bedrooms": "2",
        "area": "58m²",
        "score": 79,
        "image": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=900&q=60",
        "tags": ["Acesso fácil", "Aceita FGTS", "Novo"],
        "description": "Apartamento compacto com financiamento facilitado, próximo à orla e com opção de FGTS."
      },
      {
        "id": 7,
        "title": "Sobrado geminado - Peruíbe",
        "slug": "sobrado-geminado-peruibe",
        "city": "Peruíbe",
        "type": "Venda",
        "price": "R$ 450.000",
        "bedrooms": "3",
        "area": "130m²",
        "score": 60,
        "image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=900&q=60",
        "tags": ["Lazer", "Segurança", "Quintal"],
        "description": "Sobrado geminado em condomínio fechado, com área de lazer e segurança 24h."
      },
      {
        "id": 8,
        "title": "Apartamento alto padrão - Bertioga",
        "slug": "apartamento-alto-padrao-bertioga",
        "city": "Bertioga",
        "type": "Aluguel",
        "price": "R$ 8.900/mês",
        "bedrooms": "4",
        "area": "240m²",
        "score": 49,
        "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=900&q=60",
        "tags": ["Alto padrão", "Vista mar", "Lazer completo"],
        "description": "Apartamento alto padrão com vista mar, lazer completo e acabamento premium em Bertioga."
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
