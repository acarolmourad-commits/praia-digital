#!/usr/bin/env python3
"""Automacao de outreach: abre mailto para top 5 leads automaticamente."""
import csv, webbrowser, time
from pathlib import Path

BASE = Path(r'C:\Users\Carolina\praia-digital')
CSV = BASE / 'docs/sales/leads-litoral-enriquecido.csv'

def send_batch(top_n=5):
    with open(CSV, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    rows = sorted(rows, key=lambda r: int(r.get('pontuacao_lead', 0)), reverse=True)
    for row in rows[:top_n]:
        nome = row['nome_da_imobiliaria']
        email = row['email']
        subject = f"Parceria zero-custo para {nome}: receita recorrente nova, sem custo inicial"
        body = f"Ola, tudo bem?Eu sou Carolina Mourad, CEO da Praia Digital. Ajudo imobiliarias e construtoras do litoral paulista a captar mais leads qualificados e converter mais vendas.Proponho um piloto de 7 a 14 dias sem custo inicial para {nome}. Se fizer sentido, eu envio o Deep Dive antes da reunião.Links: Site: https://acarolmourad-commits.github.io/praia-digital/ Ferramentas: https://praia.digital Atenciosamente, Carolina Mourad CEO - Praia Digital (11) 95434-6288 comercial@praia.digital"
        url = f"mailto:{email}?subject={subject}&body={body}"
        webbrowser.open(url)
        time.sleep(1)

if __name__ == '__main__':
    send_batch()
