#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de follow-up automático por gatilho de resposta do lead.
Classifica a resposta recebida e envia automaticamente a próxima ação ideal:
- Proposta comercial
- Convite para demo 15min
- Follow-up curto
- Encerramento / nurturing
"""
import os
import re
import json
import random
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(BASE, "outreach", "followup-gatilho-resposta")
TRACKER_PATH = os.path.join(BASE, "docs", "sales", "followup-registro.md")

INTENT_RULES = [
    {
        "intent": "interesse_alto",
        "keywords": [
            "quero", "vamos", "pode enviar", "aceito", "concordo", "entendo",
            "sim", "claro", "perfeito", "avançar", "fechar", "contratar",
            "demonstração", "reunião", "ligação", "proposta"
        ],
        "weight": 3
    },
    {
        "intent": "interesse_medio",
        "keywords": [
            "interessante", "interesse", "pode mandar", "gostaria",
            "informação", "detalhes", "valores", "como funciona",
            "pode me explicar", "quando pode"
        ],
        "weight": 2
    },
    {
        "intent": "objecao_preco",
        "keywords": [
            "caro", "investimento", "orçamento", "sem verba", "custoso",
            "alto", "não tem como", "preço elevado", "descontos"
        ],
        "weight": 1
    },
    {
        "intent": "objecao_tempo",
        "keywords": [
            "agora não", "depois", "momento", "temporada",
            "janeiro", "fevereiro", "março", "ocupado", "ocupada"
        ],
        "weight": 1
    },
    {
        "intent": "objecao_ferramenta",
        "keywords": [
            "já tenho", "já uso", "outra ferramenta", "sistema",
            "estamos com outra", "não preciso", "não quero"
        ],
        "weight": 1
    },
    {
        "intent": "rejeicao",
        "keywords": [
            "não", "não obrigado", "não tenho interesse",
            "fora", "não agora", "pare", "remover"
        ],
        "weight": -2
    }
]

NEXT_ACTION_MAP = {
    "interesse_alto": "enviar_proposta_comercial",
    "interesse_medio": "agendar_demo_15min",
    "objecao_preco": "followup_preco",
    "objecao_tempo": "followup_tempo",
    "objecao_ferramenta": "followup_ferramenta",
    "rejeicao": "encerrar_nurturing"
}

NEXT_ACTION_TITLES = {
    "enviar_proposta_comercial": "Enviar Proposta Comercial",
    "agendar_demo_15min": "Agendar Demo 15min",
    "followup_preco": "Follow-up de Preço",
    "followup_tempo": "Follow-up de Tempo",
    "followup_ferramenta": "Follow-up de Ferramentas",
    "encerrar_nurturing": "Encerrar / Nurturing"
}

TEMPLATE_BY_ACTION = {
    "enviar_proposta_comercial": "outreach/template-proposta-comercial-padrao-parcerias-praia-digital-2026.html",
    "agendar_demo_15min": "outreach/template-convite-demo-15min-parcerias-2026.html",
    "followup_preco": "outreach/template-objecao-ja-tenho-ferramentas-imobiliaria.html",
    "followup_tempo": "outreach/template-negociacao-avancada-parcerias-litoral-2026.html",
    "followup_ferramenta": "outreach/template-negociacao-avancada-parcerias-litoral-2026.html",
    "encerrar_nurturing": "outreach/template-followup-curto-leads-silenciosos-2026.html"
}

def classify_response(text: str) -> str:
    text_lower = text.lower()
    scores = {}
    for rule in INTENT_RULES:
        score = sum(1 for kw in rule["keywords"] if kw in text_lower)
        if score > 0:
            scores[rule["intent"]] = scores.get(rule["intent"], 0) + score * rule["weight"]
    if not scores:
        return "interesse_medio"
    return max(scores, key=scores.get)

def suggest_next_action(intent: str) -> str:
    return NEXT_ACTION_MAP.get(intent, "followup_curto")

def generate_followup_html(lead_name: str, lead_company: str, action: str, original_message: str, city: str) -> str:
    title = NEXT_ACTION_TITLES.get(action, "Follow-up")
    template_ref = TEMPLATE_BY_ACTION.get(action, TEMPLATE_BY_ACTION["encerrar_nurturing"])
    followup_id = f"gatilho-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Follow-up #{followup_id} — {lead_company}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 20px; }}
        .container {{ max-width: 720px; margin: 0 auto; background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 4px 24px rgba(0,0,0,0.05); }}
        .header {{ background: #0d47a1; color: #fff; padding: 18px; border-radius: 12px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0 0 6px; font-size: 20px; }}
        .meta {{ color: #617d8b; font-size: 13px; margin-bottom: 18px; }}
        .message-box {{ background: #f1f5f9; border-left: 4px solid #0d47a1; padding: 14px; border-radius: 10px; margin-bottom: 18px; }}
        .action-box {{ background: #fff8e1; border: 1px solid #ffe082; padding: 18px; border-radius: 12px; }}
        .action-box h3 {{ margin-top: 0; color: #f57c00; }}
        .next-action {{ display: inline-block; background: #0d47a1; color: #fff; padding: 10px 16px; border-radius: 8px; margin-top: 14px; font-weight: bold; }}
        .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #617d8b; }}
        a {{ color: #0d47a1; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Follow-up automático por gatilho de resposta</h1>
            <div style="font-size:13px;opacity:.9;">Praia Digital — resposta adaptada ao perfil do lead</div>
        </div>
        <div class="meta">
            <strong>Lead:</strong> {lead_name} — {lead_company} ({city})<br>
            <strong>ID:</strong> {followup_id}<br>
            <strong>Data/hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}
        </div>
        <div class="message-box">
            <strong>Mensagem recebida:</strong><br>
            {original_message}
        </div>
        <div class="action-box">
            <h3>Ação recomendada</h3>
            <p>A resposta foi classificada como <strong>{action.replace('_', ' ').title()}</strong>.</p>
            <p>Próxima ação ideal: <strong>{title}</strong>.</p>
            <p>Template base sugerido: <code>{template_ref}</code></p>
            <span class="next-action">{title}</span>
        </div>
        <div class="footer">
            Este follow-up foi sugerido automaticamente pelo motor de gatilho de resposta.<br>
            Site: <a href="https://acarolmourad-commits.github.io/praia-digital/">Praia Digital</a> | Ferramentas grátis: <a href="https://praia.digital">praia.digital</a>
        </div>
    </div>
</body>
</html>"""
    return html


