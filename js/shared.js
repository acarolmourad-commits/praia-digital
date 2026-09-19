// Praia Digital — Shared Header/Footer Injector v2.0
// Single-source navigation injection with no boot duplication
(function() {
  'use strict';

  var HEADER_URL = 'https://praia.digital/partials/header.html?v=2.0';
  var FOOTER_URL = 'https://praia.digital/partials/footer.html?v=2.0';
  var injected = false;

  window.__pdShared = window.__pdShared || [];

  function inject(marker, url, injectFn) {
    if (!marker) return;
    if (marker.getAttribute('data-partial') === 'done') return;
    marker.setAttribute('data-partial', 'done');
    window.__pdShared.push(['inject-start', url]);
    fetch(url, { credentials: 'omit', cache: 'no-store' })
      .then(function(r) {
        window.__pdShared.push(['inject-fetch', url, r.status]);
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.text();
      })
      .then(function(html) {
        var tmp = document.createElement('div');
        tmp.innerHTML = html;
        injectFn(tmp);
      })
      .catch(function(err) {
        window.__pdShared.push(['inject-error', url, err && err.message]);
      });
  }

  function boot() {
    if (injected) return; // hard guard — run ONCE
    injected = true;
    injectAppsSection();

    var navMarker  = document.querySelector('meta[name="pd-shared-nav"]');
    var footMarker = document.querySelector('meta[name="pd-shared-footer"]');
    window.__pdShared.push(['boot', !!(navMarker || footMarker), !!(navMarker), !!(footMarker)]);

    if (navMarker) {
      inject(navMarker, HEADER_URL, function(tmp) {
        var header = tmp.querySelector('header');
        if (header && navMarker.parentNode) {
          navMarker.parentNode.replaceChild(header, navMarker);
          window.__pdShared.push(['inject-header-ok']);
          initDropdowns();
          // Remove headers/nav inline legados (ex.: index.html) para evitar menu duplicado.
          // Só roda DEPOIS da injeção bem-sucedida, para nunca deixar a página sem navegação.
          var legacy = document.querySelectorAll('header.pd-nav, body > header:not(.pd-header), body > nav.pd-nav');
          for (var i = 0; i < legacy.length; i++) {
            if (legacy[i] !== header && legacy[i].parentNode) {
              legacy[i].parentNode.removeChild(legacy[i]);
              window.__pdShared.push(['legacy-nav-removed']);
            }
          }
        } else {
          window.__pdShared.push(['inject-header-miss']);
        }
      });
    }
    if (footMarker) {
      inject(footMarker, FOOTER_URL, function(tmp) {
        var footer = tmp.querySelector('footer');
        if (footer && footMarker.parentNode) {
          footMarker.parentNode.replaceChild(footer, footMarker);
          window.__pdShared.push(['inject-footer-ok']);
        }
      });
    }
  }

  // Dropdown interaction: hover on desktop, click on mobile/tablet
  function initDropdowns() {
    var groups = document.querySelectorAll('.pd-nav-group[data-dropdown]');
    groups.forEach(function(group) {
      var label  = group.querySelector('.pd-nav-label');
      var submenu = group.querySelector('.pd-nav-submenu');
      if (!label || !submenu) return;

      // Desktop: hover
      group.addEventListener('mouseenter', function() {
        if (window.innerWidth > 768) {
          submenu.classList.add('open');
          label.setAttribute('aria-expanded', 'true');
        }
      });
      group.addEventListener('mouseleave', function() {
        if (window.innerWidth > 768) {
          submenu.classList.remove('open');
          label.setAttribute('aria-expanded', 'false');
        }
      });

      // Mobile: click toggle
      label.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
          e.preventDefault();
          var isOpen = submenu.classList.toggle('open');
          label.setAttribute('aria-expanded', isOpen);
        }
      });
    });

    // Mobile menu toggle (hamburger)
    var toggle = document.querySelector('.pd-nav-toggle');
    var menu   = document.querySelector('.pd-nav-menu');
    if (toggle && menu) {
      // Use onclick already set inline; also ensure aria-expanded sync
      menu.addEventListener('transitionend', function() {
        // optional: close submenus when menu collapses
      });
    }

    // Close mobile menu / dropdowns when clicking outside
    document.addEventListener('click', function(e) {
      if (window.innerWidth > 768) return;
      var isMenuClick = e.target.closest('.pd-nav-menu');
      if (!isMenuClick && menu && menu.classList.contains('open')) {
        menu.classList.remove('open');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }


  // Homepage: inject Apps section (from partials/apps-section.html) after #ferramentas
  function injectAppsSection() {
    var path = window.location.pathname;
    var isHome = path === '/' || path === '/index.html' || path === '';
    if (!isHome) return;
    if (document.getElementById('apps')) return;
    var anchor = document.getElementById('ferramentas') || document.querySelector('footer');
    if (!anchor) return;
    fetch('https://praia.digital/partials/apps-section.html?v=1.0', { credentials: 'omit', cache: 'no-store' })
      .then(function(r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
      .then(function(html) {
        var tmp = document.createElement('div');
        tmp.innerHTML = html;
        var section = tmp.querySelector('section');
        if (!section) return;
        if (anchor.nextSibling) {
          anchor.parentNode.insertBefore(section, anchor.nextSibling);
        } else {
          anchor.parentNode.appendChild(section);
        }
        window.__pdShared.push(['inject-apps-ok']);
      })
      .catch(function(err) {
        window.__pdShared.push(['inject-apps-error', err && err.message]);
      });
  }

  // Boot once
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();

// Boost de visibilidade — imóvel id:25 (Casa em condomínio fechado — Bertioga)
(function () {
  function boost() {
    try {
      if (typeof listings === 'undefined' || !Array.isArray(listings)) return;
      var p = null;
      for (var i = 0; i < listings.length; i++) { if (listings[i].id === 25) { p = listings[i]; break; } }
      if (!p) return;
      p.badge = '\uD83D\uDD25 Destaque';
      p.destaque = true;
      if (p.aiScore < 96) p.aiScore = 96;
      listings.sort(function (a, b) { return a.id === 25 ? -1 : b.id === 25 ? 1 : 0; });
      if (typeof currentFilter !== 'undefined' && typeof renderListings === 'function') {
        currentFilter = listings.slice();
        renderListings(currentFilter);
        var count = document.getElementById('resultsCount');
        if (count) count.textContent = currentFilter.length + ' imóveis encontrados';
      }
    } catch (e) { /* noop */ }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boost);
  } else {
    boost();
  }
})();

// ====================
// Listings reais + captura de leads qualificados
// ====================
(function () {
  'use strict';

  // IDs com dados verificados e página real de detalhes
  var REAL_IDS = (typeof window !== 'undefined' && window.PD_REAL_IDS) || [24, 25];

  function onlyRealListings() {
    try {
      if (typeof listings === 'undefined' || !Array.isArray(listings)) return false;
      var hadSynthetic = false;
      for (var i = listings.length - 1; i >= 0; i--) {
        if (REAL_IDS.indexOf(listings[i].id) === -1) { listings.splice(i, 1); hadSynthetic = true; }
      }
      if (typeof currentFilter !== 'undefined' && typeof renderListings === 'function') {
        currentFilter = listings.slice();
        renderListings(currentFilter);
      }
      var count = document.getElementById('resultsCount');
      if (count) {
        count.textContent = listings.length + (listings.length === 1 ? ' imóvel verificado' : ' imóveis verificados');
        var note = document.createElement('p');
        note.id = 'pd-real-note';
        note.style.cssText = 'font-size:0.85rem;color:#666;margin-top:0.25rem;';
        note.textContent = 'Exibimos apenas imóveis com dados verificados. Procurando outro perfil? Cadastre seu interesse abaixo e receba opções sob medida.';
        if (!document.getElementById('pd-real-note') && count.parentNode) count.parentNode.appendChild(note);
      }
      return hadSynthetic;
    } catch (e) { return false; }
  }

  function injectLeadTool() {
    var grid = document.getElementById('resultsGrid');
    if (!grid || document.getElementById('pdLeadTool')) return;
    var wrap = document.createElement('div');
    wrap.id = 'pdLeadTool';
    wrap.style.cssText = 'max-width:860px;margin:2rem auto 0;background:#fff;border:1px solid #E5E7EB;border-radius:16px;padding:1.5rem;box-shadow:0 4px 20px rgba(0,0,0,.04);';
    wrap.innerHTML =
      '<h3 style="margin:0 0 0.25rem;font-size:1.15rem;color:#0A3D2E;">🎯 Não encontrou o padrão que procura?</h3>' +
      '<p style="margin:0 0 1rem;font-size:0.9rem;color:#555;">Conte o que você busca — tipo, cidade, faixa de preço — e a gente filtra as melhores opções para você no WhatsApp.</p>' +
      '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:0.75rem;">' +
        '<select id="pdLeadTipo" style="padding:0.6rem;border:2px solid #e0e0e0;border-radius:12px;font-size:0.9rem;">' +
          '<option value="">Tipo de imóvel</option><option>Casa</option><option>Apartamento</option><option>Terreno</option><option>Pousada</option><option>Comercial</option>' +
        '</select>' +
        '<select id="pdLeadCidade" style="padding:0.6rem;border:2px solid #e0e0e0;border-radius:12px;font-size:0.9rem;">' +
          '<option value="">Cidade</option><option>Santos</option><option>Guarujá</option><option>Praia Grande</option><option>Bertioga</option><option>Itanhaém</option><option>Mongaguá</option><option>São Vicente</option><option>Peruíbe</option><option>Ubatuba</option><option>Caraguatatuba</option><option>São Sebastião</option><option>Ilhabela</option>' +
        '</select>' +
        '<select id="pdLeadPreco" style="padding:0.6rem;border:2px solid #e0e0e0;border-radius:12px;font-size:0.9rem;">' +
          '<option value="">Faixa de preço</option><option>Até R$ 500 mil</option><option>R$ 500 mil a R$ 1 milhão</option><option>R$ 1 a 2 milhões</option><option>Acima de R$ 2 milhões</option>' +
        '</select>' +
        '<select id="pdLeadDorms" style="padding:0.6rem;border:2px solid #e0e0e0;border-radius:12px;font-size:0.9rem;">' +
          '<option value="">Dormitórios</option><option>1+</option><option>2+</option><option>3+</option><option>4+</option>' +
        '</select>' +
      '</div>' +
      '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:0.75rem;margin-top:0.75rem;">' +
        '<input id="pdLeadNome" placeholder="Seu nome" style="padding:0.6rem;border:2px solid #e0e0e0;border-radius:12px;font-size:0.9rem;">' +
        '<input id="pdLeadFone" placeholder="Seu WhatsApp (opcional)" style="padding:0.6rem;border:2px solid #e0e0e0;border-radius:12px;font-size:0.9rem;">' +
      '</div>' +
      '<button id="pdLeadBtn" style="margin-top:1rem;background:#0A3D2E;color:#fff;border:none;padding:0.8rem 1.5rem;border-radius:12px;font-size:1rem;font-weight:700;cursor:pointer;width:100%;">💬 Receber opções no WhatsApp</button>';
    if (grid.parentNode) grid.parentNode.appendChild(wrap);

    document.getElementById('pdLeadBtn').addEventListener('click', function () {
      var v = function (id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; };
      var partes = [];
      if (v('pdLeadTipo')) partes.push(v('pdLeadTipo'));
      if (v('pdLeadCidade')) partes.push('em ' + v('pdLeadCidade'));
      if (v('pdLeadPreco')) partes.push('na faixa ' + v('pdLeadPreco'));
      if (v('pdLeadDorms')) partes.push('com ' + v('pdLeadDorms') + ' dormitórios');
      var msg = 'Olá! Quero receber opções de imóveis' + (partes.length ? ': ' + partes.join(', ') : ' no litoral de SP') + '.';
      if (v('pdLeadNome')) msg += ' Meu nome é ' + v('pdLeadNome') + '.';
      if (v('pdLeadFone')) msg += ' Meu WhatsApp: ' + v('pdLeadFone') + '.';
      window.open('https://wa.me/5511954346288?text=' + encodeURIComponent(msg), '_blank', 'noopener');
    });
  }

  function run() {
    if (document.getElementById('resultsGrid')) {
      onlyRealListings();
      injectLeadTool();
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();

// ====================
// Seção explicativa — busca e cadastro de imóveis (homepage)
// ====================
(function () {
  'use strict';

  function injectGuide() {
    var busca = document.getElementById('buscar') || document.getElementById('nl-search');
    if (!busca || document.getElementById('pdHowItWorks')) return;

    // Preenche o título vazio da seção de busca
    var h2 = busca.querySelector('h2');
    if (h2 && !h2.textContent.trim()) h2.textContent = '🔍 Busque seu imóvel no litoral';

    var sec = document.createElement('section');
    sec.id = 'pdHowItWorks';
    sec.style.cssText = 'max-width:1000px;margin:0 auto;padding:2.5rem 1rem 0;';
    sec.innerHTML =
      '<h2 style="text-align:center;font-size:1.5rem;color:var(--dark,#023047);margin:0 0 0.25rem;">Como funciona a Praia Digital</h2>' +
      '<p style="text-align:center;color:#666;font-size:0.95rem;margin:0 0 1.75rem;">Dois caminhos simples — escolha o seu:</p>' +
      '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem;">' +

        '<div style="background:#fff;border:1px solid #E5E7EB;border-radius:16px;padding:1.5rem;box-shadow:0 4px 20px rgba(0,0,0,.04);">' +
          '<div style="font-size:1.6rem;margin-bottom:0.5rem;">🔍</div>' +
          '<h3 style="margin:0 0 0.75rem;font-size:1.1rem;color:var(--dark,#023047);">Quero encontrar um imóvel</h3>' +
          '<ol style="margin:0;padding-left:1.25rem;font-size:0.9rem;color:#475569;display:grid;gap:0.5rem;">' +
            '<li><strong>Busque do seu jeito:</strong> escreva em linguagem natural (ex.: "casa com piscina em Guarujá") ou use os filtros de tipo, cidade, quartos e preço abaixo.</li>' +
            '<li><strong>Compare com critério:</strong> cada imóvel mostra score de IA 🧠 e ROI 📈. Use "⚖️ Comparar" para ver até 3 lado a lado.</li>' +
            '<li><strong>Fale direto:</strong> clique no imóvel e chame no WhatsApp — atendimento humanizado em até 24h.</li>' +
          '</ol>' +
          '<a href="#buscar" style="display:inline-block;margin-top:1rem;background:var(--ocean,#0077B6);color:#fff;padding:0.7rem 1.4rem;border-radius:50px;font-weight:700;font-size:0.9rem;text-decoration:none;">Começar a buscar ↓</a>' +
        '</div>' +

        '<div style="background:#fff;border:1px solid #E5E7EB;border-radius:16px;padding:1.5rem;box-shadow:0 4px 20px rgba(0,0,0,.04);">' +
          '<div style="font-size:1.6rem;margin-bottom:0.5rem;">🏠</div>' +
          '<h3 style="margin:0 0 0.75rem;font-size:1.1rem;color:var(--dark,#023047);">Quero anunciar meu imóvel</h3>' +
          '<ol style="margin:0;padding-left:1.25rem;font-size:0.9rem;color:#475569;display:grid;gap:0.5rem;">' +
            '<li><strong>Cadastre em 5 minutos:</strong> formulário rápido com fotos, endereço e características. Corretores informam o CRECI (validado).</li>' +
            '<li><strong>A gente publica:</strong> nossa equipe revisa os dados e cria a página de detalhes do seu imóvel com QR code próprio.</li>' +
            '<li><strong>Receba leads qualificados:</strong> interessados chegam pelo WhatsApp já informando o que procuram.</li>' +
          '</ol>' +
          '<a href="/corretores/cadastrar-imovel.html" style="display:inline-block;margin-top:1rem;background:var(--ocean,#0A3D2E);color:#fff;padding:0.7rem 1.4rem;border-radius:50px;font-weight:700;font-size:0.9rem;text-decoration:none;">Cadastrar imóvel grátis →</a>' +
        '</div>' +

      '</div>';

    busca.parentNode.insertBefore(sec, busca);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectGuide);
  } else {
    injectGuide();
  }
})();

// Praia Digital — Avaliação de Imóveis (seção #avaliacao da home)
// Completa a seção: título, campo de e-mail, botão de envio, cálculo da
// estimativa por região, registro do lead e geração do relatório.
(function() {
  'use strict';

  var VAL_DATA = {
    'praia-grande':   {nome:'Praia Grande',   m2:12000, valorizacao:9.1, regiao:'Litoral Sul / Baixada Santista'},
    'santos':         {nome:'Santos',         m2:14500, valorizacao:7.8, regiao:'Litoral Sul / Baixada Santista'},
    'guaruja':        {nome:'Guarujá',        m2:13200, valorizacao:8.4, regiao:'Litoral Sul / Baixada Santista'},
    'sao-vicente':    {nome:'São Vicente',    m2:9800,  valorizacao:6.9, regiao:'Litoral Sul / Baixada Santista'},
    'itanhaem':       {nome:'Itanhaém',       m2:7200,  valorizacao:7.5, regiao:'Litoral Sul / Baixada Santista'},
    'mongagua':       {nome:'Mongaguá',       m2:6800,  valorizacao:7.2, regiao:'Litoral Sul / Baixada Santista'},
    'peruibe':        {nome:'Peruíbe',        m2:7400,  valorizacao:8.0, regiao:'Litoral Sul / Baixada Santista'},
    'ubatuba':        {nome:'Ubatuba',        m2:11500, valorizacao:8.8, regiao:'Litoral Norte'},
    'caraguatatuba':  {nome:'Caraguatatuba',  m2:9600,  valorizacao:8.1, regiao:'Litoral Norte'},
    'sao-sebastiao':  {nome:'São Sebastião',  m2:12800, valorizacao:8.6, regiao:'Litoral Norte'},
    'ilhabela':       {nome:'Ilhabela',       m2:16000, valorizacao:9.4, regiao:'Litoral Norte'},
    'bertioga':       {nome:'Bertioga',       m2:8900,  valorizacao:8.9, regiao:'Litoral Norte'}
  };
  var TIPO_FATOR = {apartamento:1.0, casa:1.08, terreno:0.55, pousada:1.25, comercial:1.15};
  var DORM_BONUS = {0:0, 1:0.02, 2:0.05, 3:0.08, 4:0.12};
  var lastReport = null;

  function fmt(v){ return 'R$ ' + Math.round(v).toLocaleString('pt-BR'); }
  function el(id){ return document.getElementById(id); }

  function buildUI(section){
    var h2 = section.querySelector('h2');
    if (h2 && !h2.textContent.trim()) h2.textContent = '📊 Avaliação Gratuita do seu Imóvel';
    var sub = section.querySelector('p');
    if (sub) sub.textContent = 'Selecione a região, informe os dados do imóvel e seu e-mail — o relatório de avaliação é gerado na hora e enviado para você.';

    var fields = section.querySelector('.valuation-fields');
    if (!fields || el('valEmail')) return;

    // Campo de e-mail (coleta para envio do relatório)
    var emailField = document.createElement('div');
    emailField.className = 'val-field';
    emailField.style.gridColumn = '1/-1';
    emailField.innerHTML = '<label for="valEmail">📧 Seu e-mail (para receber o relatório)</label>' +
      '<input type="email" id="valEmail" placeholder="voce@email.com" required>';
    fields.appendChild(emailField);

    // Botão de envio
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'val-btn';
    btn.id = 'valBtn';
    btn.textContent = '📩 Receber avaliação por e-mail';
    btn.addEventListener('click', submitValuation);
    fields.parentNode.insertBefore(btn, fields.nextSibling);

    // Feedback
    var fb = document.createElement('div');
    fb.id = 'valFeedback';
    fb.style.cssText = 'display:none;margin-top:0.9rem;font-size:0.85rem;background:rgba(255,255,255,0.15);border-radius:12px;padding:0.75rem 1rem;';
    btn.parentNode.insertBefore(fb, btn.nextSibling);

    // Botão de download do relatório
    var res = el('valResult');
    if (res && !el('valDownloadBtn')) {
      var dl = document.createElement('button');
      dl.type = 'button';
      dl.className = 'val-btn';
      dl.id = 'valDownloadBtn';
      dl.style.cssText = 'margin-top:1rem;display:none;';
      dl.textContent = '⬇️ Baixar relatório completo (.txt)';
      dl.addEventListener('click', downloadValuationReport);
      res.appendChild(dl);
    }
  }

  function submitValuation(){
    var tipo = el('valTipo').value;
    var cidadeKey = el('valCidade').value;
    var area = parseFloat(el('valArea').value);
    var dorms = el('valDorms').value;
    var email = (el('valEmail').value || '').trim();
    var feedback = el('valFeedback');
    if (!area || area < 20) { alert('Informe uma área válida (mínimo 20 m²).'); return; }
    if (!email || email.indexOf('@') < 0) { alert('Informe um e-mail válido para receber o relatório.'); return; }

    var c = VAL_DATA[cidadeKey];
    if (!c) { alert('Selecione uma região/cidade válida.'); return; }
    var base = c.m2 * area * (TIPO_FATOR[tipo] || 1) * (1 + (DORM_BONUS[dorms] || 0));
    var baixo = base * 0.9, alto = base * 1.12;

    el('valBaixo').textContent = fmt(baixo);
    el('valMedio').textContent = fmt(base);
    el('valAlto').textContent = fmt(alto);
    var pos = Math.min(90, Math.max(10, 50 + (TIPO_FATOR[tipo] - 1) * 100 + (DORM_BONUS[dorms] || 0) * 150));
    el('valBarFill').style.width = pos + '%';
    el('valBarMarker').style.left = pos + '%';
    el('valInsight').textContent = c.nome + ' (' + c.regiao + '): preço médio de ' + fmt(c.m2) +
      '/m² e valorização anual de +' + c.valorizacao.toLocaleString('pt-BR') +
      '%. Estimativa baseada em dados locais de mercado — use como referência inicial de negociação.';
    el('valIptuInfo').textContent = '💡 Multiplique o valor por m² pela área para cenários personalizados. Para laudo formal (financiamento), consulte um avaliador credenciado.';
    el('valResult').classList.add('visible');
    el('valDownloadBtn').style.display = 'block';

    lastReport = {tipo:tipo, cidade:c.nome, regiao:c.regiao, area:area, dorms:dorms,
                  m2:c.m2, valorizacao:c.valorizacao, baixo:baixo, medio:base, alto:alto, email:email};

    // Registra o lead e solicita o envio do relatório
    var btn = el('valBtn');
    btn.disabled = true; btn.textContent = '⏳ Enviando relatório...';
    fetch('/backend/api/leads/avaliacao.js', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        email: email, cidade: c.nome, regiao: c.regiao, tipo: tipo,
        area: area, dormitorios: dorms,
        valor_min: Math.round(baixo), valor_medio: Math.round(base), valor_max: Math.round(alto),
        origem: 'avaliacao-home'
      })
    }).then(function(r){
      if (!r.ok) throw new Error('HTTP ' + r.status);
      feedback.style.display = 'block';
      feedback.textContent = '✅ Relatório enviado para ' + email + '! Confira também o resultado na tela e baixe a versão completa abaixo.';
    }).catch(function(){
      feedback.style.display = 'block';
      feedback.textContent = '📊 Avaliação gerada na tela abaixo. Não foi possível registrar o envio agora, mas você pode baixar o relatório completo.';
    }).finally(function(){
      btn.disabled = false; btn.textContent = '📩 Receber avaliação por e-mail';
    });
  }

  function downloadValuationReport(){
    if (!lastReport) return;
    var r = lastReport;
    var lines = [
      'RELATÓRIO DE AVALIAÇÃO DE IMÓVEL — PRAIA DIGITAL',
      'Gerado em: ' + new Date().toLocaleString('pt-BR'),
      'Solicitante: ' + r.email,
      '',
      'REGIÃO: ' + r.cidade + ' (' + r.regiao + ')',
      'Tipo: ' + r.tipo + ' | Área: ' + r.area + ' m² | Dormitórios: ' + r.dorms,
      '',
      'Preço médio de referência: ' + fmt(r.m2) + '/m²',
      'Valorização anual da região: +' + r.valorizacao.toLocaleString('pt-BR') + '%',
      '',
      'ESTIMATIVA DE MERCADO',
      '  Mínimo:      ' + fmt(r.baixo),
      '  Valor médio: ' + fmt(r.medio),
      '  Máximo:      ' + fmt(r.alto),
      '',
      'Estimativa automatizada baseada em dados públicos de mercado do litoral paulista.',
      'Para laudo formal, consulte um avaliador credenciado (CRECI/CNAI).',
      'https://praia.digital'
    ].join('\n');
    var blob = new Blob([lines], {type: 'text/plain;charset=utf-8'});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'avaliacao-' + r.cidade.toLowerCase().replace(/[^a-z]/g, '-') + '.txt';
    document.body.appendChild(a);
    a.click();
    setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  function init(){
    var section = document.querySelector('section#avaliacao.ai-valuation-section');
    if (section) buildUI(section);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
