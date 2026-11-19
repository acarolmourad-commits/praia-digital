(() => {
  'use strict';
  const boxes = [...document.querySelectorAll('.guide-route input[type="checkbox"]')];
  const progress = document.getElementById('guide-progress');
  const update = () => {
    progress.textContent = `${boxes.filter(box => box.checked).length} de ${boxes.length} conferências marcadas`;
  };
  boxes.forEach(box => box.addEventListener('change', update));
  // Back/forward navigation can restore checkbox state without firing change.
  window.addEventListener('pageshow', update);
  document.getElementById('guide-reset').addEventListener('click', () => {
    boxes.forEach(box => { box.checked = false; });
    update();
  });
  document.getElementById('guide-print').addEventListener('click', () => window.print());
  document.getElementById('guide-actions').hidden = false;
  update();
})();
