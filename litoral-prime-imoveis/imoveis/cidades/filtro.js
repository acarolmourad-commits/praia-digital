(function(){
  const cards = Array.from(document.querySelectorAll('.servico-card'));
  const typeSelect = document.getElementById('lp-filter-type');
  const maxSelect = document.getElementById('lp-filter-max');
  if(!cards.length || !typeSelect) return;

  function apply(){
    const t = typeSelect.value;
    const max = maxSelect.value ? parseFloat(maxSelect.value.replace(/[^0-9]/g,'')) : NaN;
    cards.forEach(card=>{
      const meta = card.querySelector('p')?.textContent || '';
      const typeOk = !t || meta.toLowerCase().includes(t);
      const raw = meta.match(/([0-9.,]+)/);
      const price = raw ? parseFloat(raw[1].replace(/\./g,'').replace(',','.')) : NaN;
      const maxOk = isNaN(max) || (isNaN(price) || price <= max);
      card.style.display = (typeOk && maxOk) ? '' : 'none';
    });
  }
  typeSelect.addEventListener('change', apply);
  maxSelect.addEventListener('input', apply);
})();
