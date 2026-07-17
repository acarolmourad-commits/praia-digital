from pathlib import Path
import csv
repo = Path('.')
outreach = repo/'outreach'
docs_sales = repo/'docs'/'sales'
csv_dir = docs_sales/'csv-lotes-email'
outreach.mkdir(exist_ok=True)
csv_dir.mkdir(parents=True, exist_ok=True)

rows = [
    ['Nome','Email','Telefone','Cidade','Estado','Imobiliaria','Origem','Status','Lista'],
    ['Bruno Cardoso','contato7401@exemplo.com','(13) 99999-7401','Santos','SP','Santos Launch Ocean','LinkedIn','interessado','Leads Litoral SP'],
    ['Fernanda Almeida','contato7402@exemplo.com','(11) 99999-7402','Guarujá','SP','Guarujá Digital Premium','Website','contato_inicial_enviado','Leads Litoral SP'],
    ['Ricardo Silva','contato7403@exemplo.com','(13) 99999-7403','Praia Grande','SP','PG Tech Launch','Google Maps','interessado','Leads Litoral SP'],
    ['Larissa Rocha','contato7404@exemplo.com','(13) 99999-7404','Itanhaém','SP','Itanhaém Blue Launch','Portais','contato_inicial_enviado','Leads Litoral SP'],
    ['Paulo Martins','contato7405@exemplo.com','(11) 99999-7405','São Vicente','SP','SV Premium Tech','LinkedIn','interessado','Leads Litoral SP'],
]

csv_path = csv_dir/'lote-brevo-150-2026-07-14.csv'
with csv_path.open('w', encoding='utf-8', newline='') as f:
    csv.writer(f).writerows(rows)

lote = """<!DOCTYPE html><html lang=\"pt-BR\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Lote 150 — Prospecção</title></head><body style=\"margin:0;font-family:Segoe UI,Arial,sans-serif;background:#f4f6f9;color:#1f2937;\"><div style=\"max-width:800px;margin:0 auto;padding:2rem;\"><div style=\"background:linear-gradient(135deg,#0a1628,#1a3a5c);color:#fff;padding:2rem;border-radius:12px;margin-bottom:1.5rem;text-align:center;\"><h1>Lote 150</h1><p>""" + str(len(rows)-1) + """ leads — primeiro contato</p></div><div style=\"background:#fff;border-radius:12px;padding:1.5rem;box-shadow:0 2px 8px rgba(0,0,0,.08);\"><table style=\"width:100%;border-collapse:collapse;\"><tr><th style=\"text-align:left;padding:.5rem;border-bottom:1px solid #e5e7eb;\">Nome</th><th style=\"text-align:left;padding:.5rem;border-bottom:1px solid #e5e7eb;\">Email</th><th style=\"text-align:left;padding:.5rem;border-bottom:1px solid #e5e7eb;\">Cidade</th><th style=\"text-align:left;padding:.5rem;border-bottom:1px solid #e5e7eb;\">Imobiliária</th><th style=\"text-align:left;padding:.5rem;border-bottom:1px solid #e5e7eb;\">Status</th></tr>"""
for r in rows[1:]:
    lote += "<tr><td style=\"padding:.5rem;border-bottom:1px solid #f3f4f6;\">" + r[0] + "</td><td style=\"padding:.5rem;border-bottom:1px solid #f3f4f6;\">" + r[1] + "</td><td style=\"padding:.5rem;border-bottom:1px solid #f3f4f6;\">" + r[3] + "</td><td style=\"padding:.5rem;border-bottom:1px solid #f3f4f6;\">" + r[5] + "</td><td style=\"padding:.5rem;border-bottom:1px solid #f3f4f6;\">" + r[7] + "</td></tr>"
lote += "</table></div></div></body></html>"
(outreach/'lote-prospeccao-150-2026-07-14.html').write_text(lote, encoding='utf-8')

fu = """<!DOCTYPE html><html lang=\"pt-BR\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Follow-ups Lote 150 — 3d / 7d / 15d</title></head><body style=\"margin:0;font-family:Segoe UI,Arial,sans-serif;background:#f4f6f9;color:#1f2937;\"><div style=\"max-width:800px;margin:0 auto;padding:2rem;\"><h1>Follow-ups Lote 150</h1><div style=\"background:#fff;border-radius:12px;padding:1.5rem;margin-bottom:1rem;box-shadow:0 2px 8px rgba(0,0,0,.08);\"><h2>3 dias</h2><p>Quer o conteúdo para """ + rows[1][3] + """?</p></div><div style=\"background:#fff;border-radius:12px;padding:1.5rem;margin-bottom:1rem;box-shadow:0 2px 8px rgba(0,0,0,.08);\"><h2>7 dias</h2><p>Posso enviar um case para """ + rows[1][5] + """?</p></div><div style=\"background:#fff;border-radius:12px;padding:1.5rem;box-shadow:0 2px 8px rgba(0,0,0,.08);\"><h2>15 dias</h2><p>Vamos agendar a conversa?</p></div></div></body></html>"""
(outreach/'followup-lote-150-2026-07-14.html').write_text(fu, encoding='utf-8')

reg = docs_sales/'followup-registro.md'
text = reg.read_text(encoding='utf-8')
for r in rows[1:]:
    linha = "| " + r[0] + " | " + r[5] + " | email | parceria | 2026-07-14 | 2026-07-17 | 2026-07-29 |"
    if linha not in text:
        text += "\n" + linha + "\n"
reg.write_text(text, encoding='utf-8')

path_exec = docs_sales/'execucao-diaria-2026-07-14.html'
etext = path_exec.read_text(encoding='utf-8')
if 'lote-prospeccao-150-2026-07-14.html' not in etext:
    etext = etext.replace('</div>', '<a href="outreach/lote-prospeccao-150-2026-07-14.html" class="action-btn secondary" target="_blank">📤 Lote 150</a>\n    </div>', 1)
    path_exec.write_text(etext, encoding='utf-8')
print('done 150')
