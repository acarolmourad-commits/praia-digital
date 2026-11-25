(() => {
  'use strict';
  const form = document.getElementById('form-ocupacao-periodo');
  const total = document.getElementById('periodo-total');
  const blocked = document.getElementById('periodo-bloqueadas');
  const booked = document.getElementById('periodo-reservadas');
  const result = document.getElementById('periodo-resultado');
  const percent = new Intl.NumberFormat('pt-BR', {style: 'percent', maximumFractionDigits: 1});
  document.getElementById('periodo-calcular').disabled = false;

  form.addEventListener('input', () => {
    blocked.setCustomValidity('');
    booked.setCustomValidity('');
    result.value = '';
  });

  form.addEventListener('submit', event => {
    event.preventDefault();
    const available = total.valueAsNumber - blocked.valueAsNumber;
    if (available < 0) {
      blocked.setCustomValidity('Os bloqueios não podem superar as noites do período.');
    } else if (booked.valueAsNumber > available) {
      booked.setCustomValidity('As reservas não podem superar as noites disponíveis para venda.');
    }
    if (!form.reportValidity()) return;
    if (available === 0) {
      result.value = 'Todas as noites estavam bloqueadas. A ocupação fica sem base de cálculo.';
      return;
    }
    result.value = 'Noites disponíveis para venda: ' + available +
      '. Noites reservadas: ' + booked.valueAsNumber +
      '. Ocupação do período: ' + percent.format(booked.valueAsNumber / available) + '.';
  });
})();
