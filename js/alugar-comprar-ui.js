(function () {
  'use strict';
  const core = window.PDRentBuy;
  const form = document.getElementById('rent-buy-form');
  if (!core || !form) return;
  const byId = id => document.getElementById(id);
  const ids = { ...Object.fromEntries(Object.entries(core.fields).map(([key, field]) => [key, field.id])), rateType: 'tipoTaxa', amortization: 'sistema' };
  const currency = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
  const percent = new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 2 });
  const money = value => currency.format(Math.abs(value) < 0.005 ? 0 : value);
  const text = (id, value) => { byId(id).textContent = value; };
  const read = () => Object.fromEntries(Object.entries(ids).map(([key, id]) => [key, byId(id).value]));
  function clearErrors() {
    byId('error-summary').hidden = true;
    byId('error-list').replaceChildren();
    for (const id of Object.values(ids)) { byId(id).removeAttribute('aria-invalid'); text(`${id}-error`, ''); }
  }
  function showErrors(errors) {
    clearErrors();
    byId('res').hidden = true;
    for (const [key, error] of Object.entries(errors)) {
      const id = ids[key];
      const field = byId(id);
      field.setAttribute('aria-invalid', 'true');
      text(`${id}-error`, error);
      const item = document.createElement('li');
      const link = document.createElement('a');
      link.href = `#${id}`;
      link.textContent = `${core.fields[key]?.label || (key === 'rateType' ? 'Tipo de taxa' : 'Sistema de amortização')}: ${error}`;
      link.addEventListener('click', event => { event.preventDefault(); reveal(field); });
      item.append(link); byId('error-list').append(item);
    }
    byId('error-summary').hidden = false;
    text('result-live', 'Não foi possível comparar. Corrija os campos indicados.');
    reveal(byId(ids[Object.keys(errors)[0]]));
  }
  function reveal(field) {
    let parent = field.parentElement;
    while (parent) { if (parent.tagName === 'DETAILS') parent.open = true; parent = parent.parentElement; }
    field.focus();
  }
  function appendRow(tbody, cells) {
    const row = document.createElement('tr');
    cells.forEach((value, index) => {
      const cell = document.createElement(index === 0 ? 'th' : 'td');
      if (index === 0) cell.scope = 'row';
      cell.textContent = value;
      row.append(cell);
    });
    tbody.append(row);
  }
  function render(result, example, focus) {
    clearErrors();
    byId('res').hidden = false;
    const p = result.params;
    text('result-label', example ? 'Exemplo ilustrativo' : 'Cenário informado');
    text('result-title', `Patrimônio ao fim de ${p.horizonYears} ${p.horizonYears === 1 ? 'ano' : 'anos'}`);
    const verdict = result.outcome === 'close' ? 'Patrimônios próximos neste cenário.' :
      `${result.outcome === 'buy' ? 'Comprar' : 'Alugar e investir'} termina com ${money(Math.abs(result.difference))} a mais neste cenário.`;
    text('rVerdict', verdict);
    text('owner-wealth', money(result.ownerWealth));
    text('renter-wealth', money(result.renterWealth));
    text('owner-components', `Imóvel líquido ${money(result.netEquity)} + investimentos ${money(result.ownerInvestments)}.`);
    text('renter-components', `Capital inicial investido ${money(result.initialCash)} + aportes e rendimentos.`);
    const metrics = {
      'initial-cash': result.initialCash, 'purchase-costs': result.purchaseCosts,
      'financed': result.financed, 'rParc': result.firstPayment,
      'first-owner-cost': result.firstOwnerCost, 'first-renter-cost': result.firstRenterCost,
      'rAlug': result.totalRent, 'owner-outlay': result.ownerOutlay,
      'renter-outlay': result.renterOutlay, 'total-loan': result.totalLoanPayments,
      'total-interest': result.totalInterest, 'total-indexation': result.totalIndexation,
      'rImovel': result.property, 'remaining-debt': result.debt, 'sale-costs': result.sellingCosts,
      'sale-tax': result.saleTax, 'owner-contributions': result.ownerContributions,
      'renter-contributions': result.renterContributions
    };
    Object.entries(metrics).forEach(([id, amount]) => text(id, money(amount)));
    text('rate-description', result.financed === 0 ? 'Compra à vista: não há parcelas, juros ou seguros do financiamento.' :
      `${p.amortization === 'PRICE' ? 'Price' : 'SAC'} • juros de ${percent.format(p.annualInterest)}% a.a. ${p.rateType === 'nominal' ? 'nominais, com capitalização mensal' : 'efetivos'} (${percent.format(result.interestRate * 100)}% a.m.) • correção do saldo de ${percent.format(p.balanceIndex)}% a.a. no cenário.`);
    text('yield-info', `Aluguel inicial anual ÷ preço: ${percent.format(p.rent * 12 / p.price * 100)}%. Esse indicador não determina a conclusão.`);
    text('net-warning', result.netEquity < 0 ? 'Atenção: a venda estimada não cobre saldo devedor, custos e provisão de imposto. O déficit foi mantido no patrimônio.' :
      p.saleTax === 0 ? 'Imposto de venda não provisionado. Zero não significa isenção; consulte o valor aplicável ao seu caso.' : 'O imposto de venda é a provisão nominal que você informou, não um cálculo tributário.');
    const years = byId('yearly-body'); years.replaceChildren();
    result.yearly.forEach(row => appendRow(years, [String(row.year), money(row.property), money(row.debt), money(row.ownerWealth), money(row.renterWealth), money(row.difference)]));
    const sensitivity = byId('sensitivity-body'); sensitivity.replaceChildren();
    core.sensitivity(p).forEach(scenario => appendRow(sensitivity, [
      `${scenario.label} (${percent.format(scenario.rate)}% a.a.)`,
      scenario.result.valid ? money(scenario.result.difference) : 'Fora dos limites de taxa',
      scenario.result.valid ? scenario.result.outcome === 'close' ? 'Próximos' : scenario.result.outcome === 'buy' ? 'Comprar' : 'Alugar e investir' : 'Não calculado'
    ]));
    text('result-live', `${example ? 'Exemplo carregado. ' : 'Comparação atualizada. '}${verdict}`);
    if (focus) { byId('result-title').focus(); byId('result-title').scrollIntoView({ block: 'start', behavior: 'auto' }); }
  }
  function calculate(example, focus) {
    const result = core.calculate(read());
    if (!result.valid) { showErrors(result.errors); return; }
    render(result, example, focus);
  }
  form.addEventListener('submit', event => { event.preventDefault(); calculate(false, true); });
  form.addEventListener('input', event => {
    if (!Object.values(ids).includes(event.target.id)) return;
    byId('res').hidden = true;
    clearErrors();
    text('result-live', 'Premissas alteradas. Use Comparar patrimônios para atualizar o resultado.');
  });
  form.addEventListener('change', () => { byId('res').hidden = true; text('result-live', 'Premissas alteradas. Compare novamente.'); });
  form.addEventListener('reset', () => {
    byId('res').hidden = true;
    clearErrors();
    window.setTimeout(() => calculate(true, false), 0);
  });
  byId('restore-example').addEventListener('click', () => {
    Object.entries(ids).forEach(([key, id]) => { byId(id).value = core.defaults[key]; });
    calculate(true, true);
  });
  calculate(true, false);
  form.querySelector('[type="submit"]').disabled = false;
})();
