/* Academy assisted enrollment: catalog is the only source of title and price. */
(function (root) {
  'use strict';
  const money = value => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
  function selectCourse(items, search) {
    const params = new URLSearchParams(search);
    const slug = params.get('course') || params.get('slug');
    if (!slug || !Array.isArray(items)) return null;
    return items.find(item => (item.slug === slug || (Array.isArray(item.aliases) && item.aliases.includes(slug))) && typeof item.title === 'string' &&
      typeof item.price === 'number' && Number.isFinite(item.price) && item.price >= 0 &&
      typeof item.path === 'string' && item.path.startsWith('/education/') && !item.path.includes('\\')) || null;
  }
  function messageFor(course) {
    const intro = 'Olá! Quero informações para matrícula assistida na Praia Digital Academy.';
    const selection = course ? '\nMaterial: ' + course.title + '\nValor anunciado: ' + money(course.price) + '\nPágina: https://praia.digital' + course.path : '\nGostaria de ajuda para escolher um material no catálogo.';
    return intro + selection + '\nEntendo que o conteúdo é 100% digital, para estudo autônomo. Por favor, confirmem os materiais incluídos, a forma e o prazo de entrega e as condições de pagamento antes da contratação.';
  }
  function contactLinks(course) {
    const body = messageFor(course);
    return { whatsapp: 'https://wa.me/5511954346288?text=' + encodeURIComponent(body),
      email: 'mailto:comercial@praia.digital?subject=' + encodeURIComponent('Matrícula assistida — Praia Digital Academy') + '&body=' + encodeURIComponent(body) };
  }
  async function init() {
    const status = document.getElementById('selection-status');
    const details = document.getElementById('selected-course');
    const whatsapp = document.getElementById('contact-whatsapp');
    const email = document.getElementById('contact-email');
    function apply(course) {
      const links = contactLinks(course);
      whatsapp.href = links.whatsapp;
      email.href = links.email;
      if (course) {
        document.getElementById('course-title').textContent = course.title;
        document.getElementById('course-price').textContent = money(course.price);
        document.getElementById('course-link').href = course.path;
        details.hidden = false;
        status.textContent = 'Material selecionado. O contato já incluirá o título e o valor anunciado abaixo.';
      }
    }
    apply(null);
    try {
      const response = await fetch('/education/assets/catalog.json', { cache: 'no-cache' });
      if (!response.ok) throw new Error('catalog');
      const course = selectCourse(await response.json(), window.location.search);
      if (course) apply(course);
      else status.textContent = 'Nenhum material válido foi selecionado. Escolha no catálogo ou peça orientação à equipe.';
    } catch (_) {
      status.textContent = 'Não foi possível confirmar o material e o valor agora. Consulte o catálogo ou peça confirmação à equipe antes de pagar.';
    }
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { selectCourse, messageFor, contactLinks };
  if (typeof document !== 'undefined') init();
})(typeof window !== 'undefined' ? window : globalThis);
