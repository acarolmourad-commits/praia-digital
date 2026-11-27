(() => {
  'use strict';
  const form = document.getElementById('turnover-form');
  if (!form) return;
  const inputs = [...form.querySelectorAll('input')];
  const submit = form.querySelector('[type="submit"]');
  const example = document.getElementById('turnover-example');
  const error = document.getElementById('turnover-error');
  const result = document.getElementById('turnover-result');

  function time(value) {
    if (!/^(?:[01]\d|2[0-3]):[0-5]\d$/.test(value)) return NaN;
    const [hours, minutes] = value.split(':').map(Number);
    return hours * 60 + minutes;
  }
  function clock(minute) {
    return [Math.floor(minute / 60), minute % 60].map(part => String(part).padStart(2, '0')).join(':');
  }
  function duration(minute) {
    const hours = Math.floor(minute / 60);
    const rest = minute % 60;
    return hours && rest ? `${hours} h ${rest} min` : hours ? `${hours} h` : `${rest} min`;
  }
  function clear() {
    error.textContent = '';
    result.hidden = true;
    result.textContent = '';
    inputs.forEach(input => input.removeAttribute('aria-invalid'));
  }
  function fail(input, message) {
    input.setAttribute('aria-invalid', 'true');
    error.textContent = message;
    input.focus();
  }

  form.addEventListener('input', clear);
  submit.disabled = false;
  example.disabled = false;
  example.addEventListener('click', () => {
    clear();
    ['11:00', '15:00', '120', '30', '30'].forEach((value, index) => { inputs[index].value = value; });
    submit.focus();
  });
  form.addEventListener('submit', event => {
    event.preventDefault();
    clear();
    const [out, arrival, clean, inspect, buffer] = inputs;
    const start = time(out.value);
    const end = time(arrival.value);
    if (!Number.isFinite(start)) return fail(out, 'Informe um horário válido de check-out.');
    if (!Number.isFinite(end) || end <= start) return fail(arrival, 'Informe um check-in depois do check-out, no mesmo dia.');
    for (const input of [clean, inspect, buffer]) {
      const number = input.valueAsNumber;
      const minimum = Number(input.min);
      if (!Number.isInteger(number) || number < minimum || number > 1440) {
        const label = input.labels[0].textContent.trim().replace(' (min)', '');
        return fail(input, `${label}: informe um número inteiro de ${minimum} a 1440 minutos.`);
      }
    }
    const windowMinutes = end - start;
    const needed = clean.valueAsNumber + inspect.valueAsNumber + buffer.valueAsNumber;
    const slack = windowMinutes - needed;
    const summary = document.createElement('p');
    const detail = document.createElement('p');
    summary.textContent = slack > 0 ? `Sobram ${duration(slack)} além da margem informada.` :
      slack === 0 ? 'Cabe no intervalo, sem folga extra além da margem informada.' :
      `Faltam ${duration(-slack)} para caber no intervalo com a margem informada.`;
    detail.textContent = `Janela: ${duration(windowMinutes)}. Tempo necessário: ${duration(needed)}. ` +
      (slack >= 0 ? `Último horário estimado para começar e manter a margem: ${clock(end - needed)}.` :
        'Nesta janela, não cabe manter o plano. Combine outro horário ou revise o tempo necessário com a equipe.');
    result.hidden = false;
    result.append(summary, detail);
    result.focus();
  });
})();
