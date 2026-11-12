/* Educational models. No market forecast, tax computation or credit approval. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.PDInvestir = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  function validate(v, rules) {
    const errors = {};
    for (const [key, [min, max, integer]] of Object.entries(rules)) {
      if (
        typeof v[key] !== "number" ||
        !Number.isFinite(v[key]) ||
        v[key] < min ||
        v[key] > max ||
        (integer && !Number.isInteger(v[key]))
      )
        errors[key] =
          `Informe ${integer ? "um inteiro" : "um número"} entre ${min} e ${max}.`;
    }
    return errors;
  }
  function finance(v) {
    const errors = validate(v, {
      valor: [1, 1e8],
      entrada: [0, 1e8],
      taxa: [0, 100],
      meses: [1, 600, true],
      seguros: [0, 1e6],
      comprometimento: [1, 100],
    });
    if (v.entrada > v.valor)
      errors.entrada = "A entrada não pode superar o preço do imóvel.";
    if (!["nominal", "effective"].includes(v.tipo))
      errors.tipo = "Escolha o tipo de taxa.";
    if (Object.keys(errors).length) return { valid: false, errors };
    const principal = v.valor - v.entrada,
      rate =
        v.tipo === "nominal"
          ? v.taxa / 1200
          : Math.expm1(Math.log1p(v.taxa / 100) / 12),
      fees = principal > 0 ? v.seguros : 0;
    const pmt =
      rate === 0
        ? principal / v.meses
        : (principal * rate) / -Math.expm1(-v.meses * Math.log1p(rate));
    const amort = principal / v.meses;
    const sacInterest = (rate * principal * (v.meses + 1)) / 2;
    const priceInterest = pmt * v.meses - principal;
    const item = (first, last, interest) => ({
      first: first + fees,
      last: last + fees,
      interest,
      fees: fees * v.meses,
      total: principal + interest + fees * v.meses,
      income: (first + fees) / (v.comprometimento / 100),
    });
    return {
      valid: true,
      principal,
      rate,
      sac: item(amort + principal * rate, amort * (1 + rate), sacInterest),
      price: item(pmt, pmt, Math.max(0, priceInterest)),
    };
  }
  function valuation(v) {
    const errors = validate(v, {
      area: [0.01, 1e5],
      referencia: [0.01, 1e6],
      ajuste: [-90, 200],
      variacao: [0, 100],
    });
    if (Object.keys(errors).length) return { valid: false, errors };
    const base = v.area * v.referencia,
      central = base * (1 + v.ajuste / 100);
    return {
      valid: true,
      base,
      central,
      low: central * (1 - v.variacao / 100),
      high: central * (1 + v.variacao / 100),
    };
  }
  return {
    finance,
    valuation,
    references: Object.freeze({
      Santos: 8678,
      Guarujá: 6944,
      "Praia Grande": 6800,
    }),
  };
});
