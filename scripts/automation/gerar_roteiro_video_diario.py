#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de roteiros de vídeo diários para YouTube/Reels/TikTok
focado em conteúdo imobiliário para o litoral paulista.
Gera variações suficientes para 14 dias sem repetição.
"""
import json
import os
import random
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "marketing", "videos")
TEMPLATE_POOL = "marketing" + os.sep + "roteiro-video-diario-7dias.html"

TEMPLATES = [
    {
        "canal": "youtube",
        "formato": "longo",
        "temas": [
            "5 bairros do litoral paulista para investir NOW 2026",
            "Como avaliar se um imóvel no litoral vale a pena para temporada",
            "IMOXY: 7 erros que corretores cometem ao anunciar no verão",
            "IA para imobiliárias no litoral: 3 usos práticos hoje",
            "Checklist 30 itens antes de visitar um apartamento na praia",
            "Predição de preço: 3 exemplos reais no litoral paulista",
            "Gestão de temporada sem dor de cabeça para corretores",
            "Captação de imóveis offseason: roteiro completo",
            "WhatsApp Business para imobiliárias: automação passo a passo",
            "SEO local para corretores do litoral: guia definitivo",
            "Negociação de imóveis na praia: 11 táticas testadas",
            "Follow-up automático: do primeiro contato ao fechamento",
            "Cases reais: como parceiros da Praia Digital aumentam vendas",
            "Como usar avaliação automática de preço no atendimento",
            "Assistente virtual para compradores: first response e qualificação",
            "Otimização de anúncios para marketplace de temporada",
            "LGPD para imobiliárias: o que realmente muda no dia a dia",
            "Google Business Profile para agências do litoral",
            "Reativação de leads frios sem parecer insistente",
            "Geração de descrições de imóveis com IA em 60s",
            "Plano de assinatura para corretores: quando contratar",
            "Modelo econômico de temporada: sazonalidade e fluxo de caixa",
            "Como estruturar parceria entre imobiliárias no litoral",
            "Visita virtual e staging digital: quando usar e por quê",
            "Indicadores que todo corretor deve medir na temporada"
        ],
        "cta": "Acesse ferramentas gratuitas em https://praia.digital  |  Fale com a Praia Digital pelo WhatsApp",
        "tags": ["imobiliaria litoral", "corretor de imoveis", "investimento imobiliario", "praia digital", "ferramentas para corretores"]
    },
    {
        "canal": "reels",
        "formato": "curto",
        "temas": [
            "3 perguntas para fechar mais vendas no verão",
            "1 erro que custa vendas no litoral",
            "2 templates prontos para WhatsApp de corretor",
            "Ferramenta grátis para avaliar imóvel em 1 minuto",
            "5 segundos que fazem o cliente responder",
            "Copy que converte para temporada",
            "Hook de abertura para visita de imóvel",
            "Número que você deve pedir no primeiro contato",
            "Follow-up que não parece insistente",
            "Checklist de visita rápida para compradores",
            "Prompt de IA para gerar descrição de imóvel",
            "Objeção comum: resolvida em 15 palavras",
            "SEO local em 3 passos para corretores",
            "O que é parceria inteligente no litoral",
            "Melhor horário para enviar WhatsApp de venda"
        ],
        "cta": "Veja mais ferramentas gratuitas em https://praia.digital  |  Curte e compartilha",
        "tags": ["corretor", "imoveis", "litoral", "vendas", "negocios", "temporada"]
    },
    {
        "canal": "tiktok",
        "formato": "curto",
        "temas": [
            "Dica rápida para atrair mais clientes na praia",
            "Erro novo na captação de imóveis para temporada",
            "Modelo de proposta pronta para imobiliárias",
            "Automação que economiza horas por semana",
            "Comparação de bairros do litoral em 60s",
            "O que o comprador pensa antes de fechar",
            "Viés de ancoragem usado no preço do imóvel",
            "Follow-up no Instagram para alta temporada",
            "Robô de atendimento para corretor iniciante",
            "Ganhar dinheiro no pico e na baixa temporada"
        ],
        "cta": "Ferramentas gratuitas para corretores: https://praia.digital  |  Segue para mais dicas",
        "tags": ["imobiliaria", "corretor", "litoral", "vendas", "dicas", "ia"]
    }
]

HOOKS = [
    "Hoje eu vou te mostrar exatamente o que funciona no litoral, sem teoria.",
    "Esse método já ajudou parceiros a acelerar vendas.",
    "Essa dica é diferente porque eu testei na prática.",
    "Se você é corretor do litoral, pare de cometer esse erro.",
    "Vou entregar um roteiro que você pode usar hoje mesmo.",
    "Isso vai economizar horas no seu atendimento.",
    "Eu não entendo por que mais corretores não fazem isso.",
    "Essa ferramenta grátis mudou nosso fluxo.",
    "O que eu vou mostrar é para quem quer vender mais no verão.",
    "Chega de perder resposta de cliente por demora."
]

BODY_FRAMES_LONGO = [
    [
        "Contexto rápido: o litoral mudou.",
        "Hoje o comprador compara preço, prazo e experiência antes da primeira visita.",
        "Se a sua imobiliária não responde em minutos, você já perdeu.",
        "A solução não é contratar mais gente. É usar automação inteligente.",
        "Nós testamos essa abordagem com parceiros e o resultado foi mais agendamentos em menos tempo."
    ],
    [
        "Primeiro, entenda o problema real.",
        "Depois, escolha a ferramenta que resolve o gargalo.",
        "Depois, meça o resultado em respostas por dia.",
        "Depois, repita com base no que melhorar.",
        "Esse ciclo vale para temporada alta e baixa."
    ],
    [
        "O erro mais caro é anunciar sem copy.",
        "O segundo erro é enviar proposta sem qualificação.",
        "O terceiro é não follow-up por medo de parecer insistente.",
        "Se você corrigir esses três pontos, suas conversas já melhoram.",
        "E o melhor: pode fazer isso com ferramentas gratuitas."
    ]
]

BODY_FRAMES_CURTO = [
    "Esse hook quebra a objeção em 3s.",
    "Esse modelo de resposta encurta o ciclo.",
    "Esse prompt entrega descrição de imóvel em segundos.",
    "Esse checklist evita visita desperdiçada.",
    "Essa dica remove a desconfiança do primeiro contato."
]

def format_duration(seconds: int) -> str:
    m = seconds // 60
    s = seconds % 60
    return f"{m:02d}:{s:02d}"

def build_youtube_block(idx: int, tema: str) -> dict:
    body = BODY_FRAMES_LONGO[idx % len(BODY_FRAMES_LONGO)]
    roteiro = {
        "canal": "YouTube",
        "tema": tema,
        "duracao": random.choice([480, 540, 660]),
        "titulo_sugerido": tema,
        "descricao": f"{tema}\n\nNeste vídeo eu mostro um passo a passo prático com aplicação no litoral paulista.",
        "hook": random.choice(HOOKS),
        "blocos": [
            {"timestamp": f"0:00 - 0:{random.randint(8,15):02d}", "acao": "Hook + promessa de valor"},
            {"timestamp": f"0:{random.randint(10,20):02d} - 2:00", "acao": random.choice(body)},
            {"timestamp": "2:00 - final", "acao": "Exemplo prático + aplicação na imobiliária"},
        ],
        "thumbnail_hint": "rosto + frase curta + imóvel de fachada atraente",
        "seo_title": tema,
        "seo_description": f"{tema} — guia prático para imobiliárias do litoral paulista.",
        "tags": ["imobiliaria litoral", "corretor de imoveis", "temporada", "praia digital"],
        "call_to_action": random.choice([
            "Baixe material complementar em https://praia.digital",
            "Agende uma conversa rápida pelo WhatsApp",
            "Assista também o vídeo complementar no YouTube"
        ]),
    }
    return roteiro

def build_short_block(idx: int, tema: str) -> dict:
    duracao = random.choice([28, 45, 60])
    hook = random.choice(HOOKS)
    body_line = random.choice(BODY_FRAMES_CURTO)
    roteiro = {
        "canal": random.choice(["Reels", "TikTok"]),
        "tema": tema,
        "duracao": duracao,
        "titulo_sugerido": tema,
        "descricao": f"{tema}\n\nConteúdo direto para sua timeline.",
        "hook": hook,
        "blocos": [
            {"timestamp": f"0:00 - 0:03", "acao": hook},
            {"timestamp": f"0:03 - {format_duration(duracao-6)}", "acao": body_line},
            {"timestamp": f"{format_duration(duracao-6)} - {format_duration(duracao)}", "acao": "CTA final"},
        ],
        "thumbnail_hint": "texto em destaque + pessoa explicando",
        "seo_title": tema,
        "seo_description": f"{tema} — dica prática para imobiliárias e corretores.",
        "tags": ["imoveis", "litoral", "temporada", "praia digital"],
        "call_to_action": "Veja mais estratégias em https://praia.digital"
    }
    return roteiro

def generate_roteiros(days=14):
    lines = [
        "# Roteiro de vídeos diários",
        f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        ""
    ]
    all_roteiros = []
    for d in range(days):
        data = (datetime.now() + timedelta(days=d)).strftime("%d/%m/%Y")
        bloco_longo = build_youtube_block(d, TEMPLATES[0]["temas"][d % len(TEMPLATES[0]["temas"])])
        bloco_curto1 = build_short_block(d, TEMPLATES[1]["temas"][d % len(TEMPLATES[1]["temas"])])
        bloco_curto2 = build_short_block((d + 3), TEMPLATES[2]["temas"][d % len(TEMPLATES[2]["temas"])])
        item = {
            "data": data,
            "dia": d + 1,
            "youtube": bloco_longo,
            "reels": bloco_curto1,
            "tiktok": bloco_curto2
        }
        all_roteiros.append(item)
        lines.extend([
            f"## Dia {d+1} — {data}",
            "",
            "### YouTube",
            f"- Tema: {bloco_longo['tema']}",
            f"- Hook: {bloco_longo['hook']}",
            f"- CTA: {bloco_longo['call_to_action']}",
            "",
            "### Reels",
            f"- Tema: {bloco_curto1['tema']}",
            f"- Hook: {bloco_curto1['hook']}",
            f"- CTA: {bloco_curto1['call_to_action']}",
            "",
            "### TikTok",
            f"- Tema: {bloco_curto2['tema']}",
            f"- Hook: {bloco_curto2['hook']}",
            f"- CTA: {bloco_curto2['call_to_action']}",
            ""
        ])
    os.makedirs(OUT_DIR, exist_ok=True)
    md_path = os.path.join(OUT_DIR, "roteiro-video-diario-gerado.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    json_path = os.path.join(OUT_DIR, "roteiro-video-diario-gerado.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_roteiros, f, ensure_ascii=False, indent=2)
    print(f"Gerado: {md_path}")
    print(f"Gerado: {json_path}")
    return md_path, json_path


if __name__ == "__main__":
    generate_roteiros(days=14)
