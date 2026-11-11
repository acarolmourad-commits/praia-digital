/* Educational annual scenario. No market presets or statutory tax calculation. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.PDRoiTemporada = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const rules = {
    valor: { label: 'Valor do imóvel', min: 0, exclusive: true },
    adr: { label: 'Diária média', min: 0 },
    ocup: { label: 'Ocupação', min: 0, max: 100 },
    noites: { label: 'Noites disponíveis', min: 0, max: 365, integer: true },
    custos: { label: 'Custos operacionais', min: 0 },
    plataforma: { label: 'Taxa da plataforma', min: 0, max: 100 },
    iptu: { label: 'IPTU anual', min: 0 },
    cond: { label: 'Condomínio anual', min: 0 },
    ir: { label: 'Provisão tributária simulada', min: 0, max: 100 }
  };
  function calculate(input) {
    const errors = {};
    for (const [key, rule] of Object.entries(rules)) {
      const value = input[key];
      if (typeof value !== 'number' || !Number.isFinite(value)) errors[key] = `${rule.label}: informe um número válido.`;
      else if (value < rule.min || (rule.exclusive && value === rule.min)) errors[key] = `${rule.label}: informe um valor ${rule.exclusive ? 'maior que' : 'igual ou maior que'} ${rule.min}.`;
      else if (rule.max !== undefined && value > rule.max) errors[key] = `${rule.label}: o máximo é ${rule.max}${key === 'noites' ? ' noites' : '%'}.`;
      else if (rule.integer && !Number.isInteger(value)) errors[key] = `${rule.label}: informe um número inteiro.`;
    }
    if (Object.keys(errors).length) return { valid: false, errors };
    const nights = input.noites * input.ocup / 100;
    const gross = input.adr * nights;
    const platformFee = gross * (input.plataforma / 100);
    const costs = input.custos + input.iptu + input.cond;
    const beforeTax = gross - platformFee - costs;
    const tax = Math.max(0, beforeTax) * (input.ir / 100);
    const net = beforeTax - tax;
    const grossYield = gross / input.valor * 100;
    const netYield = net / input.valor * 100;
    const payback = net > 0 ? input.valor / net : null;
    const result = { nights, gross, platformFee, costs, beforeTax, tax, net, grossYield, netYield, payback };
    if (Object.values(result).some(v => v !== null && !Number.isFinite(v))) {
      return { valid: false, errors: { valor: 'Os valores excedem a capacidade de cálculo. Revise as premissas.' } };
    }
    return { valid: true, ...result };
  }
  return { calculate };
});
