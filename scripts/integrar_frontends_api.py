
import os, re

assets_dir = 'C:/Users/Carolina/praia-digital/assets'
api_base = 'http://localhost:8000'

integrations = {
    'servico-avaliacao-preco-imoveis-litoral.html': {
        'endpoint': '/avaliar',
        'btn': 'Avaliar preço',
        'fields': [
            ('cidade', 'select', 'Santos', ['Santos','Guarujá','Praia Grande','São Vicente','Bertioga','Itanhaém','Peruíbe','Mongaguá']),
            ('tipo', 'select', 'Apartamento', ['Apartamento','Casa','Cobertura','Flat']),
            ('area', 'number', '70'),
            ('quartos', 'number', '2'),
        ],
        'keys': ['cidade','tipo','area','quartos']
    },
    'servico-geracao-descricoes-anuncios-ia.html': {
        'endpoint': '/descrever',
        'btn': 'Gerar descrição',
        'fields': [
            ('tipo', 'select', 'Apartamento', ['Apartamento','Casa','Cobertura','Flat']),
            ('cidade', 'select', 'Santos', ['Santos','Guarujá','Praia Grande','São Vicente','Bertioga','Itanhaém','Peruíbe','Mongaguá']),
            ('diferenciais', 'text', 'frente mar, varanda'),
        ],
        'keys': ['tipo','cidade','diferenciais']
    },
    'priorizacao-leads-ia.html': {
        'endpoint': '/priorizar',
        'btn': 'Priorizar lead',
        'fields': [
            ('origem', 'select', 'WhatsApp', ['Indicação','WhatsApp','Google Maps','Site','Instagram']),
            ('tempo_resposta', 'number', '15'),
            ('interacoes', 'number', '3'),
        ],
        'keys': ['origem','tempo_resposta','interacoes']
    },
}

updated = 0
for fname, cfg in integrations.items():
    fpath = os.path.join(assets_dir, fname)
    if not os.path.exists(fpath):
        continue
    html = open(fpath, 'r', encoding='utf-8').read()
    if 'fetch(' in html or 'integrated-form' in html:
        continue

    out_id = 'out-' + fname.replace('.html', '')
    form_html = '<form id="integrated-form" autocomplete="off">\n'
    for field in cfg['fields']:
        key = field[0]
        kind = field[1]
        default = field[2]
        options = field[3] if len(field) > 3 else []
        if kind == 'select':
            opts = ''.join("            <option value=\"" + o + "\">" + o + "</option>\n" for o in options)
            control = "            <select name=\"" + key + "\" id=\"field-" + key + "\">\n              <option value=\"" + default + "\">" + default + "</option>\n" + opts + "            </select>"
        else:
            control = "            <input type=\"" + kind + "\" name=\"" + key + "\" id=\"field-" + key + "\" value=\"" + default + "\"/>"
        form_html += "  <div class=\"form-row\"><label>" + key.replace("_", " ").title() + "</label>\n" + control + "\n  </div>\n"
    submit_btn = "  <button class=\"btn\" type=\"submit\" id=\"btn-run\">" + cfg['btn'] + "</button>\n"
    form_html += submit_btn + "</form>\n"

    result_html = '<div id="' + out_id + '" class=\"result\" style=\"margin-top:1rem;\">Resultado da IA aparecerá aqui após o envio.</div>\n'

    script = (
        "<script>\n"
        "(function(){\n"
        "  const API_BASE = '" + api_base + "';\n"
        "  const ENDPOINT = '" + cfg['endpoint'] + "';\n"
        "  const OUTPUT_ID = '" + out_id + "';\n"
        "  const FIELDS = [" + ','.join('"' + k + '"' for k in cfg['keys']) + "];\n"
        "  function run(){\n"
        "    const out = document.getElementById(OUTPUT_ID);\n"
        "    if(out) out.textContent = 'Processando...';\n"
        "    const payload = {};\n"
        "    FIELDS.forEach(function(k){\n"
        "      var el = document.getElementById('field-' + k) || document.querySelector('[name=\"' + k + '\"]');\n"
        "      if(el){ payload[k] = isNaN(Number(el.value)) ? el.value : Number(el.value); }\n"
        "    });\n"
        "    fetch(API_BASE + ENDPOINT, {\n"
        "      method: 'POST',\n"
        "      headers: {'Content-Type': 'application/json'},\n"
        "      body: JSON.stringify(payload)\n"
        "    })\n"
        "    .then(function(res){ return res.json(); })\n"
        "    .then(function(data){\n"
        "      if(out) out.textContent = JSON.stringify(data, null, 2);\n"
        "    })\n"
        "    .catch(function(err){\n"
        "      if(out) out.textContent = 'Erro: ' + err.message;\n"
        "    });\n"
        "  }\n"
        "  var form = document.getElementById('integrated-form');\n"
        "  if(form){ form.addEventListener('submit', function(e){ e.preventDefault(); run(); }); }\n"
        "  var btn = document.getElementById('btn-run');\n"
        "  if(btn){ btn.addEventListener('click', run); }\n"
        "})();\n"
        "</script>\n"
    )

    if '</body>' in html.lower():
        idx = re.search(re.escape('</body>'), html, re.IGNORECASE).start()
        html = html[:idx] + form_html + result_html + script + html[idx:]
    else:
        html += form_html + result_html + script

    open(fpath, 'w', encoding='utf-8').write(html)
    updated += 1

print('updated:' + str(updated))
