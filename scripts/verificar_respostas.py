import os
from datetime import datetime

base = r'C:\Users\Carolina\praia-digital'
outreach_dir = os.path.join(base, 'outreach')

# Count files by type
prospeccao = [f for f in os.listdir(outreach_dir) if f.startswith('prospeccao-') and f.endswith('.txt')]
followups = [f for f in os.listdir(outreach_dir) if f.startswith('followup-') and f.endswith('.txt')]
respostas = [f for f in os.listdir(outreach_dir) if f.startswith('resposta-') and f.endswith('.txt')]
templates = [f for f in os.listdir(outreach_dir) if f.endswith('.html')]

print('=== Status do Outreach ===')
print(f'Prospecções: {len(prospeccao)}')
print(f'Follow-ups: {len(followups)}')
print(f'Respostas: {len(respostas)}')
print(f'Templates: {len(templates)}')
print(f'Total: {len(prospeccao) + len(followups) + len(respostas) + len(templates)}')
print(f'Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}')
