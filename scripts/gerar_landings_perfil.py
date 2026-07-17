#!/usr/bin/env python3
"""
Landings por Perfil — Hermes (Praia Digital).
Gera 1 landing por persona da plataforma de Inteligencia Imobiliaria, cada uma
falando so com aquele perfil e acionando a ferramenta certa. Reusa padrao das
landings norte (iframe da calculadora ou link direto p/ ferramenta).
Uso: python scripts/gerar_landings_perfil.py
"""
import os
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
OUT = os.path.join(REPO, "perfis")
CALC = "https://praia.digital/assets/calculadora-widget-standalone.html?tenant=pd-norte"
POS = "https://praia.digital/assets/posicionamento-inteligencia-imobiliaria.html"
TODAY = date.today().isoformat()

PERFIS = {
    "comprador": {
        "titulo": "Comprador do 1º Imóvel",
        "sub": "Wa sua casa certa sem sustos — com inteligência, não feeling.",
        "dor": "Medo de pagar caro, de escolher bairro errado, de não saber se o financiamento fecha.",
        "ganho": "Busca Inteligente filtra por orçamento + Simulador de Financiamento mostra as parcelas reais. Você decide sabendo.",
        "ferramenta_nome": "Busca Inteligente + Simulador de Financiamento",
        "ferramenta_url": POS,
        "cta": "Quero simular meu financiamento",
    },
    "investidor": {
        "titulo": "Investidor Imobiliário",
        "sub": "Retorno embasado em dado, não em palpite.",
        "dor": "Dúvida se o imóvel valoriza, se a temporada paga o financiamento, onde está o melhor ROI.",
        "ganho": "Calculadora de ROI + Análise de Rental Yield por CEP mostram exatamente onde seu dinheiro rende mais.",
        "ferramenta_nome": "Calculadora de ROI + Análise de Rental Yield",
        "ferramenta_url": CALC,
        "cta": "Simular ROI do meu imóvel",
    },
    "proprietario": {
        "titulo": "Proprietário Anuncia Sozinho (Airbnb/Booking)",
        "sub": "Ganhe mais trabalhando zero horas.",
        "dor": "Perde horas com limpeza, check-in e precificação errada. Dias vazios custam seu lucro.",
        "ganho": "Gestão Completa + Precificação Dinâmica assumem TUDO. Você lucra mais e não levanta um dedo.",
        "ferramenta_nome": "Calculadora de ROI + Gestão Completa",
        "ferramenta_url": CALC,
        "cta": "Simular meu yield",
    },
    "corretor": {
        "titulo": "Corretor",
        "sub": "Capture mais e feche mais rápido, com IA do seu lado.",
        "dor": "Gerar leads quentes, escrever anúncios que convertem, triar quem tem intimidade.",
        "ganho": "Gerador de Descrições + Qualificador de Leads fazem o trabalho pesado. Você foca no fechamento.",
        "ferramenta_nome": "Gerador de Descrições + Qualificador de Leads",
        "ferramenta_url": "https://praia.digital/docs/ferramentas/qualificador-leads.json",
        "cta": "Ver o Qualificador Hermes",
    },
    "imobiliaria": {
        "titulo": "Imobiliária",
        "sub": "Parceira, não concorrente. Capte mais proprietários com nossa marca no seu site.",
        "dor": "Captação cara, ocupação baixa da carteira, operação de temporada complexa.",
        "ganho": "White-label: Calculadora no SEU site (lead 100% seu) + Gestão Completa 70/30. Inventário recorrente.",
        "ferramenta_nome": "Calculadora White-label + Gestão Completa",
        "ferramenta_url": "https://praia.digital/docs/product/ranking-whitelabel.html",
        "cta": "Ver ranking de ativação",
    },
    "construtora": {
        "titulo": "Construtora / Incorporadora",
        "sub": "Qualifique seus interessados e acelere vendas.",
        "dor": "Leads frios, funil de vendas manual, dificuldade de converter quem apareceu.",
        "ganho": "Busca Inteligente + Qualificador de Leads no seu funil: lead certo, no momento certo.",
        "ferramenta_nome": "Busca Inteligente + Qualificador de Leads",
        "ferramenta_url": "https://praia.digital/docs/ferramentas/qualificador-leads.json",
        "cta": "Integrar Qualificador",
    },
    "adm_temporada": {
        "titulo": "Administrador de Temporada / Anfitrião Pro",
        "sub": "Suba ocupação e inventário sem virar escravo da operação.",
        "dor": "Pricing manual, ocupação baixa fora de pico, dificuldade de captar mais imóveis.",
        "ganho": "Precificação Dinâmica (PriceLabs/Stays) + White-label para captar proprietários no seu canal.",
        "ferramenta_nome": "Análise de Rental Yield + White-label",
        "ferramenta_url": CALC,
        "cta": "Simular yield da minha carteira",
    },
    "turista": {
        "titulo": "Turista que quer Investir no Litoral",
        "sub": "O imóvel das férias que se paga no resto do ano.",
        "dor": "Se apaixonou pela praia e quer saber se vale como investimento.",
        "ganho": "Busca Inteligente + ROI de temporada mostram o imóvel que rende nas férias e aluga no resto do ano.",
        "ferramenta_nome": "Busca Inteligente + Calculadora de ROI",
        "ferramenta_url": CALC,
        "cta": "Simular ROI de imóvel de férias",
    },
}

def landing(p, d):
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{d['titulo']} — Praia Digital</title>
<meta name="description" content="{d['sub']}">
<style>body{{font-family:Arial,sans-serif;max-width:720px;margin:auto;padding:20px;color:#112}}
h1{{color:#0a3a6b;font-size:1.7rem}}p{{line-height:1.6;color:#334}}
.hero{{background:linear-gradient(135deg,#063a5a,#0a3a6b);color:#fff;border-radius:14px;padding:1.6rem;margin-bottom:1.2rem}}
.hero h1{{color:#fff}}.hero p{{color:#cbd5e1}}
.card{{background:#f0f7ff;border:1px solid #cfe3f5;border-radius:12px;padding:1.2rem;margin:1rem 0;line-height:1.7}}
.card b{{color:#0a3a6b}}.cta{{text-align:center;margin-top:1.2rem}}
.cta a{{display:inline-block;background:linear-gradient(90deg,#22d3ee,#4ade80);color:#04141f;font-weight:800;padding:.8rem 1.4rem;border-radius:10px;text-decoration:none}}
small{{color:#667}}</style></head><body>
<div class="hero"><h1>🧠 {d['titulo']}</h1><p>{d['sub']}</p></div>
<div class="card"><b>Sua dor:</b> {d['dor']}</div>
<div class="card"><b>O que a Praia Digital resolve:</b> {d['ganho']}</div>
<div class="cta"><a href="{d['ferramenta_url']}">{d['cta']} →</a></div>
<p style="font-size:.8rem;color:#667">Praia Digital · 1ª Plataforma Brasileira de Inteligência Imobiliária · {p}</p>
</body></html>"""

def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, d in PERFIS.items():
        open(os.path.join(OUT, f"perfil-{slug}.html"), "w", encoding="utf-8").write(landing(TODAY, d))
        print(f"Landing perfil: {slug} -> perfil-{slug}.html")
    print(f"\n{len(PERFIS)} landings de perfil em {OUT}")

if __name__ == "__main__":
    main()
