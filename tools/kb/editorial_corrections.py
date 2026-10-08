import json
from pathlib import Path

def apply_corrections(families):
    records = json.loads((Path(__file__).parent / 'editorial_corrections_20261008.json').read_text(encoding='utf-8'))
    corrections = {record['aula']: record for record in records}
    found = set()
    for family in families.values():
        for module in family['modulos']:
            for lesson in module['aulas']:
                record = corrections.get(lesson['t'])
                if record:
                    if lesson['c'] != record['antes']:
                        raise RuntimeError('Editorial base changed; review correction: ' + lesson['t'])
                    lesson['c'] = record['depois']
                    found.add(lesson['t'])
                    if lesson['t'] == 'Case de marketing real no litoral':
                        lesson['t'] = 'Estudo de caso simulado de marketing no litoral'
    if found != set(corrections):
        raise RuntimeError('Missing editorial targets: ' + ', '.join(sorted(set(corrections) - found)))
    return families
