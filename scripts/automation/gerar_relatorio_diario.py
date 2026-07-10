import csv, os, re
from datetime import datetime

base = r'C:\Users\Carolina\praia-digital'
outreach_dir = os.path.join(base, 'outreach')
csv_dir = os.path.join(base, 'csv-lotes-email')
docs_dir = os.path.join(base, 'docs', 'sales')
os.makedirs(docs_dir, exist_ok=True)

today = datetime.now().strftime('%Y-%m-%d')

actions = []

# Mapear leads por arquivos de prospecção
for fname in sorted(os.listdir(outreach_dir)):
    if fname.startswith('prospeccao-') and fname.endswith('.txt'):
        path = os.path.join(outreach_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            txt = f.read().strip()
        subject = txt.splitlines()[0].replace('Assunto: ', '') if txt else fname
        offer = 'captacao' if 'Captação' in txt else 'mini site' if 'Mini Site' in txt else 'video' if 'Vídeo' in txt else 'consultoria' if 'Consultoria' in txt else 'pacote' if 'Pacote Completo' in txt else 'foto'
        actions.append({'Arquivo': fname, 'Assunto': subject, 'Oferta': offer, 'Acao': 'Enviar hoje'})

# Follow-ups existentes
for fname in sorted(os.listdir(outreach_dir)):
    if fname.startswith('followup-') and fname.endswith('.txt'):
        path = os.path.join(outreach_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            txt = f.read().strip()
        offer = 'captacao' if 'Captação' in txt else 'mini site' if 'Mini Site' in txt else 'video' if 'Vídeo' in txt else 'consultoria' if 'Consultoria' in txt else 'pacote' if 'Pacote Completo' in txt else 'follow-up'
        actions.append({'Arquivo': fname, 'Assunto': 'Follow-up', 'Oferta': offer, 'Acao': 'Agendar para 72h/7d'})

# Agrupar resumo
from collections import Counter
resumo = Counter(a['Oferta'] for a in actions if a['Acao'] == 'Enviar hoje')
followups = Counter(a['Oferta'] for a in actions if a['Acao'].startswith('Agendar'))

relatorio = f"""# Relatório Diário — Ações de Prospecção
Data: {today}

## Resumo
- Total de ações planejadas: {len(actions)}
- E-mails para enviar hoje: {sum(v for k,v in resumo.items())}
  - Captação: {resumo.get('captacao',0)}
  - Mini site: {resumo.get('mini site',0)}
  - Vídeo: {resumo.get('video',0)}
  - Consultoria: {resumo.get('consultoria',0)}
  - Pacote completo: {resumo.get('pacote',0)}
- Follow-ups preparados: {sum(v for k,v in followups.items())}

## Próximos passos
1. Enviar `csv-lotes-email/checklist-envio-hoje-limpo.csv` pelo Brevo
2. Usar `outreach/emails-prontos-para-enviar.html` para colar textos
3. Responder com `outreach/resposta-automatica-leads.html`
4. Avançar negociação com `outreach/avanco-negociacao-templates.html`
"""

path = os.path.join(docs_dir, f'relatorio-diario-{datetime.now().strftime("%Y%m%d")}.md')
with open(path, 'w', encoding='utf-8') as f:
    f.write(relatorio)

print('Relatório criado:', path)
