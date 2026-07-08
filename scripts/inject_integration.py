
import os, re
api='http://127.0.0.1:8000'
files=['predicao-vendidos-litoral.html','servico-assistente-virtual-compradores-litoral.html','servico-aluguel-temporada-ia-litoral.html']
tpl_form = '<form id="integrated-form" autocomplete="off"><div class="form-row"><label>Cidade</label><input name="cidade" value="Santos"/></div><div class="form-row"><label>Objetivo</label><input name="objetivo" value="Investir"/></div><div class="form-row"><label>Perfil</label><input name="perfil" value="investidor"/></div><button class="btn" type="submit" id="b-run">Consultar IA</button></form>'
tpl_script = """
<div id="out-integrated" class="result" style="margin-top:1rem;">Resultado da IA aparecerá aqui.</div>
<script>
(function(){
  const API_BASE = '""" + api + """';
  function run(){
    const out = document.getElementById('out-integrated');
    if(out) out.textContent = 'Processando...';
    const payload = {};
    document.querySelectorAll('#integrated-form [name]').forEach(function(el){
      const n = el.getAttribute('name');
      payload[n] = isNaN(Number(el.value)) ? el.value : Number(el.value);
    });
    fetch(API_BASE + '/roteiro', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    })
    .then(function(res){ return res.json(); })
    .then(function(data){
      if(out) out.textContent = JSON.stringify(data, null, 2);
    })
    .catch(function(err){
      if(out) out.textContent = 'Erro: ' + err.message;
    });
  }
  var form = document.getElementById('integrated-form');
  if(form){ form.addEventListener('submit', function(e){ e.preventDefault(); run(); }); }
  var btn = document.getElementById('b-run');
  if(btn){ btn.addEventListener('click', run); }
})();
</script>
"""
for fname in files:
    p = os.path.join('.', fname)
    if not os.path.exists(p):
        continue
    html = open(p, 'r', encoding='utf-8').read()
    if 'fetch(' in html or 'integrated-form' in html:
        continue
    if '</body>' in html.lower():
        idx = re.search(re.escape('</body>'), html, re.IGNORECASE).start()
        html = html[:idx] + tpl_form + tpl_script + html[idx:]
        open(p, 'w', encoding='utf-8').write(html)
        print('updated', fname)
    else:
        print('skip', fname)
