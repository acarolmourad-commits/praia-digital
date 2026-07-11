#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de calendário automático de conteúdo 30 dias.
Alinha: blog SEO, roteiros de vídeo, posts sociais e CTAs para parcerias/ferramentas.
Saída: docs/materiais/calendario-conteudo-30dias-YYYY-MM-DD.md
"""
import os
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(BASE, "docs", "materiais")
os.makedirs(OUT_DIR, exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")
OUT = os.path.join(OUT_DIR, f"calendario-conteudo-30dias-{TODAY}.md")

BLOG_TEMAS = [
    "SEO local para imobiliárias do litoral",
    "Follow-up automático no WhatsApp",
    "Captação de imóveis na baixa temporada",
    "Avaliação automática de preço de imóveis",
    "Gestão de temporada para corretores",
    "Indicadores de vendas no litoral",
    "Assistente virtual para compradores",
    "Geração de descrições de anúncios com IA",
    "Reativação de leads frios",
    "Google Business Profile para imobiliárias",
    "LGPD no atendimento imobiliário",
    "Plano de ação de 30 dias para imobiliárias",
    "SEO local em 3 passos",
    "Checklist antes de anunciar no verão",
    "Como escolher ferramentas para corretores",
    "Follow-up que não parece insistente",
    "Predição de vendas no litoral",
    "Captação sem custo para imobiliárias",
    "Modelo econômico de temporada",
    "Negociação de imóveis no litoral",
    "ROI de automação para imobiliárias",
    "Erros na captação de imóveis",
    "Visitantes que não fecham: causas e soluções",
    "Prospecção omnichannel para corretores",
    "Geração de leads qualificados"
]

VIDEO_TEMAS = [
    "1 erro que custa vendas no litoral",
    "Ferramenta grátis para avaliar imóvel",
    "Copy que converte para temporada",
    "Prompt de IA para descrição de imóvel",
    "Follow-up que não parece insistente",
    "5 segundos que fazem o cliente responder",
    "Número que você deve pedir no primeiro contato",
    "SEO local para corretores em 3 passos",
    "Melhor horário para enviar WhatsApp de venda",
    "Hook de abertura para visita de imóvel",
    "Checklist de visita rápida para compradores",
    "Follow-up no Instagram para temporada",
    "Comparação de bairros do litoral em 60s",
    "Otimização para marketplace de temporada",
    "Modelo de proposta pronta para imobiliárias"
]

SOCIAL_TEMPLATES = [
    "Dica rápida: {tema}",
    "Pare de cometer esse erro no litoral",
    "Ferramenta grátis: {tema}",
    "ROI de {tema}",
    "Checklist: {tema}",
    "Case prático: {tema}",
    "Mito: {tema}",
    "Pergunta: {tema}?",
    "3 passos: {tema}",
    "Automação: {tema}"
]

CTA_BLOG = "Ferramentas gratuitas em https://praia.digital | Quer parceria? Fale com a Praia Digital"
CTA_SOCIAL = "Veja mais em https://praia.digital | Parcerias: https://acarolmourad-commits.github.io/praia-digital/"


def build_calendar():
    lines = ["# Calendário de Conteúdo — 30 dias", "", f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ""]
    for d in range(30):
        data = (datetime.now() + timedelta(days=d)).strftime("%d/%m/%Y")
        blog_tema = BLOG_TEMAS[d % len(BLOG_TEMAS)]
        video_tema = VIDEO_TEMAS[d % len(VIDEO_TEMAS)]
        social_tema = SOCIAL_TEMPLATES[d % len(SOCIAL_TEMPLATES)].format(tema=blog_tema.split(":")[0] if ":" in blog_tema else blog_tema)
        lines.extend([
            f"## Dia {d+1} — {data}",
            "",
            "- **Blog SEO:**",
            f"  - Título: {blog_tema}",
            f"  - CTA: {CTA_BLOG}",
            "",
            "- **Vídeo (YouTube/Reels/TikTok):**",
            f"  - Tema: {video_tema}",
            "",
            "- **Post social:**",
            f"  - Texto: {social_tema}",
            f"  - CTA: {CTA_SOCIAL}",
            ""
        ])
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Gerado: {OUT}")
    return OUT


if __name__ == "__main__":
    build_calendar()
