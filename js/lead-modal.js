(function(){
  var STORAGE_KEY = 'praia_digital_lead_modal_shown';
  var shown = false;
  try { shown = sessionStorage.getItem(STORAGE_KEY) === '1'; } catch(e){}

  function getModal(){
    return document.getElementById('leadModal');
  }

  function openModal(){
    var m = getModal();
    if(!m || m.dataset.open === '1') return;
    m.setAttribute('aria-hidden', 'false');
    m.classList.add('is-open');
    m.dataset.open = '1';
  }

  function closeModal(){
    var m = getModal();
    if(!m) return;
    m.setAttribute('aria-hidden', 'true');
    m.classList.remove('is-open');
    m.dataset.open = '0';
  }

  function markShown(){
    try { sessionStorage.setItem(STORAGE_KEY, '1'); } catch(e){}
  }

  function maybeOpen(){
    if(shown) return;
    openModal();
    markShown();
  }

  function saveLeadSilently(name, phone){
    try {
      var payload = {
        nome: name,
        telefone: phone,
        origem: 'Modal de Captura',
        timestamp: new Date().toISOString(),
        material: 'Analise de Mercado PDF'
      };
      if(navigator.sendBeacon){
        var blob = new Blob([JSON.stringify(payload)], {type: 'application/json'});
        navigator.sendBeacon('/api/leads', blob);
      }
    } catch(e){}
  }

  function bindEvents(){
    var m = getModal();
    var backdrop = m ? m.querySelector('.lead-modal-backdrop') : null;
    var closeBtn = m ? m.querySelector('.lead-modal-close') : null;
    if(backdrop){ backdrop.addEventListener('click', closeModal); }
    if(closeBtn){ closeBtn.addEventListener('click', closeModal); }

    var scrollTarget = Math.max(300, Math.floor(document.body.scrollHeight * 0.6));
    window.addEventListener('scroll', function(){
      if(shown) return;
      if(window.scrollY >= scrollTarget){
        maybeOpen();
      }
    }, {passive:true});

    document.addEventListener('mouseout', function(e){
      if(shown) return;
      if(e.clientY <= 0){
        maybeOpen();
      }
    });

    var form = document.getElementById('leadModalForm');
    if(form){
      form.addEventListener('submit', function(e){
        e.preventDefault();
        var name = (document.getElementById('leadName')||{}).value || '';
        var phone = (document.getElementById('leadPhone')||{}).value || '';
        if(!name || !phone){ return; }
        saveLeadSilently(name, phone);
        var success = m.querySelector('.lead-modal-success');
        if(success) success.style.display = 'block';
        if(form) form.style.display = 'none';
        var title = m.querySelector('h2');
        if(title) title.textContent = 'Análise liberada!';
        var desc = m.querySelector('p');
        if(desc) desc.textContent = 'Essa é uma demonstração estática. Na versão final, aqui será exibido o PDF para download.';
      });
    }
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', bindEvents);
  } else {
    bindEvents();
  }
})();
