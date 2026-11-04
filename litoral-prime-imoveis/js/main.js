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
  

      const properties = [];

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
    if (!list.length) {
      grid.innerHTML = '<p>Veja também os <a href="/imoveis.html">imóveis do catálogo atual</a>.</p>';
      return;
    }
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
