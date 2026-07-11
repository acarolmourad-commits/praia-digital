"""Classifica respostas de leads por palavras-chave, atualiza a base principal
e gera follow-ups automáticos por classificação.

Uso:
  python scripts/automation/classificar_respostas_leads.py docs/sales/respostas-leads.csv
Saídas:
  - docs/sales/leads-litoral-enriquecido-classificado.csv
  - outreach/emails-followup-classificados/*.html
"""
import csv, sys
from pathlib import Path
from datetime import datetime, timedelta

REGRAS = {
    'interessado': ['interesse','quero','sim','vamos','agendar','call','proposta','demo','avançar','pode','mande','envie','solicita','material','case','contrato'],
    'rejeitado': ['não','obrigado','agora não','sem orçamento','não preciso','recusar'],
    'fechado': ['aceito','fechado','combinado','assinar','contrato','bora','fechou','ok','parceria','voucher'],
    'neutro': ['talvez','depois','mais tarde','informaç','dúvida','preço','valor','como funciona','ajudar','esclarecer']
}

FOLLOWUP_TEMPLATES = {
    'interessado': """<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>Follow-up — {imobiliaria}</title></head>
<body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:20px;color:#222;">
  <p>Olá, <strong>{nome_contato}</strong>!</p>
  <p>Pelo seu retorno, vejo que você está <strong>interessado</strong> em avançar. Vou adiantar a próxima etapa para não perder o momento.</p>
  <p>Próximos passos sugeridos:</p>
  <ul>
    <li>Envio de proposta comercial adaptada em até 24h</li>
    <li>Agendamento de demo de 15 minutos</li>
    <li>Apresentação do case conjunto e métricas</li>
  </ul>
  <p>Se preferir, responda este e-mail com o horário que funciona melhor.</p>
  <p>Site: <a href="https://acarolmourad-commits.github.io/praia-digital/">Praia Digital</a></p>
  <p>Ferramentas gratuitas: <a href="https://praia.digital">https://praia.digital</a></p>
  <p>CEO — Praia Digital</p>
</body>
</html>""",
    'rejeitado': """<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>Follow-up — {imobiliaria}</title></head>
<body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:20px;color:#222;">
  <p>Olá, <strong>{nome_contato}</strong>!</p>
  <p>Sem problema. Vou deixar o contato aberto para quando fizer sentido. Voltarei daqui a 90 dias com novidades relevantes para {imobiliaria}.</p>
  <p>Aproveite nossas ferramentas gratuitas enquanto isso: <a href="https://praia.digital">https://praia.digital</a></p>
  <p>CEO — Praia Digital</p>
</body>
</html>""",
    'fechado': """<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>Onboarding — {imobiliaria}</title></head>
<body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:20px;color:#222;">
  <p>Olá, <strong>{nome_contato}</strong>!</p>
  <p>Ótimo! Vamos iniciar o onboarding de <strong>{imobiliaria}</strong> em até 24h. Você receberá cronograma, acessos e métricas do case.</p>
  <p>Site: <a href="https://acarolmourad-commits.github.io/praia-digital/">Praia Digital</a></p>
  <p>Ferramentas gratuitas: <a href="https://praia.digital">https://praia.digital</a></p>
  <p>CEO — Praia Digital</p>
</body>
</html>""",
    'neutro': """<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>Aprofundamento — {imobiliaria}</title></head>
<body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:20px;color:#222;">
  <p>Olá, <strong>{nome_contato}</strong>!</p>
  <p>Perfeito, vamos manter uma conversa objetiva. Seguem dados adicionais sobre redução de custos e aumento de conversão para {imobiliaria}.</p>
  <p>Se fizer sentido, reagendamos uma call de 15 minutos.</p>
  <p>Site: <a href="https://acarolmourad-commits.github.io/praia-digital/">Praia Digital</a></p>
  <p>Ferramentas gratuitas: <a href="https://praia.digital">https://praia.digital</a></p>
  <p>CEO — Praia Digital</p>
</body>
</html>"""
}

def classificar(texto):
    texto = (texto or '').lower()
    for classe, palavras in REGRAS.items():
        if any(p in texto for p in palavras):
            return classe
    return 'neutro'

def next_action(classe):
    return {
        'interessado': 'enviar_proposta',
        'rejeitado': 'follow_up_90d',
        'fechado': 'onboarding',
        'neutro': 'follow_up_7d'
    }.get(classe, 'follow_up_7d')

def main():
    if len(sys.argv) < 2:
        print('Uso: python scripts/automation/classificar_respostas_leads.py <csv_respostas>')
        sys.exit(1)
    resp_path = Path(sys.argv[1])
    root = Path('C:/Users/Carolina/praia-digital')
    out_csv = root / 'docs/sales/leads-litoral-enriquecido-classificado.csv'
    out_dir = root / 'outreach/emails-followup-classificados'
    out_dir.mkdir(parents=True, exist_ok=True)
    with resp_path.open('r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter=';'))
    headers = list(rows[0].keys()) if rows else []
    if 'classificacao' not in headers:
        headers += ['classificacao','proxima_acao','data_classificacao']
    hoje = datetime.now().strftime('%d/%m/%Y')
    processed=[]
    for r in rows:
        texto = ' '.join([str(r.get('status','')), str(r.get('observacao','')), str(r.get('dor_principal',''))])
        cls = classificar(texto)
        r['classificacao'] = cls
        r['proxima_acao'] = next_action(cls)
        r['data_classificacao'] = hoje
        processed.append(r)
    with out_csv.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=headers, delimiter=';')
        w.writeheader()
        for r in processed:
            w.writerow({k: r.get(k,'') for k in headers})
    count=0
    for r in processed:
        acao = r.get('proxima_acao','')
        template = FOLLOWUP_TEMPLATES.get(acao)
        if not template:
            continue
        nome = (r.get('pessoa_de_contato') or r.get('nome_contato') or 'Contato').strip()
        imob = (r.get('nome_da_imobiliaria') or r.get('imobiliaria') or 'Imobiliária').strip()
        fname = f"{r.get('id') or r.get('lead_id') or '0'}-{acao}-{imob.lower().replace(' ','-')[:30]}.html"
        (out_dir / fname).write_text(template.format(nome_contato=nome, imobiliaria=imob), encoding='utf-8')
        count += 1
    print('Processados:', len(processed))
    print('Classificados:', dict(__import__('collections').Counter(r.get('classificacao') for r in processed)))
    print('Follow-ups gerados:', count)
    print('Saídas:', out_csv)
    print('Pasta:', out_dir)

if __name__ == '__main__':
    main()
