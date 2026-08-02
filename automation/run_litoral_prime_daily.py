#!/usr/bin/env python3
"""
run_litoral_prime_daily.py
Runner diário da Litoral Prime: captura, follow-up e métricas.
Uso: python litoral-prime-imoveis/automation/run_litoral_prime_daily.py
"""
import csv
import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
LEADS_FILE = BASE / 'docs/leads-litoral-prime.csv'
TRACKER_FILE = BASE / 'docs/tracker-litoral-prime.csv'
PORTFOLIO = BASE / 'imoveis/portfolio.json'
REPORT_FILE = BASE / 'docs/relatorio-diario-litoral-prime.html'

for f in [LEADS_FILE, TRACKER_FILE]:
    f.parent.mkdir(parents=True, exist_ok=True)

MENSAGENS = {
    'comprar': 'Olá! Temos ótimas opções de compra no litoral de SP. Qual seu perfil?',
    'alugar': 'Olá! Podemos ajudar a encontrar o imóvel ideal para alugar.',
    'vender': 'Olá! Faça uma avaliação gratuita do seu imóvel no litoral de SP.',
}

def mensagem_boas_vindas(nome):
    return f"Olá, {nome}! Bem-vindo à Litoral Prime. Em breve um especialista vai te atender."

def enviar_whatsapp(telefone, mensagem):
    print(f"[WhatsApp] {telefone}: {mensagem}")

def capturar_lead(nome, email, telefone, interesse, mensagem=''):
    hoje = datetime.now().strftime('%Y-%m-%d')
    lead_id = datetime.now().strftime('%Y%m%d%H%M%S')
    with LEADS_FILE.open('a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        if LEADS_FILE.stat().st_size == 0:
            writer.writerow(['lead_id','nome','email','telefone','interesse','mensagem','data_criacao'])
        writer.writerow([lead_id, nome, email, telefone, interesse, mensagem, hoje])
    with TRACKER_FILE.open('a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        if TRACKER_FILE.stat().st_size == 0:
            writer.writerow(['lead_id','nome','interesse','status','data_envio','observacao'])
        writer.writerow([lead_id, nome, interesse, 'novo', hoje, ''])
    return lead_id

def follow_up_novos_leads():
    leads = []
    if LEADS_FILE.exists():
        with LEADS_FILE.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                leads.append(row)
    processados = 0
    for lead in leads:
        interesse = lead.get('interesse', '')
        telefone = lead.get('telefone', '')
        nome = lead.get('nome', '')
        if telefone:
            enviar_whatsapp(telefone, mensagem_boas_vindas(nome))
            processados += 1
        if interesse and telefone:
            enviar_whatsapp(telefone, MENSAGENS.get(interesse, 'Entraremos em contato em breve.'))
            processados += 1
    return processados

def gerar_relatorio():
    hoje = datetime.now().strftime('%Y-%m-%d')
    leads = []
    if LEADS_FILE.exists():
        with LEADS_FILE.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                leads.append(row)
    total = len(leads)
    por_interesse = {}
    for lead in leads:
        i = lead.get('interesse', 'outro')
        por_interesse[i] = por_interesse.get(i, 0) + 1
    por_dia = {}
    for lead in leads:
        d = lead.get('data_criacao', hoje)
        por_dia[d] = por_dia.get(d, 0) + 1
    html = f"""
<!DOCTYPE html><html lang='pt-BR'><head><meta charset='UTF-8'><title>Relatório Diário — Litoral Prime</title>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#f8fafc;color:#0f172a;padding:24px}}
.wrap{{max-width:980px;margin:0 auto}}
.card{{background:#fff;border:1px solid #e5e7eb;border-radius:18px;padding:18px;margin:14px 0}}
table{{width:100%;border-collapse:collapse;margin-top:10px}}th,td{{border:1px solid #e5e7eb;padding:8px;text-align:left;font-size:13px}}
</style></head><body><div class='wrap'>
<div class='card'><h1>Relatório Diário — Litoral Prime</h1><p class='muted'>Data: {hoje}</p></div>
<div class='card'><h2>Resumo</h2><p>Total de leads: <strong>{total}</strong></p>
<table><tr><th>Interesse</th><th>Quantidade</th></tr>
"""
    for k,v in por_interesse.items():
        html += f"<tr><td>{k}</td><td>{v}</td></tr>"
    html += """</table></div>
<div class='card'><h2>Leads por dia</h2><table><tr><th>Data</th><th>Leads</th></tr>"""
    for k,v in sorted(por_dia.items()):
        html += f"<tr><td>{k}</td><td>{v}</td></tr>"
    html += "</table></div></div></body></html>"
    REPORT_FILE.write_text(html, encoding='utf-8')
    print(f"[Litoral Prime] Relatório gerado: {REPORT_FILE}")

def main():
    print("[Litoral Prime] Executando runner diário...", datetime.now())
    processados = follow_up_novos_leads()
    print(f"[Litoral Prime] Follow-ups enviados: {processados}")
    gerar_relatorio()
    print("[Litoral Prime] Runner concluído.")

if __name__ == '__main__':
    main()
