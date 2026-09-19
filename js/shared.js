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
