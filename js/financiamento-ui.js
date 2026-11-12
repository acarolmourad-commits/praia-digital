(function () {
  "use strict";
  const form = document.getElementById("calculator"),
    result = document.getElementById("resultado"),
    status = document.getElementById("status"),
    ids = ["valor", "entrada", "taxa", "meses", "seguros", "comprometimento"];
  const money = (v) =>
    v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
  function clear() {
    result.hidden = true;
    for (const id of ids) {
      document.getElementById(id).removeAttribute("aria-invalid");
      document.getElementById(id + "-error").textContent = "";
    }
  }
  form.addEventListener("input", () => {
    clear();
    status.textContent = "Premissas alteradas. Calcule novamente.";
  });
  form.addEventListener("change", () => {
    clear();
    status.textContent = "Premissas alteradas. Calcule novamente.";
  });
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    clear();
    const values = { tipo: document.getElementById("tipo").value };
    for (const id of ids) {
      const raw = document.getElementById(id).value;
      values[id] = raw.trim() === "" ? NaN : Number(raw);
    }
    const r = window.PDInvestir.finance(values);
    if (!r.valid) {
      for (const [id, message] of Object.entries(r.errors)) {
        document.getElementById(id).setAttribute("aria-invalid", "true");
        const span = document.getElementById(id + "-error");
        if (span) span.textContent = message;
      }
      status.textContent = "Revise os campos indicados.";
      document.getElementById(Object.keys(r.errors)[0]).focus();
      return;
    }
    document.getElementById("summary").textContent =
      r.principal === 0
        ? "Compra à vista: não há parcelas, juros ou encargos de financiamento."
        : `Saldo financiado: ${money(r.principal)}. Taxa mensal: ${(r.rate * 100).toLocaleString("pt-BR", { maximumFractionDigits: 6 })}%. Sem correção do saldo.`;
    const rows = document.getElementById("rows");
    rows.replaceChildren();
    for (const [label, key] of [
      ["Primeira parcela com encargos", "first"],
      ["Última parcela com encargos", "last"],
      ["Juros totais", "interest"],
      ["Seguros e tarifas informados", "fees"],
      ["Total das parcelas, sem entrada", "total"],
      ["Renda mensal indicativa", "income"],
    ]) {
      const tr = document.createElement("tr");
      for (const value of [label, money(r.sac[key]), money(r.price[key])]) {
        const td = document.createElement("td");
        td.textContent = value;
        tr.append(td);
      }
      rows.append(tr);
    }
    result.hidden = false;
    status.textContent =
      "Cálculo atualizado. Estimativa, não proposta de crédito.";
    document.getElementById("result-title").focus();
  });
})();
