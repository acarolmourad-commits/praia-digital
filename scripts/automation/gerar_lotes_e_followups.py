#!/usr/bin/env python3
"""
gerar_lotes_e_followups.py
Gera automaticamente lotes de prospecção, páginas de imóveis e follow-ups personalizados.
Uso: python scripts/automation/gerar_lotes_e_followups.py
"""

import csv
import json
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path(__file__).resolve().parents[2]
IMOVEIS_DIR = BASE / "imoveis"
OUTREACH_DIR = BASE / "outreach"
BLOG_DIR = BASE / "blog"
TRACKER_CSV = BASE / "docs/sales/tracker_envios.csv"
LEADS_CSV = BASE / "docs/sales/leads-litoral-enriquecido.csv"

TOOLS = {
    "avaliacao": "/praia-digital/ferramentas-gratuitas/imobiliarias/avaliacao-preco-mercado-litoral.html",
    "comparar": "/praia-digital/ferramentas-gratuitas/imobiliarias/comparar-imoveis-litoral.html",
    "gerador": "/praia-digital/ferramentas-gratuitas/imobiliarias/gerador-descricao-ia.html",
    "assistente": "/praia-digital/ferramentas-gratuitas/imobiliarias/assistente-virtual-compradores-litoral.html",
    "recomendacao": "/praia-digital/ferramentas-gratuitas/imobiliarias/recomendacao-automatica-imoveis-litoral.html",
    "roteiro": "/praia-digital/ferramentas-gratuitas/imobiliarias/roteiro-visita-automatico-litoral.html",
    "analise": "/praia-digital/ferramentas-gratuitas/imobiliarias/analise-retorno-temporada-litoral.html",
    "predicao": "/praia-digital/ferramentas-gratuitas/imobiliarias/predicao-vendas-litoral.html",
    "orcamento": "/praia-digital/ferramentas-gratuitas/imobiliarias/orcamento-temporada-litoral.html",
    "agendamento": "/praia-digital/ferramentas-gratuitas/imobiliarias/agendamento-visita-automatico-litoral.html",
    "checklist-captacao": "/praia-digital/ferramentas-gratuitas/imobiliarias/checklist-captacao-imoveis-litoral.html",
    "checklist-documentacao": "/praia-digital/ferramentas-gratuitas/imobiliarias/checklist-documentacao-imoveis-litoral.html",
    "onboarding": "/praia-digital/ferramentas-gratuitas/imobiliarias/onboarding-rapido-parceiros-praia-digital-2026.html",
    "guia-aluguel": "/praia-digital/ferramentas-gratuitas/imobiliarias/guia-aluguel-temporada-litoral.html",
    "pre-qualificacao": "/praia-digital/ferramentas-gratuitas/imobiliarias/pre-qualificacao-leads-litoral.html",
}

SEO_ARTICLES = [
    "/praia-digital/blog/funil-vendas-imobiliaria-litoral-2026.html",
    "/praia-digital/blog/modelo-proposta-parceria-imobiliaria-litoral-2026.html",
    "/praia-digital/blog/case-social-rapido-parcerias-imobiliarias-litoral-2026.html",
    "/praia-digital/blog/reels-imoveis-litoral-paulista-2026.html",
    "/praia-digital/blog/instagram-imobiliaria-litoral-paulista-2026.html",
    "/praia-digital/blog/videos-imoveis-convertem-litoral-2026.html",
    "/praia-digital/blog/prova-social-imobiliaria-litoral-paulista-2026.html",
    "/praia-digital/blog/links-curtos-imoveis-convertem-litoral-2026.html",
    "/praia-digital/blog/gestao-disponibilidade-temporada-litoral-2026.html",
    "/praia-digital/blog/geracao-leads-qualificados-temporada-litoral-2026.html",
]

PROPERTIES = [
    ("imovel-0288", "Apartamento com Sacada Gourmet — Cananéia", "Cananéia"),
    ("imovel-0289", "Sobrado Geminado — São Sebastião", "São Sebastião"),
    ("imovel-0290", "Casa em Condomínio — Maresias", "Maresias"),
    ("imovel-0291", "Loft Moderno — Guarujá", "Guarujá"),
    ("imovel-0292", "Apartamento Vista Mar — Praia Grande", "Praia Grande"),
    ("imovel-0293", "Casa Rural — Iguape", "Iguape"),
    ("imovel-0294", "Cobertura Duplex — Ilhabela", "Ilhabela"),
    ("imovel-0295", "Studio para Temporada — Ubatuba", "Ubatuba"),
    ("imovel-0296", "Casa com Piscina — Caraguatatuba", "Caraguatatuba"),
    ("imovel-0297", "Apartamento Beira-Mar — Bertioga", "Bertioga"),
]

LOTE_MIX = {
    "31": ["orcamento", "onboarding"],
    "32": ["checklist-captacao", "checklist-documentacao"],
    "33": ["gerador", "roteiro"],
    "34": ["avaliacao", "comparar"],
    "35": ["assistente", "guia-aluguel", "pre-qualificacao"],
}


def ensure_csv(path, headers):
    if not path.exists():
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()


def save_tracker(rows):
    headers = [
        "nome",
        "email",
        "cidade",
        "imovel_url",
        "fonte",
        "data_captura",
        "status",
        "ultimo_contato",
        "proxima_acao",
        "observacoes",
        "lote",
        "ferramenta",
    ]
    ensure_csv(TRACKER_CSV, headers)
    with open(TRACKER_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerows(rows)


def build_followup(city, lead_name, imovel_url, tool_url, day):
    today = datetime.now().isoformat()
    next_date = (datetime.now() + timedelta(days=int(day))).isoformat()
    return {
        "nome": lead_name,
        "cidade": city,
        "imovel_url": imovel_url,
        "tool_url": tool_url,
        "day": day,
        "next_date": next_date,
        "created_at": today,
    }


def generate():
    tracker_rows = []
    followups = []
    for lote, tools in LOTE_MIX.items():
        for idx, (prop_id, prop_title, city) in enumerate(PROPERTIES[:2], start=1):
            imovel_url = f"/praia-digital/imoveis/{prop_id}.html"
            lead_name = f"Lead {lote}-{idx}"
            lead_email = f"lead{lote}{idx}@example.com"
            tool_url = TOOLS[tools[idx % len(tools)]]
            tracker_rows.append(
                {
                    "nome": lead_name,
                    "email": lead_email,
                    "cidade": city,
                    "imovel_url": imovel_url,
                    "fonte": "lote",
                    "data_captura": datetime.now().isoformat(),
                    "status": "novo",
                    "ultimo_contato": "",
                    "proxima_acao": f"follow-up {day('3d', lote)}",
                    "observacoes": f"Lote {lote}",
                    "lote": lote,
                    "ferramenta": tool_url,
                }
            )
            for d in ["3", "7"]:
                followups.append(build_followup(city, lead_name, imovel_url, tool_url, d))

    save_tracker(tracker_rows)
    followup_path = BASE / "docs/sales/followups_gerados.json"
    with open(followup_path, "w", encoding="utf-8") as f:
        json.dump(followups, f, indent=2, ensure_ascii=False)


def day(label, lote):
    # simple deterministic mix
    return "3" if (int(lote) % 2 == 0) else "7"


if __name__ == "__main__":
    generate()
    print("Lotes gerados. Follow-ups salvos em docs/sales/followups_gerados.json")
