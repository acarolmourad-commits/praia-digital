(function () {
  'use strict';
  const form = document.getElementById('roi-form');
  const result = document.getElementById('result');
  const status = document.getElementById('roi-status');
  const fields = ['valor','adr','ocup','noites','custos','plataforma','iptu','cond','ir'];
  const money = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
  const number = new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 1 });
  let calculated = false;
  function clearErrors() {
    fields.forEach(id => {
      document.getElementById(id).removeAttribute('aria-invalid');
      document.getElementById(id + '-error').textContent = '';
    });
  }
  function invalidate() {
    result.hidden = true;
    clearErrors();
    status.textContent = calculated ? 'Premissas alteradas. Calcule novamente para atualizar o resultado.' : '';
  }
  form.addEventListener('input', invalidate);
  form.addEventListener('change', invalidate);
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    result.hidden = true;
    clearErrors();
    const values = {};
    fields.forEach(id => {
      const value = document.getElementById(id).value;
      values[id] = value.trim() === '' ? NaN : Number(value);
    });
    const data = window.PDRoiTemporada.calculate(values);
    if (!data.valid) {
      for (const [id, message] of Object.entries(data.errors)) {
        document.getElementById(id).setAttribute('aria-invalid', 'true');
        document.getElementById(id + '-error').textContent = message;
      }
      status.textContent = 'Revise os campos indicados. Nenhum resultado foi calculado.';
      document.getElementById(Object.keys(data.errors)[0]).focus();
      return;
    }
    const display = {
      rNoites: number.format(data.nights) + ' noites', rBruta: money.format(data.gross),
      rPlat: '− ' + money.format(data.platformFee), rCustos: '− ' + money.format(data.costs),
      rIR: '− ' + money.format(data.tax), rLiq: money.format(data.net),
      rRoiB: number.format(data.grossYield) + '% ao ano', rRoiL: number.format(data.netYield) + '% ao ano',
      rPayback: data.payback === null ? 'Não recuperado neste cenário' : number.format(data.payback) + ' anos'
    };
    Object.entries(display).forEach(([id, text]) => { document.getElementById(id).textContent = text; });
    document.getElementById('rBig').textContent = data.net > 0
      ? 'Saldo anual positivo nas premissas informadas.'
      : data.net < 0 ? 'As despesas superam a receita neste cenário.' : 'Receita e despesas se equilibram neste cenário.';
    document.getElementById('rCidade').textContent = document.getElementById('cidade').value || 'Sem cidade informada';
    result.hidden = false;
    calculated = true;
    status.textContent = 'Cálculo concluído. Resultado atualizado abaixo; as premissas são suas, não uma previsão de mercado.';
    document.getElementById('roi-result-title').focus();
  });
})();