def process_csv_answers(csv_path: str):
    if not os.path.exists(csv_path):
        print(f"Arquivo não encontrado: {csv_path}")
        return
    results = []
    with open(csv_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(";")]
            if len(parts) < 4:
                continue
            lead_name, lead_company, city, message = parts[0], parts[1], parts[2], parts[3]
            intent = classify_response(message)
            action = suggest_next_action(intent)
            html = generate_followup_html(lead_name, lead_company, action, message, city)
            results.append({
                "lead_name": lead_name,
                "lead_company": lead_company,
                "city": city,
                "intent": intent,
                "action": action,
                "html": html
            })
    os.makedirs(OUT_DIR, exist_ok=True)
    for i, item in enumerate(results, 1):
        filename = f"gatilho-resposta-{i:03d}-{item['lead_company'].replace(' ', '-').lower()}.html"
        path = os.path.join(OUT_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(item["html"])
    summary_path = os.path.join(OUT_DIR, "resumo-classificacao-gatilho.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        for item in results:
            f.write(f"- {item['lead_company']} ({item['city']}) => {item['intent']} -> {item['action']}\n")
    print(f"Gerados {len(results)} follow-ups por gatilho em {OUT_DIR}")
    print(f"Resumo: {summary_path}")
    return summary_path


def main():
    default_csv = os.path.join(BASE, "docs", "sales", "respostas-leads.csv")
    if not os.path.exists(default_csv):
        print("Arquivo de respostas não encontrado. Nenhum lead respondeu ainda.")
        print(f"Crie o CSV em: {default_csv}")
        print("Colunas: nome;empresa;cidade;mensagem_recebida")
        return


if __name__ == "__main__":
    main()
