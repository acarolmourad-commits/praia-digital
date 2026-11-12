(function () {
  "use strict";
  const $ = (id) => document.getElementById(id),
    form = $("calculator"),
    ids = ["area", "referencia", "ajuste", "variacao"],
    money = (v) =>
      v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
  let snapshot = null,
    custom = false,
    inFlight = false,
    sent = false;
  function invalidate() {
    snapshot = null;
    $("resultado").hidden = true;
    sent = false;
    if (!inFlight) $("enviar-simulacao").disabled = false;
    $("contact-status").textContent = "";
    for (const id of ids) {
      $(id).removeAttribute("aria-invalid");
      $(id + "-error").textContent = "";
    }
    $("status").textContent = "Premissas alteradas. Calcule novamente.";
  }
  function source() {
    const ref = window.PDInvestir.references[$("cidade").value];
    $("source-note").textContent = custom
      ? "Referência personalizada: confira e registre a fonte."
      : ref
        ? "Referência inicial: FipeZAP, outubro/2026, preço médio anunciado na cidade. Você pode substituir."
        : "Sem referência municipal verificada nesta ferramenta. Informe seu valor por m² e a fonte.";
  }
  $("cidade").addEventListener("change", () => {
    $("referencia").value =
      window.PDInvestir.references[$("cidade").value] || "";
    custom = false;
    source();
  });
  $("referencia").addEventListener("input", () => {
    custom = true;
    source();
  });
  form.addEventListener("input", invalidate);
  form.addEventListener("change", invalidate);
  source();
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    invalidate();
    const values = {};
    for (const id of ids)
      values[id] = $(id).value.trim() === "" ? NaN : Number($(id).value);
    const r = window.PDInvestir.valuation(values);
    if (!r.valid) {
      for (const [id, message] of Object.entries(r.errors)) {
        $(id).setAttribute("aria-invalid", "true");
        $(id + "-error").textContent = message;
      }
      $("status").textContent = "Revise os campos indicados.";
      $(Object.keys(r.errors)[0]).focus();
      return;
    }
    snapshot = {
      cidade: $("cidade").value,
      ...values,
      fonte: custom
        ? $("origem").value.trim() ||
          "Referência personalizada sem fonte informada"
        : "FipeZAP, outubro/2026",
      observacao: $("origem").value.trim(),
      central: r.central,
      inferior: r.low,
      superior: r.high,
    };
    $("central").textContent = "Cenário central: " + money(r.central);
    $("range").textContent =
      `Sensibilidade de ±${values.variacao}%: ${money(r.low)} a ${money(r.high)}.`;
    $("basis").textContent =
      `${snapshot.cidade} · ${values.area} m² × ${money(values.referencia)}/m² · ajuste ${values.ajuste}%. Fonte: ${snapshot.fonte}.`;
    $("resultado").hidden = false;
    $("status").textContent =
      "Cenário calculado, sem avaliação individual ou garantia de negociação.";
    $("result-title").focus();
  });
  $("download").addEventListener("click", () => {
    if (!snapshot) return;
    const content =
      "Praia Digital — cenário preliminar de preço\n" +
      new Date().toLocaleDateString("pt-BR") +
      "\n" +
      Object.entries(snapshot)
        .map(([k, v]) => k + ": " + v)
        .join("\n") +
      "\nNão é laudo, preço de fechamento nem faixa de confiança.\nhttps://praia.digital/ferramentas/avaliacao-preco.html";
    const url = URL.createObjectURL(
      new Blob([content], { type: "text/plain;charset=utf-8" }),
    );
    const a = document.createElement("a");
    a.href = url;
    a.download = "cenario-preco-imovel.txt";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  $("contact").addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!snapshot || inFlight || sent) return;
    const email = $("lead-email");
    if (!email.validity.valid) {
      $("contact-status").textContent = "Informe um e-mail válido.";
      email.focus();
      return;
    }
    const current = snapshot;
    inFlight = true;
    $("enviar-simulacao").disabled = true;
    $("contact-status").textContent = "Enviando solicitação…";
    const controller = new AbortController(),
      timeout = setTimeout(() => controller.abort(), 15000);
    try {
      const response = await fetch(
        "https://formsubmit.co/ajax/comercial@praia.digital",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          signal: controller.signal,
          body: JSON.stringify({
            _subject: "Solicitação de contato — cenário de preço",
            nome: $("lead-nome").value.trim(),
            email: email.value.trim(),
            ...current,
          }),
        },
      );
      const data = await response.json();
      if (!response.ok || !(data.success === true || data.success === "true"))
        throw new Error("unconfirmed");
      if (snapshot === current) {
        sent = true;
        $("contact-status").textContent =
          "O serviço confirmou o recebimento da solicitação. Isso não confirma entrega de e-mail nem prazo de resposta da equipe.";
      }
    } catch (error) {
      if (snapshot === current)
        $("contact-status").textContent =
          "Não foi possível confirmar o recebimento. O envio pode ter ocorrido; confira antes de tentar novamente ou use a página de contato. Seu resumo continua disponível para baixar.";
    } finally {
      clearTimeout(timeout);
      inFlight = false;
      $("enviar-simulacao").disabled = sent;
    }
  });
})();
