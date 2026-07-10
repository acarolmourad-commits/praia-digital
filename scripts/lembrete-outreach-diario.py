import os, datetime

repo = r"C:\Users\Carolina\praia-digital"
csv_dir = os.path.join(repo, "csv-lotes-email")

now = datetime.date.today().isoformat()

msg = f"""CHECKLIST OUTREACH — {now}

1. Brevo: importar e enviar csv-lotes-email/batch-30-emails-2026-07-10.csv
2. WhatsApp: enviar mensagens de outreach/acao-completa.html
3. Follow-up: verificar docs/sales/followup-registro.md
4. Respostas: usar outreach/resposta-interesse-agendar-call.txt
5. Instagram: publicar conteúdo de marketing/instagram/

Links:
- Ação completa: outreach/acao-completa.html
- Brevo: https://www.brevo.com
- Site: https://acarolmourad-commits.github.io/praia-digital/
- Ferramentas: https://praia.digital
"""

print(msg)
