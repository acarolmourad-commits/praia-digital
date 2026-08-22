"""Fix dry-run report targets for Lote 1 and regenerate report."""
import json
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
REPORT_PATH = BASE / 'scripts/link_automation/dry-run-report.json'

PREFIX_MAP = {
    'diagnosticos-anfitrioes.html': 'anfitrioes/diagnosticos-anfitrioes.html',
    'tutoriais-anfitrioes.html': 'anfitrioes/tutoriais-anfitrioes.html',
    'checklists-anfitrioes.html': 'anfitrioes/checklists-anfitrioes.html',
    'analise-completa-imovel.html': 'assets/analise-completa-imovel.html',
    'roi-ia-imobiliaria.html': 'assets/roi-ia-imobiliaria.html',
    'servico-avaliacao-preco-imoveis-litoral.html': 'assets/servico-avaliacao-preco-imoveis-litoral.html',
}

report = json.loads(REPORT_PATH.read_text(encoding='utf-8'))
changed = 0
for c in report['batch']['candidates']:
    if c['status'] != 'REPARAR':
        continue
    href = c['original_href']
    if href in PREFIX_MAP:
        new_target = PREFIX_MAP[href]
        if c['target_href'] != new_target:
            c['target_href'] = new_target
            changed += 1

REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print('fixed', changed)
