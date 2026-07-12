import csv
from pathlib import Path

REPO = Path(r'C:/Users/Carolina/praia-digital')
OUT = REPO / 'outreach'
rows = []
with open(REPO / 'docs/sales/leads-litoral-enriquecido.csv', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        rows.append(row)

chosen = []
seen = set()
for row in rows:
    key = row.get('nome_da_imobiliaria') or row.get('email') or ''
    if key and key not in seen:
        chosen.append(row)
        seen.add(key)
    if len(chosen) >= 11:
        break
chosen = chosen[5:11]


def build_email(row):
    nome = row.get('nome_da_imobiliaria') or ''
    cidade = row.get('cidade') or ''
    contato = row.get('pessoa_de_contato') or ''
    status = (row.get('status') or '').lower()
    primeiro_nome = contato.split()[0] if contato else ''
    if 'parceria' in status or 'fechada' in status:
        return f"Olá {primeiro_nome},\n\nParceria confirmada! Avancemos com a priorização de leads e o onboarding rápido em {cidade}.\n\nAbraço,\nCarolina Mourad\nCEO · Praia Digital\n(11) 95434-6288\nhttps://praia.digital"
    if 'interessado' in status:
        return f"Olá {primeiro_nome},\n\nÓtimo sinal! Vamos agendar uma call de 15 minutos para apresentar um plano personalizado para {nome}.\n\nAbraço,\nCarolina Mourad\nCEO · Praia Digital\n(11) 95434-6288\nhttps://praia.digital"
    return f"Olá {primeiro_nome},\n\nA Praia Digital pode ajudar {nome} em {cidade} com captação inteligente e automação sem custo inicial.\n\nQuer um tour rápido pelas ferramentas gratuitas?\n\nAbraço,\nCarolina Mourad\nCEO · Praia Digital\n(11) 95434-6288\nhttps://praia.digital"


blocks = []
for i, lead in enumerate(chosen, 1):
    nome = lead.get('nome_da_imobiliaria') or ''
    cidade = lead.get('cidade') or ''
    contato = lead.get('pessoa_de_contato') or ''
    email = lead.get('email') or ''
    status = lead.get('status') or ''
    dor = lead.get('dor_principal') or ''
    template = build_email(lead)
    subject = f"Parceria Praia Digital x {nome} - {cidade}"
    mailto = "mailto:" + email + "?subject=" + subject.replace(" ", "%20") + "&body=" + template.replace(" ", "%20").replace("\n", "%0A")

    block = (
        '<div class="lead-card">'
        '<div class="lead-header">'
        f'<div><strong>{i}. {nome}</strong> - {cidade}</div>'
        f'<span class="badge {status.lower()}">{status}</span>'
        '</div>'
        f'<div class="lead-meta">Contato: {contato} - E-mail: {email} - Dor: {dor}</div>'
        f'<div class="template" id="t{i}">{template}</div>'
        '<div class="actions">'
        f'<a class="btn" href="{mailto}" target="_blank">Abrir e-mail</a>'
        f'<button class="copy" onclick="navigator.clipboard.writeText(document.getElementById(\'t{i}\').innerText);alert(\'Copiado\')">Copiar</button>'
        '</div>'
        '</div>'
    )
    blocks.append(block)

batch = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Lote 36 - Prospeccao Personalizada</title>
<style>
body{font-family:Arial,sans-serif;background:#0d1117;color:#e6edf3;padding:2rem;}
.container{max-width:1000px;margin:0 auto;}
.header{background:linear-gradient(135deg,#7b2ff7,#00d4ff);padding:2rem;border-radius:12px;margin-bottom:2rem;text-align:center;}
.header h1{margin:0 0 0.5rem;}
.lead-card{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;}
.lead-header{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;margin-bottom:0.5rem;align-items:center;}
.badge{padding:0.35rem 0.7rem;border-radius:999px;font-size:0.8rem;font-weight:700;text-transform:uppercase;background:rgba(0,212,255,0.15);color:#00d4ff;border:1px solid rgba(0,212,255,0.4);}
.badge.interessado{background:rgba(123,47,247,0.15);color:#d4a0ff;border-color:rgba(123,47,247,0.4);}
.badge.parceria_fechada{background:rgba(0,200,150,0.15);color:#00ffa3;border-color:rgba(0,200,150,0.4);}
.lead-meta{color:#8b949e;font-size:0.9rem;margin-bottom:1rem;}
.template{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:1rem;white-space:pre-wrap;font-size:0.95rem;line-height:1.6;margin-bottom:1rem;}
.actions{display:flex;gap:0.75rem;flex-wrap:wrap;}
.btn{background:linear-gradient(135deg,#00d4ff,#7b2ff7);color:#fff;border:none;padding:0.75rem 1.25rem;border-radius:8px;font-weight:700;cursor:pointer;text-decoration:none;}
.copy{background:#21262d;border:1px solid #30363d;color:#e6edf3;padding:0.75rem 1.25rem;border-radius:8px;cursor:pointer;}
.footer{text-align:center;color:#8b949e;margin-top:2rem;font-size:0.9rem;}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>Lote 36 - Prospeccao Personalizada</h1>
    <p>Pronto para envio manual via Outlook/Gmail</p>
  </div>
  """ + "\n".join(blocks) + """
  <div class="footer">
    <p>Praia Digital - Lote 36</p>
  </div>
</div>
</body>
</html>"""

path = OUT / 'lote-prospeccao-36-2026-07-12.html'
path.write_text(batch, encoding='utf-8')
print('Lote 36 criado:', path)
print('Leads:')
for c in chosen:
    print('-', c.get('nome_da_imobiliaria'), c.get('cidade'), c.get('status'))
