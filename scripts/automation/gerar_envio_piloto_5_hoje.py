import csv, os
from pathlib import Path

REPO = Path(r'C:/Users/Carolina/praia-digital')
OUT = REPO / 'outreach' / 'envio-piloto-5-hoje'
OUT.mkdir(parents=True, exist_ok=True)

rows = []
with open(REPO / 'docs/sales/leads-litoral-enriquecido.csv', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        rows.append(row)

# pick 5 distinct leads
chosen = []
seen = set()
for row in rows:
    key = row.get('nome_da_imobiliaria') or row.get('email')
    if key and key not in seen:
        chosen.append(row)
        seen.add(key)
    if len(chosen) == 5:
        break

print('Leads escolhidos:')
for c in chosen:
    print('-', c['nome_da_imobiliaria'], c['cidade'], c['pessoa_de_contato'], c['email'])

# email templates by scenario
templates = {
    'interessado': """Olá, {contato},

Trabalhamos com imobiliárias do litoral paulista que querem captar mais leads e reduzir trabalho repetitivo.

A Praia Digital tem 4 ferramentas gratuitas utilizadas por +50 parceiros: avaliação automática de preço, recomendação inteligente, assistente virtual 24/7 e geração automática de descrições.

Queremos oferecer um plano personalizado para a {empresa}, começando por um diagnóstico gratuito. Posso enviar mais detalhes ou agendar uma call de 15 minutos?

Abraço,
Carolina Mourad
CEO · Praia Digital
(11) 95434-6288
https://praia.digital""",
    'parceria_fechada': """Olá, {contato},

Agradeço a parceria até aqui. A próxima etapa é ampliar resultados em {cidade}: já identificamos imobiliárias similares com crescimento em 30 dias após implementar recomendação automática e atendimento inteligente.

Quer que eu avance com a priorização de leads e um script de onboarding rápido para a {empresa}?

Abraço,
Carolina Mourad
CEO · Praia Digital
(11) 95434-6288
https://praia.digital""",
    'default': """Olá, {contato},

A Praia Digital tem um programa focado em imobiliárias do litoral paulista: ferramentas gratuitas de IA + parcerias sem investimento inicial.

Gostaria de apresentar um case rápido para a {empresa} em {cidade} e propor um próximo passo leve: diagnóstico ou call de 15 minutos.

Abraço,
Carolina Mourad
CEO · Praia Digital
(11) 95434-6288
https://praia.digital"""
}

os.makedirs(OUT, exist_ok=True)
created = []
for i, lead in enumerate(chosen, 1):
    nome = lead.get('nome_da_imobiliaria') or ''
    cidade = lead.get('cidade') or ''
    contato = lead.get('pessoa_de_contato') or ''
    email = lead.get('email') or ''
    status = lead.get('status') or ''
    dor = lead.get('dor_principal') or ''

    template = templates.get(status, templates['default']).format(
        contato=contato.split()[0] if contato else '',
        empresa=nome,
        cidade=cidade,
        dor=dor
    )

    subject = f"Parceria Praia Digital × {nome} · {cidade}"
    mailto = f"mailto:{email}?subject={subject.replace(' ', '%20')}&body={template.replace(' ', '%20').replace(chr(10), '%0A')}"

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Envio Piloto {i}/5 — {nome}</title>
<style>
body {{ font-family:Arial,sans-serif; background:#0d1117; color:#e6edf3; padding:2rem; }}
.card {{ max-width:900px; margin:0 auto; background:#161b22; border:1px solid #30363d; border-radius:12px; padding:2rem; }}
h1 {{ font-size:1.4rem; margin-bottom:1rem; }}
.meta {{ color:#8b949e; font-size:0.9rem; margin-bottom:1rem; }}
.template {{ background:#0d1117; border:1px solid #30363d; border-radius:8px; padding:1rem; white-space:pre-wrap; font-size:0.95rem; line-height:1.6; }}
.actions {{ display:flex; gap:0.75rem; margin-top:1.25rem; flex-wrap:wrap; }}
.btn {{ background:linear-gradient(135deg,#00d4ff,#7b2ff7); color:#fff; border:none; padding:0.75rem 1.25rem; border-radius:8px; font-weight:700; cursor:pointer; text-decoration:none; }}
.btn:hover {{ transform:translateY(-2px); }}
.copy {{ background:#21262d; border:1px solid #30363d; color:#e6edf3; padding:0.75rem 1.25rem; border-radius:8px; cursor:pointer; }}
.copy:hover {{ background:#30363d; }}
</style>
</head>
<body>
<div class="card">
  <h1>📤 Envio Piloto {i}/5 — {nome}</h1>
  <div class="meta">Cidade: {cidade} • Contato: {contato} • Status: {status}</div>
  <div class="template" id="template">{template}</div>
  <div class="actions">
    <a class="btn" href="{mailto}" target="_blank">📧 Abrir no cliente de e-mail</a>
    <button class="copy" onclick="navigator.clipboard.writeText(document.getElementById('template').innerText);alert('Copiado')">📋 Copiar texto</button>
  </div>
</div>
</body>
</html>"""
    path = OUT / f'envio-piloto-{i}-{nome.lower().replace(" ","-").replace("/","-")}.html'
    path.write_text(html, encoding='utf-8')
    created.append(str(path))

print(f'\n✅ Criados {len(created)} envios piloto em: {OUT}')
for p in created:
    print('-', Path(p).name)
