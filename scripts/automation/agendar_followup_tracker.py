#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agenda follow-ups no tracker unificado com base em regras.
Gera linhas prontas para docs/sales/followup-registro.md
"""

import os
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACKER = os.path.join(ROOT, 'docs/sales/followup-registro.md')

DAY0_HOURS = 0
DAY3_HOURS = 72
DAY7_HOURS = 168


def add_entry(nome, imobiliaria, canal, tipo, data_ref):
    ref = datetime.strptime(data_ref, '%Y-%m-%d')
    d0 = ref + timedelta(hours=DAY0_HOURS)
    d3 = ref + timedelta(hours=DAY3_HOURS)
    d7 = ref + timedelta(hours=DAY7_HOURS)
    lines = [
        f'| {nome} | {imobiliaria} | {canal} | {tipo} | {d0.strftime("%Y-%m-%d")} | {d3.strftime("%Y-%m-%d")} | {d7.strftime("%Y-%m-%d")} |'
    ]
    with open(TRACKER, 'a', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print('Entrada adicionada no tracker.')


def main():
    print('Agendamento rápido de follow-up no tracker')
    nome = input('Nome do lead: ').strip()
    imobiliaria = input('Imobiliária: ').strip()
    canal = input('Canal (email/whatsapp): ').strip()
    tipo = input('Tipo (parceria/venda/teste): ').strip()
    data_ref = input('Data de referência (YYYY-MM-DD): ').strip()
    add_entry(nome, imobiliaria, canal, tipo, data_ref)


if __name__ == '__main__':
    main()
