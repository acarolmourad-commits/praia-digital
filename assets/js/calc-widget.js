/* ============================================================
   Praia Digital — Calculadora Imobiliária Widget
   ============================================================ */
window.PD_CALC = window.PD_CALC || {};

PD_CALC.init = function ({ container = '.pd-calc', currency = 'BRL' } = {}) {
  const root = document.querySelector(container);
  if (!root) return null;

  const priceInput = root.querySelector('.pd-calc__input[data-field="price"]');
  const taxInput = root.querySelector('.pd-calc__input[data-field="tax"]');
  const modeSelect = root.querySelector('.pd-calc__select[data-field="mode"]');
  const nightsInput = root.querySelector('.pd-calc__input[data-field="nights"]');
  const dailyInput = root.querySelector('.pd-calc__input[data-field="daily"]');
  const resultBox = root.querySelector('.pd-calc__result');
  const resultBody = root.querySelector('.pd-calc__result-body');

  const fmt = (n) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency }).format(n || 0);

  const calculate = () => {
    const price = parseFloat((priceInput && priceInput.value) || 0);
    const tax = parseFloat((taxInput && taxInput.value) || 0);
    const mode = (modeSelect && modeSelect.value) || 'season';
    const nights = parseFloat((nightsInput && nightsInput.value) || 0);
    const daily = parseFloat((dailyInput && dailyInput.value) || 0);

    const grossSeason = daily * nights;
    const effectiveSeason = grossSeason - tax;

    const monthlyRent = price * 0.004;
    const annualRent = monthlyRent * 12;
    const effectiveAnnual = annualRent - tax;

    const base = mode === 'season' ? effectiveSeason : effectiveAnnual;
    const compare = mode === 'season' ? effectiveAnnual : effectiveSeason;

    const roi = price > 0 ? (base / price) * 100 : 0;

    resultBody.innerHTML = `
      <div class="pd-calc__result-row"><span>Receita estimada</span><span>${fmt(base)}</span></div>
      <div class="pd-calc__result-row"><span>Receita comparativa</span><span>${fmt(compare)}</span></div>
      <div class="pd-calc__result-row"><span>ROI estimado</span><span>${roi.toFixed(2)}%</span></div>
    `;
    resultBox.classList.add('is-visible');
  };

  const reset = () => {
    if (priceInput) priceInput.value = '';
    if (taxInput) taxInput.value = '';
    if (modeSelect) modeSelect.value = 'season';
    if (nightsInput) nightsInput.value = '';
    if (dailyInput) dailyInput.value = '';
    resultBox.classList.remove('is-visible');
  };

  const calcBtn = root.querySelector('.pd-calc__button[data-action="calculate"]');
  const resetBtn = root.querySelector('.pd-calc__button[data-action="reset"]');

  if (calcBtn) calcBtn.addEventListener('click', calculate);
  if (resetBtn) resetBtn.addEventListener('click', reset);

  return { calculate, reset };
};
