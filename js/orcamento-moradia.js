(() => {
  "use strict";
  const form = document.getElementById("orcamento");
  const result = document.getElementById("result");
  const money = new Intl.NumberFormat("pt-BR", {style: "currency", currency: "BRL"});
  const nextStep = {
    sbpe: "Compare as parcelas SAC e Price com as condições da proposta.",
    fgts: "Inclua na entrada apenas o saldo autorizado para a sua operação.",
    mcmv: "Confirme o enquadramento da família e do imóvel antes de contar com um subsídio.",
    consorcio: "Confira a carta de crédito, a taxa de administração e as condições do lance."
  };
  form.addEventListener("input", () => {
    form.elements.entrada.setCustomValidity("");
    result.textContent = "";
  });
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const {preco, entrada, renda, percentual, tipo} = form.elements;
    if (entrada.valueAsNumber > preco.valueAsNumber) {
      entrada.setCustomValidity("A entrada deve ser menor ou igual ao valor do imóvel.");
      entrada.reportValidity();
      return;
    }
    const restante = preco.valueAsNumber - entrada.valueAsNumber;
    const reserva = renda.valueAsNumber * (percentual.valueAsNumber / 100);
    result.textContent = `Valor a cobrir após a entrada: ${money.format(restante)}. Reserva mensal escolhida: ${money.format(reserva)}. ${nextStep[tipo.value]}`;
  });
  form.querySelector('button[type="submit"]').disabled = false;
})();
