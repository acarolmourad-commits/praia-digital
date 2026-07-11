from pathlib import Path
import csv

p = Path('docs/sales/leads-litoral-enriquecido-exemplo-teste.csv')
out_dir = Path('outreach/teste-csv-real')
out_dir.mkdir(parents=True, exist_ok=True)
rows = []
with p.open('r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))
print('rows', len(rows))
for r in rows:
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>Parceria - {r['nome_imobiliaria']}</title></head>
<body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:20px;color:#222;">
  <p>Olá, <strong>{r['nome_contato']}</strong>!</p>
  <p>Sou <strong>CEO da Praia Digital</strong>, startup focada no litoral paulista. Acompanho a <strong>{r['nome_imobiliaria']}</strong> em <strong>{r['cidade']}/{r['uf']}</strong>.</p>
  <p>Oferecemos <strong>ferramentas gratuitas de IA</strong> em <a href="https://praia.digital">https://praia.digital</a> e conteúdo SEO local.</p>
  <p>Queremos primeiro entregar valor com um caso conjunto real, sem custo inicial.</p>
  <p>Site: <a href="https://acarolmourad-commits.github.io/praia-digital/">https://acarolmourad-commits.github.io/praia-digital/</a></p>
  <p>CEO — Praia Digital | (11) 95434-6288</p>
</body>
</html>"""
    imob = r['nome_imobiliaria'].lower().replace(' ', '-')[:30]
    fname = f"{r['lead_id'].zfill(3)}-{imob}.html"
    (out_dir / fname).write_text(html, encoding='utf-8')
    print('email', fname)
print('emails:', len(rows))

out_csv = Path('docs/sales/csv-lotes-email/teste-csv-real-importavel-2026-07-12.csv')
headers = ['email','nome','imobiliaria','cidade','uf','whatsapp','assunto','corpo_html']
with out_csv.open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(headers)
    for r in rows:
        w.writerow([
            r.get('email',''),
            r.get('nome_contato',''),
            r.get('nome_imobiliaria',''),
            r.get('cidade',''),
            r.get('uf',''),
            r.get('whatsapp',''),
            'Parceria Praia Digital',
            'template-email-real'
        ])
print('csv:', out_csv)
