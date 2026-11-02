/* ============================================================
   Praia Digital — CTA nativo + captura de newsletter
   ============================================================ */
window.PD_LEADS = window.PD_LEADS || {};

PD_LEADS.injectCTA = function ({ selector = 'article', every = 4 } = {}) {
  const article = document.querySelector(selector);
  if (!article) return null;

  const paragraphs = Array.from(article.querySelectorAll('p'));
  const targetIndex = Math.min(every, paragraphs.length - 1);
  const target = paragraphs[targetIndex];
  if (!target || !target.parentNode) return null;

  const cta = document.createElement('div');
  cta.className = 'pd-cta-native';
  cta.setAttribute('data-pd-cta', 'native');
  cta.innerHTML = `
    <div class="pd-cta-native__inner">
      <p class="pd-cta-native__title">Quer vender ou alugar seu imóvel no litoral?</p>
      <p class="pd-cta-native__text">Fale agora com um especialista pelo WhatsApp.</p>
      <a class="pd-cta-native__button" href="https://wa.me/5511954346288?text=Ol%C3%A1,%20tenho%20interesse%20em%20${encodeURIComponent(document.title || 'Blog')}" target="_blank" rel="noopener">Atendimento pelo WhatsApp</a>
    </div>
  `;

  target.parentNode.insertBefore(cta, target.nextSibling);
  return cta;
};

PD_LEADS.injectNewsletter = function ({ selector = 'article' } = {}) {
  const article = document.querySelector(selector);
  if (!article) return null;

  const box = document.createElement('div');
  box.className = 'pd-newsletter';
  box.setAttribute('data-pd-newsletter', '');
  box.innerHTML = `
    <div class="pd-newsletter__inner">
      <p class="pd-newsletter__title">Acompanhe o boletim de inteligência</p>
      <p class="pd-newsletter__text">Fontes verificadas e contexto sobre o litoral, no site ou por RSS.</p>
      <p>Assinatura por e-mail ainda não está ativa. Nenhum cadastro é coletado aqui.</p>
      <a href="/docs/inteligencia/feed.xml">Acompanhar gratuitamente por RSS</a>
      <a href="/newsletter/assinatura.html">Status da assinatura</a>
    </div>
  `;

  article.appendChild(box);
  return box;
};

PD_LEADS.injectFloatingWhatsApp = function () {
  const btn = document.createElement('a');
  btn.className = 'pd-whatsapp-float';
  btn.setAttribute('data-pd-whatsapp-float', '');
  btn.href = 'https://wa.me/5511954346288?text=' + encodeURIComponent('Olá, tenho interesse em ' + (document.title || 'Blog'));
  btn.target = '_blank';
  btn.rel = 'noopener';
  btn.innerHTML = 'WhatsApp';
  document.body.appendChild(btn);
  return btn;
};
