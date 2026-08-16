#!/usr/bin/env python3
"""
Motor B — leitor de eventos locais do site.
Lê localStorage de tracking-motor-b.js e gera relatório simples.
"""

import json
from pathlib import Path
from datetime import datetime

STORAGE_KEY = 'motor_b_events_v1'


def main():
    print('=== Motor B — Relatório de Eventos Locais ===')
    print('Para usar: exporte o localStorage do browser para um arquivo JSON')
    print('e passe o caminho como argumento.')
    print()
    print('Comando no browser console:')
    print(f'  copy(JSON.stringify(localStorage.getItem("{STORAGE_KEY}")||"[]"))')
    print()
    print('Depois salve o clipboard em um arquivo .json e execute:')
    print('  python scripts/ler_eventos_motor_b.py <arquivo.json>')
    print()
    
    import sys
    if len(sys.argv) < 2:
        sys.exit(0)
    
    path = Path(sys.argv[1])
    if not path.exists():
        print(f'Arquivo não encontrado: {path}')
        sys.exit(1)
    
    try:
        raw = path.read_text(encoding='utf-8')
        events = json.loads(raw)
    except Exception as e:
        print(f'Erro ao ler JSON: {e}')
        sys.exit(1)
    
    if not isinstance(events, list):
        print('Formato inválido: esperado array de eventos')
        sys.exit(1)
    
    print(f'Total eventos: {len(events)}')
    print()
    
    # Contagem por tipo
    from collections import Counter
    type_counts = Counter(e.get('type', 'UNKNOWN') for e in events)
    print('Por tipo:')
    for t, c in sorted(type_counts.items()):
        print(f'  {t}: {c}')
    
    # Páginas mais visitadas
    path_counts = Counter(e.get('path', 'UNKNOWN') for e in events if e.get('type') == 'page_view')
    print()
    print('Page views:')
    for p, c in path_counts.most_common(10):
        print(f'  {p}: {c}')
    
    # CTAs WhatsApp clicados
    wa_clicks = [e for e in events if e.get('type') == 'whatsapp_click']
    if wa_clicks:
        print()
        print(f'WhatsApp clicks: {len(wa_clicks)}')
        for e in wa_clicks[:5]:
            print(f'  {e.get("path")} -> {e.get("href", "")[:80]}')
    
    # Formulários submetidos
    forms = [e for e in events if e.get('type') == 'form_submit']
    if forms:
        print()
        print(f'Form submits: {len(forms)}')
        for e in forms[:5]:
            print(f'  {e.get("path")} | form={e.get("formId")} | fields={e.get("fields")}')
    
    # Timeline
    print()
    print('Timeline (primeiros 10):')
    for e in events[:10]:
        ts = e.get('timestamp', '')
        print(f'  {ts} | {e.get("type")} | {e.get("path", "")}')
    
    # Salvar resumo
    summary = {
        'total': len(events),
        'por_tipo': dict(type_counts),
        'page_views': dict(path_counts.most_common(10)),
        'whatsapp_clicks': len(wa_clicks),
        'form_submits': len(forms),
        'gerado_em': datetime.now().isoformat()
    }
    
    out_path = Path('docs/comercial/motor_b_eventos_resumo.json')
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print()
    print(f'Resumo salvo em: {out_path}')


if __name__ == '__main__':
    main()
