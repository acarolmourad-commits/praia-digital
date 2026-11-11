(function (root, factory) {
  'use strict';
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.CompraViabilidade = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const references = Object.freeze({
    'Santos': 8678, 'Guarujá': 6944, 'Praia Grande': 6800
  });
  const monthlyRate = annualPercent => Math.pow(1 + annualPercent / 100, 1 / 12) - 1;
  function schedule(principal, months, annualRate, system) {
    if (!principal) return [];
    const rate = monthlyRate(annualRate);
    const fixed = rate === 0 ? principal / months : principal * rate / (1 - Math.pow(1 + rate, -months));
    let balance = principal;
    return Array.from({ length: months }, (_, index) => {
      const interest = balance * rate;
      const amortization = index === months - 1 ? balance : Math.min(balance, system === 'sac' ? principal / months : fixed - interest);
      const payment = interest + amortization;
      balance = Math.max(0, balance - amortization);
      return { payment, interest, amortization, balance };
    });
  }
  function validate(v) {
    const errors = {};
    const number = (key, min, max, label, integer = false) => {
      if (typeof v[key] !== 'number' || !Number.isFinite(v[key])) errors[key] = 'Informe ' + label + '.';
      else if (v[key] < min || v[key] > max || (integer && !Number.isInteger(v[key]))) {
        errors[key] = label + ': use ' + (integer ? 'um número inteiro ' : 'um valor ') + 'entre ' + min.toLocaleString('pt-BR') + ' e ' + max.toLocaleString('pt-BR') + '.';
      }
    };
    if (!['moradia', 'temporada', 'anual'].includes(v.goal)) errors.goal = 'Escolha o objetivo da compra.';
    if (!['financiado', 'avista'].includes(v.purchase)) errors.purchase = 'Escolha a forma de compra.';
    if (!v.city) errors.city = 'Escolha uma cidade ou Outra cidade.';
    number('price', 1, 1e9, 'o preço do imóvel');
    number('area', 0.01, 1e6, 'a área útil');
    if (v.purchase === 'financiado') {
      number('entry', 0, 1e9, 'a entrada');
      if (Number.isFinite(v.price) && v.entry > v.price) errors.entry = 'A entrada não pode superar o preço do imóvel.';
      number('months', 1, 600, 'o prazo em meses', true);
      number('annualRate', 0, 100, 'a taxa anual efetiva');
      number('financeFees', 0, 1e7, 'os seguros e as tarifas mensais');
      if (!['price', 'sac'].includes(v.system)) errors.system = 'Escolha Price ou SAC.';
    }
    number('acquisitionRate', 0, 100, 'os custos de aquisição em %');
    number('upfront', 0, 1e9, 'os extras iniciais');
    ['condo', 'tax', 'maintenance', 'otherCosts'].forEach(k => number(k, 0, 1e7, 'o custo mensal'));
    if (v.goal === 'moradia') {
      number('rent', 0, 1e7, 'o aluguel alternativo');
      number('tenantCosts', 0, 1e7, 'os encargos mensais do inquilino');
      number('years', 1, 40, 'o horizonte em anos', true);
      number('appreciation', -30, 30, 'a valorização anual');
      number('investmentReturn', -30, 30, 'o retorno líquido anual');
      number('annualAdjustment', -20, 30, 'o reajuste anual dos custos e do aluguel');
      number('saleRate', 0, 100, 'os custos de venda em %');
    } else {
      number('variableRate', 0, 100, 'as despesas variáveis em % da receita');
      if (v.goal === 'temporada') {
        number('dailyRate', 0, 1e7, 'a diária média');
        number('nights', 0, 365, 'as noites ocupadas por ano', true);
      } else {
        number('annualRent', 0, 1e7, 'o aluguel mensal');
        number('vacancy', 0, 100, 'a vacância anual em %');
      }
    }
    return errors;
  }
  function compareHousing(v, debtSchedule, appreciation = v.appreciation) {
    let buyerInvestments = 0;
    let renterInvestments = v.entryUsed + v.acquisition + v.upfront;
    const gain = monthlyRate(v.investmentReturn);
    const adjustment = monthlyRate(v.annualAdjustment);
    const ownerCosts = v.condo + v.tax + v.maintenance + v.otherCosts;
    const months = v.years * 12;
    for (let month = 0; month < months; month++) {
      const factor = Math.pow(1 + adjustment, month);
      const loan = debtSchedule[month];
      const buyerCost = ownerCosts * factor + (loan ? loan.payment + v.financeFeesUsed : 0);
      const renterCost = (v.rent + v.tenantCosts) * factor;
      const budget = Math.max(buyerCost, renterCost);
      buyerInvestments = buyerInvestments * (1 + gain) + budget - buyerCost;
      renterInvestments = renterInvestments * (1 + gain) + budget - renterCost;
    }
    const residualDebt = debtSchedule[Math.min(months, debtSchedule.length) - 1]?.balance || 0;
    const propertyValue = v.price * Math.pow(1 + appreciation / 100, v.years);
    const saleCosts = propertyValue * v.saleRate / 100;
    const buyerBeforeSale = propertyValue - residualDebt + buyerInvestments;
    const buyerAfterSale = buyerBeforeSale - saleCosts;
    return { buyerBeforeSale, buyerAfterSale, renterInvestments, buyerInvestments, residualDebt, propertyValue, saleCosts, difference: buyerAfterSale - renterInvestments };
  }
  function calculate(input) {
    const errors = validate(input);
    if (Object.keys(errors).length) return { valid: false, errors };
    const v = { ...input };
    v.entryUsed = v.purchase === 'avista' ? v.price : v.entry;
    v.financeFeesUsed = v.purchase === 'avista' ? 0 : v.financeFees;
    v.acquisition = v.price * v.acquisitionRate / 100;
    const principal = v.price - v.entryUsed;
    const debtSchedule = schedule(principal, v.months, v.annualRate, v.system);
    const firstPayment = debtSchedule[0]?.payment || 0;
    const lastPayment = debtSchedule.at(-1)?.payment || 0;
    const fixedCosts = v.condo + v.tax + v.maintenance + v.otherCosts;
    const upfront = v.entryUsed + v.acquisition + v.upfront;
    const reference = references[v.city] || null;
    const result = {
      valid: true, errors: {}, principal, firstPayment, lastPayment, fixedCosts, upfront,
      acquisition: v.acquisition, pricePerM2: v.price / v.area, reference,
      m2Deviation: reference ? (v.price / v.area / reference - 1) * 100 : null,
      totalInterest: debtSchedule.reduce((sum, m) => sum + m.interest, 0),
      ownerFirstMonth: fixedCosts + firstPayment + (principal > 0 ? v.financeFeesUsed : 0),
      entryPercent: v.entryUsed / v.price * 100, debtSchedule
    };
    if (v.goal === 'moradia') {
      result.renterFirstMonth = v.rent + v.tenantCosts;
      result.housing = compareHousing(v, debtSchedule);
      result.sensitivity = [-2, 0, 2].map(delta => ({ appreciation: v.appreciation + delta, ...compareHousing(v, debtSchedule, v.appreciation + delta) }));
    } else {
      const gross = v.goal === 'temporada' ? v.dailyRate * v.nights : v.annualRent * 12 * (1 - v.vacancy / 100);
      const variableCosts = gross * v.variableRate / 100;
      const operatingNet = gross - variableCosts - fixedCosts * 12;
      const firstYearDebt = debtSchedule.slice(0, 12).reduce((sum, m) => sum + m.payment + v.financeFeesUsed, 0);
      result.rental = {
        gross, variableCosts, operatingNet, firstYearDebt, cashflow: operatingNet - firstYearDebt,
        grossYield: gross / v.price * 100, operatingYield: operatingNet / v.price * 100,
        yieldOnTotalCost: operatingNet / (v.price + v.acquisition + v.upfront) * 100,
        breakEvenNights: v.goal === 'temporada' && v.dailyRate > 0 && v.variableRate < 100 ? Math.ceil((fixedCosts * 12 + firstYearDebt) / (v.dailyRate * (1 - v.variableRate / 100))) : null
      };
    }
    return result;
  }
  return Object.freeze({ calculate, validate, schedule, monthlyRate, references });
}));
