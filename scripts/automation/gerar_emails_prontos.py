import csv, os
from datetime import datetime

base = r'C:\Users\Carolina\praia-digital'
csv_path = os.path.join(base, 'csv-lotes-email', 'checklist-envio-hoje-limpo.csv')
out_path = os.path.join(base, 'outreach', 'emails-prontos-para-enviar.html')

rows = []
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>E-mails Prontos para Enviar — Brevo</title>
  <style>
    body { font-family: 'Segoe UI', system-ui, sans-serif; background: #f4f7fb; color: #1a2332; padding: 2rem; }
    .box { max-width: 900px; margin: 0 auto; }
    .header { background: linear-gradient(135deg,#00d4ff,#00ff88); padding: 2rem; border-radius: 20px; margin-bottom: 2rem; color: #0a0f1f; }
    .email-block { background: #fff; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); margin: 1.5rem 0; }
    .email-block h3 { margin: 0 0 0.5rem; font-size: 1.2rem; color: #0a0f1f; }
    .email-meta { color: #666; font-size: 0.85rem; margin-bottom: 1rem; }
    .subject { font-weight: 700; color: #0077b6; margin-bottom: 0.75rem; }
    .body { background: #f8fafc; padding: 1.5rem; border-radius: 12px; font-size: 0.95rem; line-height: 1.7; color: #2d3748; white-space: pre-wrap; }
    .copy-btn { background: #0a0f1f; color: #fff; border: none; padding: 0.5rem 1rem; border-radius: 8px; cursor: pointer; font-size: 0.85rem; margin-top: 0.75rem; }
  </style>
</head>
<body>
  <div class="box">
    <div class="header">
      <h1>📧 E-mails Prontos para Enviar</h1>
      <p>Copie o assunto e o corpo de cada bloco e cole no Brevo.</p>
      <p><strong>Total:</strong> """ + str(len(rows)) + """ leads</p>
    </div>
"""

for i, row in enumerate(rows, 1):
    html += f"""
    <div class="email-block">
      <h3>E-mail {i} — {row['Empresa']}</h3>
      <div class="email-meta">Para: {row['Email']} | {row['Cidade']}</div>
      <div class="subject">Assunto: {row['Assunto']}</div>
      <div class="body">{row['Mensagem']}</div>
      <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('email{i}').innerText); this.innerText='Copiado!'">Copiar</button>
      <div id="email{i}" style="display:none;">{row['Mensagem']}</div>
    </div>
"""

html += """
  </div>
</body>
</html>"""

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Arquivo criado:', out_path)
print('E-mails prontos:', len(rows))
