#!/usr/bin/env python3
"""Atualiza o tracker de envios em lote após disparo Brevo/WhatsApp."""
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r'C:\Users\Carolina\praia-digital')
TRACKER = BASE / 'docs/sales/tracker-envios-unificado-2026-07-10.md'
LEADS_CSV = BASE / 'csv-lotes-email' / 'lote-brevo-30-2026-07-10.csv'


def main():
    if not LEADS_CSV.exists():
        print(f'CSV not found: {LEADS_CSV}')
        return
    with open(LEADS_CSV, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    hoje = datetime.now().strftime('%Y-%m-%d')
    linhas = [
        '# Tracker de Envios Unificado — Praia Digital',
        '',
        f'**Data base:** {hoje}',
        '**Canais monitorados:** Brevo (emails), WhatsApp (top 5 leads), Follow-ups 72h/7d',
        '',
        '---',
        '',
        '## Resumo geral',
        '',
        '| Canal | Total preparado | Enviados hoje | Follow-up 72h | Follow-up 7d |',
        '|------|----------------|---------------|---------------|--------------|',
        f"| Brevo (csv 30 emails) | 30 | {len(rows)} | 0 | 0 |",
        '| WhatsApp (top 5) | 5 | 0 | 0 | 0 |',
        f"| Total | 35 | {len(rows)} | 0 | 0 |",
        '',
        '---',
        '',
        '## Status por lead — Top 5 + lote Brevo 30',
        '',
        '### Brevo — 30 leads (lote principal)',
        '',
        '| # | Lead / Cidade | Email | Data envio | Status | Follow-up 72h | Follow-up 7d | Resposta |',
        '|---|---------------|-------|------------|--------|---------------|--------------|----------|',
    ]
    for i, r in enumerate(rows, 1):
        nome = r.get('nome', '').strip() or f'Lead {i}'
        cidade = r.get('cidade', '').strip() or '—'
        email = r.get('email', '').strip() or '—'
        linhas.append(f'| {i} | {nome} | {email} | {hoje} | Enviado | — | — | — |')
    linhas += [
        '',
        '### WhatsApp — Top 5 leads',
        '',
        '| # | Lead | Cidade | Data envio | Status | Follow-up 72h | Follow-up 7d | Resposta |',
        '|---|------|--------|------------|--------|---------------|--------------|----------|',
        '| 1 | Porto da Lua Prime | Itanhaém | — | ⏳ Aguardando envio | — | — | — |',
        '| 2 | Praia Grande Site View | Praia Grande | — | ⏳ Aguardando envio | — | — | — |',
        '| 3 | Porto da Lua Blue | Itanhaém | — | ⏳ Aguardando envio | — | — | — |',
        '| 4 | Prime Imóveis Centro | Centro Histórico | — | ⏳ Aguardando envio | — | — | — |',
        '| 5 | Costa Verde Imóveis | Costa Verde | — | ⏳ Aguardando envio | — | — | — |',
        '',
        '---',
        '',
        '## Próximos passos obrigatórios',
        '',
        f'1. **Hoje ({hoje}):**',
        '   - [ ] Confirmar envio do lote Brevo',
        '   - [ ] Enviar os 5 WhatsApps',
        '   - [ ] Registrar status final no tracker',
        '',
        '2. **72h depois:**',
        '   - [ ] Follow-up automático Brevo',
        '   - [ ] Follow-up WhatsApp Top 5',
        '',
        '3. **7d depois:**',
        '   - [ ] Follow-up final Brevo',
        '   - [ ] Follow-up final WhatsApp Top 5',
        '',
        '---',
        '',
        '## Histórico de atualizações',
        '',
        f'- {hoje}: tracker atualizado automaticamente com {len(rows)} emails enviados (Brevo)',
    ]
    TRACKER.write_text('\n'.join(linhas), encoding='utf-8')
    print(f'UPDATED {TRACKER}')


if __name__ == '__main__':
    main()
