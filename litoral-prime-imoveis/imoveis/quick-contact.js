(function(){
  const container = document.getElementById('lp-quick-contact');
  if (!container) return;
  const titleEl = document.querySelector('title');
  const pageTitle = (titleEl && titleEl.textContent ? titleEl.textContent.trim() : '') || (document.querySelector('h1') ? document.querySelector('h1').textContent.trim() : '');
  const slug = (location.pathname.split('/').pop() || '').replace(/\.html$/,'');
  const waNum = '5511954346288';
  container.innerHTML = `
    <form id="lp-quick-form" style="display:flex;flex-direction:column;gap:10px">
      <h3>Contato rápido</h3>
      <input id="lp-q-name" placeholder="Seu nome" required>
      <input id="lp-q-phone" placeholder="Seu WhatsApp" required>
      <textarea id="lp-q-msg" rows="3" placeholder="Mensagem">Tenho interesse no imóvel: ${pageTitle || slug}</textarea>
      <button type="submit" class="btn btn-primary">Enviar pelo WhatsApp</button>
    </form>
    <p id="lp-q-msg" style="margin-top:10px;color:#0f172a"></p>
  `;
  const form = document.getElementById('lp-quick-form');
  if (!form) return;
  form.addEventListener('submit', function(e){
    e.preventDefault();
    const name = document.getElementById('lp-q-name').value.trim();
    const phone = document.getElementById('lp-q-phone').value.trim();
    const msg = document.getElementById('lp-q-msg').value.trim();
    const text = encodeURIComponent(`Olá! Meu nome é ${name || 'um visitante'}. ${msg} ${phone ? 'Meu WhatsApp: ' + phone : ''}`);
    const waUrl = `https://wa.me/${waNum}?text=${text}`;
    const row = {ts: new Date().toISOString(), title: pageTitle, slug, name, phone, msg, url: location.href};
    try {
      const key = 'lp_leads_v1';
      const arr = JSON.parse(localStorage.getItem(key) || '[]');
      arr.push(row);
      localStorage.setItem(key, JSON.stringify(arr.slice(-200)));
      if (window.LP_TRACK && typeof window.LP_TRACK.track === 'function') {
        window.LP_TRACK.track('quick-contact', msg);
      }
    } catch {}
    const el = document.getElementById('lp-q-msg');
    if (el) el.innerHTML = `Cadastro salvo. <a href="${waUrl}" target="_blank" rel="noopener">Abrir WhatsApp</a>.`;
  });
})();
