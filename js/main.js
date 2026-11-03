/* Litoral Prime Imóveis — dataset inicial + busca + CTA WhatsApp */
(function () {
  const WHATSAPP_NUMBER = '5511954346288';

  function waLink(message) {
    return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message || '')}`;
  }

  const detailUrl = (p) => p.slug.startsWith('../')
    ? `${p.slug.slice(3)}.html`
    : `imoveis/${p.slug}.html`;

  const propertyCardTemplate = (p) => `
    <article class="property-card" itemscope itemtype="https://schema.org/Product">
      <meta itemprop="name" content="${escapeHtml(p.title)}">
      ${p.image ? `<div class="property-media"><img src="${p.image}" alt="${escapeHtml(p.title)}" loading="lazy" itemprop="image"></div>` : ''}
      <div class="property-info">
        <h3 class="property-title" itemprop="name">${escapeHtml(p.title)} ${p.score ? `<span style="margin-left:8px;font-size:12px;color:#64748b">#${p.score}</span>` : ''}</h3>
        <p class="property-meta">${escapeHtml(p.city)} · ${escapeHtml(p.type)}</p>
        <p class="property-price" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
          <meta itemprop="priceCurrency" content="BRL">
          <meta itemprop="price" content="${priceNumber(p.price)}">
          <link itemprop="availability" href="https://schema.org/InStock">
          <span>${escapeHtml(p.price)}</span>
        </p>
        <p class="property-meta">${escapeHtml(p.bedrooms)} quartos · ${escapeHtml(p.area)}</p>
        <p class="property-meta">${escapeHtml((p.tags||[]).join(', '))}</p>
        <a class="btn-whatsapp" href="${waLink(`Olá! Tenho interesse no imóvel: ${escapeHtml(p.title)} — ${escapeHtml(p.city)}. Pode me enviar mais detalhes?`)}" target="_blank" rel="noopener">Conversar no WhatsApp</a>
        <a class="btn-secondary" href="${detailUrl(p)}">Ver detalhes</a>
      </div>
    </article>
  `;
  
  const properties = [
      {
        "id": 12,
        "title": "Casa térrea a uma quadra da praia em Bertioga",
        "slug": "casa-terrea-bertioga-675m2",
        "city": "Bertioga",
        "type": "Venda",
        "price": "R$ 1.800.000",
        "bedrooms": "3",
        "area": "234 m² construídos",
        "image": "https://praia.digital/assets/casa-terrea-bertioga-675m2/01_IMG_0098.jpeg",
        "tags": [
                "Terreno 675 m²",
                "2 suítes",
                "10 vagas",
                "Quintal",
                "Uma quadra da praia"
        ],
        "description": "Casa térrea em Bertioga a uma quadra da praia: terreno de 675 m², 234 m² construídos, 3 dormitórios, 2 suítes e 10 vagas. Venda por R$ 1.800.000. Fotos reais e cenários ilustrativos."
},
      {
        "id": 11,
        "title": "Apartamento reformado a uma quadra da praia em Bertioga",
        "slug": "apartamento-bertioga-70m2",
        "city": "Bertioga",
        "type": "Venda",
        "price": "R$ 600.000",
        "bedrooms": "2",
        "area": "70,53 m²",
        "image": "https://praia.digital/assets/apartamento-bertioga-70m2/03_IMG_0047_ajustada.jpg",
        "tags": [
                "1 suíte",
                "Elevador",
                "Piscina",
                "1 vaga",
                "Aceita financiamento",
                "Uma quadra da praia",
                "Armários fixos e ar-condicionado"
        ],
        "description": "Apartamento reformado a uma quadra da praia em Bertioga por R$ 600 mil: 70,53 m², 2 quartos sendo 1 suíte, elevador, piscina e 1 vaga. Aceita financiamento. Fotos reais e simuladores ilustrativos."
},
      {
        "id": 10,
        "title": "Lançamento: casas de alto padrão em São Lourenço",
        "slug": "casas-lancamento-sao-lourenco",
        "city": "Bertioga",
        "type": "Lançamento",
        "price": "R$ 2.500.000",
        "bedrooms": "4",
        "area": "aprox. 200m²",
        "score": 100,
        "image": "https://praia.digital/assets/casas-sao-lourenco/fachada.jpg",
        "tags": ["São Lourenço", "Terreno 180m²", "Piscina", "Sauna", "Espaço gourmet integrado", "Vista para Itaguaré"],
        "description": "Lançamento de casas em São Lourenço, Bertioga. Terreno de 180m² (6 x 30m), aproximadamente 200m² construídos, 4 suítes, piscina, sauna, espaço gourmet integrado e suíte master com vista para a praia de Itaguaré. Parcelamento direto em até 18 meses ou financiamento direto em até 100 meses, sujeito a condições."
      },

      {
        "id": 9,
        "title": "Casa em condomínio fechado - Bertioga",
        "slug": "../casa-condominio-fechado-bertioga",
        "city": "Bertioga",
        "type": "Venda",
        "price": "R$ 595.000",
        "bedrooms": "2",
        "area": "105m²",
        "score": 95,
        "image": "https://praia.digital/img/bertioga-casa-fachada-externa.webp",
        "tags": ["100m da praia", "Piscina", "Sauna", "Academia"],
        "description": "Casa em condomínio fechado a 100m da praia, com piscina, sauna e academia. Imóvel real cadastrado na Praia Digital."
      },
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
      }
    ];

  function priceNumber(text) {
    // Extrai valor numérico puro ("R$ 1.250.000" -> 1250000, "R$ 4.500/mês" -> 4500)
    if (text === null || text === undefined) return '';
    const value = window.PDPropertySearch.money(String(text).replace(/\/(?:mes|mês|dia).*$/i, ''));
    return value === null ? '' : value;
  }

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
      grid.innerHTML = '<p class="imoveis-empty">Nenhum imóvel encontrado com esses filtros. Tente outra cidade ou característica.</p>';
      return;
    }
    grid.innerHTML = list.map((item) => propertyCardTemplate(item)).join('');
  }

  const search = window.PDPropertySearch;
  let state;
  const fields = {cidade:'cidade-filtro', finalidade:'tipo-filtro', tipo:'categoria-filtro', quartos:'quartos-filtro', preco_max:'preco-filtro'};
  const {budgetUnit,withoutBudget}=search || {};
  function initFilters() {
    const citySelect=document.getElementById('cidade-filtro');
    if(citySelect) citySelect.innerHTML='<option value="">Todas as cidades</option>'+search.cities.map(c=>`<option value="${c}">${c}</option>`).join('');
    const purpose=document.getElementById('tipo-filtro');
    if(purpose) purpose.innerHTML='<option value="">Escolha: comprar ou alugar</option><option value="Venda">Comprar (inclui lançamentos)</option><option value="Aluguel">Alugar por mês</option><option value="Lançamento">Somente lançamentos</option>';
  }
  function updateControls() {
    document.getElementById('busca').value=state.q;
    for(const [key,id] of Object.entries(fields)) {
      const el=document.getElementById(id);
      if(el.tagName==='SELECT' && state[key] && !Array.from(el.options).some(o=>search.normalize(o.value)===search.normalize(state[key]))) el.add(new Option(state[key],state[key]));
      const option=el.tagName==='SELECT' && Array.from(el.options).find(o=>search.normalize(o.value)===search.normalize(state[key]));
      el.value=option?option.value:state[key];
    }
    document.getElementById('preco-label').textContent=state.finalidade==='Aluguel' ? 'Aluguel máximo (R$/mês)' : state.finalidade ? 'Preço de compra máximo (R$)' : 'Orçamento máximo (escolha a finalidade)';
  }
  function showResults() {
    if(state.preco_max && !state.finalidade) {
      document.getElementById('lista-imoveis').innerHTML='<p class="imoveis-empty">Escolha comprar ou alugar para aplicar o orçamento informado.</p>';
      document.getElementById('search-status').textContent='Finalidade pendente: preço de compra e aluguel mensal não são comparáveis.';
      return;
    }
    const filtered=properties.filter(p=>search.matches(p,state)).sort((a,b)=>Number(b.score||0)-Number(a.score||0));
    render(filtered);
    document.getElementById('search-status').textContent=filtered.length+' imóvel(is) encontrado(s).'+(state.perfil==='investimento'?' Investimento é seu objetivo; rentabilidade não é garantida.':'')+(state.perfil==='temporada'?' Temporada: somente anúncios que mencionam esse perfil.':'');
    if(state.budgetCleared) document.getElementById('search-status').textContent+=' Orçamento limpo: o texto e a finalidade do link eram diferentes. Informe o valor para a finalidade escolhida.';
  }
  function saveSearch(push) {
    const url=new URL(location.href);
    for(const key of ['q',...Object.keys(fields),'perfil']) url.searchParams.set(key,state[key] || '');
    history[push?'pushState':'replaceState'](null,'',url);
    showResults();
  }
  function restoreSearch() {
    state=search.fromParams(new URLSearchParams(location.search));
    updateControls(); showResults();
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
    if(document.getElementById('lista-imoveis') && search) {
      initFilters(); restoreSearch();
      const input=document.getElementById('busca');
      function queryChanged() {
        const parsed=search.parse(input.value);
        const explicit=/\b(comprar|compra|venda|alugar|aluguel|locacao)\b/.test(search.normalize(input.value));
        // Explicit text edits win over the current selector; otherwise keep its choice.
        const purpose=explicit?parsed.finalidade:state.finalidade;
        const unitChanged=state.finalidade && budgetUnit(purpose)!==budgetUnit(state.finalidade);
        state={q:input.value,...parsed,finalidade:purpose};
        if(unitChanged) { state.preco_max=''; state.q=withoutBudget(state.q); }
        updateControls(); saveSearch(false);
        if(unitChanged) document.getElementById('search-status').textContent+=' Orçamento limpo: informe o valor para a nova finalidade.';
      }
      input.addEventListener('input',queryChanged);
      input.addEventListener('search',queryChanged);
      for(const [key,id] of Object.entries(fields)) document.getElementById(id).addEventListener('change',function(){
        if(!this.checkValidity()) { this.reportValidity(); return; }
        state.budgetCleared=false;
        // Preserve a pending budget on first selection; clear it when switching units.
        const unitChanged=key==='finalidade' && state.finalidade && budgetUnit(this.value)!==budgetUnit(state.finalidade);
        if(unitChanged) {
          state.preco_max='';
          state.q=withoutBudget(state.q);
        }
        // A manual selector choice supersedes purpose words in the old query.
        if(key==='finalidade') state.q=state.q.replace(/\b(?:comprar|compra|venda|alugar|aluguel|loca[cç][aã]o)\b/gi,' ').replace(/\s+/g,' ').trim();
        state[key]=this.value; updateControls(); saveSearch(true);
        if(unitChanged) document.getElementById('search-status').textContent+=' Orçamento limpo: informe o valor para a nova finalidade.';
      });
      document.getElementById('limpar-busca').addEventListener('click',function(){ state={q:'',...search.parse('')}; updateControls(); saveSearch(true); input.focus(); });
      window.addEventListener('popstate',restoreSearch);
    }

    const contatoForm = document.getElementById('contato-form');
    if (contatoForm) contatoForm.addEventListener('submit', onFormSubmit);
  });
})();
