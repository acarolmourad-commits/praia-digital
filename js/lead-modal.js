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

  function bindEvents(){
    var m = getModal();
    if(!m) return;

    m.addEventListener('click', function(e){
      if(e.target.classList.contains('lead-modal-backdrop') || e.target.classList.contains('lead-modal-close')){
        closeModal();
      }
    });

    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape' && m.dataset.open === '1') closeModal();
    });

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
        var msg = encodeURIComponent('Olá! Quero receber a Análise de Mercado Imobiliário em PDF. Nome: ' + name + ' WhatsApp: ' + phone);
        var success = m.querySelector('.lead-modal-success');
        if(success) success.style.display = 'block';
        if(form) form.style.display = 'none';
        window.open('https://wa.me/5511954346288?text=' + msg, '_blank');
      });
    }
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', bindEvents);
  } else {
    bindEvents();
  }
})();
