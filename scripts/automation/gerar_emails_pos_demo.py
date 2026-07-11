"""Lê docs/sales/csv-lotes-email/pos-demo-qualificados-2026-07-12.csv
e gera e-mails HTML personalizados por proxima_acao em outreach/emails-pos-demo/.
"""
import csv
from pathlib import Path

ROOT = Path('C:/Users/Carolina/praia-digital')
csv_path = ROOT / 'docs/sales/csv-lotes-email/pos-demo-qualificados-2026-07-12.csv'
out_dir = ROOT / 'outreach/emails-pos-demo'
out_dir.mkdir(parents=True, exist_ok=True)

TEMPLATES = {
    'enviar_proposta': """<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>Proposta - {imobiliaria}</title></head>
<body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:20px;color:#222;">
  <p>Olá, <strong>{nome_contato}</strong>!</p>
  <p>Obrigado pela demo. Segue proposta comercial da Praia Digital para <strong>{imobiliaria}</strong>, com início sem custo e case conjunto.</p>
  <p>Acesse detalhes: <a href="https://acarolmourad-commits.github.io/praia-digital/">site</a>.</p>
  <p>Ferramentas gratuitas: <a href="https://praia.digital">https://praia.digital</a></p>
  <p>CEO — Praia Digital</p>
</body>
</html>""",
    'onboarding': """<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>Onboarding - {imobiliaria}</title></head>
<body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:20px;color:#222;">
  <p>Olá, <strong>{nome_contato}</strong>!</p>
  <p>Vamos começar o onboarding de <strong>{imobiliaria}</strong> em até 24h. Você receberá cronograma, acesso e métricas.</p>
  <p>Links úteis: <a href="https://acarolmourad-commits.github.io/praia-digital/">site</a> | <a href="https://praia.digital">ferramentas gratuitas</a></p>
  <p>CEO — Praia Digital</p>
</body>
</html>""",
    'assinatura': """<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>Assinatura - {imobiliaria}</title></head>
<body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:20px;color:#222;">
  <p>Olá, <strong>{nome_contato}</strong>!</p>
  <p>Parabéns pelo fechamento com <strong>{imobiliaria}</strong>. O documento de assinatura está pronto e inclui participação no case oficial.</p>
  <p>Site: <a href="https://acarolmourad-commits.github.io/praia-digital/">Praia Digital</a></p>
  <p>Ferramentas gratuitas: <a href="https://praia.digital">https://praia.digital</a></p>
  <p>CEO — Praia Digital</p>
</body>
</html>""",
}

def main():
    with csv_path.open('r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter=';'))
    count = 0
    for r in rows:
        acao = (r.get('proxima_acao') or '').strip()
        template = TEMPLATES.get(acao)
        if not template:
            continue
        nome = (r.get('nome_contato') or '').strip() or 'Contato'
        imob = (r.get('imobiliaria') or '').strip() or 'Imobiliária'
        fname = f"{r.get('lead_id','0').zfill(3)}-{acao}-{imob.lower().replace(' ','-')[:30]}.html"
        html = template.format(nome_contato=nome, imobiliaria=imob)
        (out_dir / fname).write_text(html, encoding='utf-8')
        count += 1
    print(f'Gerados {count} e-mails pós-demo em {out_dir}')

if __name__ == '__main__':
    main()
