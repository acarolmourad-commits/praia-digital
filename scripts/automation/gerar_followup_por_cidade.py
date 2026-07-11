"""Gera e-mails de follow-up personalizados por cidade, combinando leads do CSV
com os modelos prontos em docs/sales/followup-*.md.

Saída: outreach/followup-por-cidade/email-followup-{cidade}-{lead_id}-{imobiliaria}.html
"""
import csv, re
from pathlib import Path

ROOT = Path('C:/Users/Carolina/praia-digital')
leads_path = ROOT / 'docs/sales/leads-litoral-enriquecido-emails-validos.csv'
followup_dir = ROOT / 'docs/sales'
out_dir = ROOT / 'outreach/followup-por-cidade'
out_dir.mkdir(parents=True, exist_ok=True)

cidade_map = {
    'santos': 'followup-santos.md',
    'guarujá': 'followup-guarujá.md',
    'praia grande': 'followup-praia-grande.md',
    'bertioga': 'followup-bertioga.md',
    'itanhaém': 'followup-itanhaém.md',
    'mongaguá': 'followup-mongaguá.md',
    'peruíbe': 'followup-peruíbe.md',
}

def load_followup(cidade):
    fname = cidade_map.get(cidade.lower())
    if not fname:
        return None
    p = followup_dir / fname
    if not p.exists():
        return None
    return p.read_text(encoding='utf-8')

def main():
    with leads_path.open('r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter=';'))
    count = 0
    for r in rows:
        cidade = (r.get('cidade') or '').strip()
        template = load_followup(cidade)
        if not template:
            continue
        nome = (r.get('pessoa_de_contato') or '').strip() or 'Contato'
        imob = (r.get('nome_da_imobiliaria') or '').strip() or 'Imobiliária'
        lead_id = (r.get('id') or '0').strip()
        email = (r.get('email') or '').strip()
        if not email:
            continue
        # Convert markdown template to HTML email body
        body = template.replace('**', '').replace('## ', '<h2>').replace('# ', '<h1>')
        body = re.sub(r'^- (.+)$', r'<li>\1</li>', body, flags=re.MULTILINE)
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>Follow-up {cidade} - {imob}</title></head>
<body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:20px;color:#222;">
  <p>Olá, <strong>{nome}</strong>!</p>
  {body}
  <p>Site: <a href="https://acarolmourad-commits.github.io/praia-digital/">Praia Digital</a></p>
  <p>Ferramentas gratuitas: <a href="https://praia.digital">https://praia.digital</a></p>
  <p>CEO — Praia Digital</p>
</body>
</html>"""
        fname = f"{lead_id.zfill(3)}-{cidade.lower().replace(' ','-')}-{imob.lower().replace(' ','-')[:30]}.html"
        (out_dir / fname).write_text(html, encoding='utf-8')
        count += 1
    print(f'Gerados {count} e-mails de follow-up por cidade em {out_dir}')

if __name__ == '__main__':
    main()
