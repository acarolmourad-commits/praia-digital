#!/usr/bin/env python3
"""
Expansao D — Landings B2C de DONO do Litoral Norte (Ubatuba/Ilhabela/Caraguatatuba/Sao Sebastiao).
Geram pagina propria do dono com a calculadora embarcada (iframe) + copy de gestao completa.
Reuso o assets/calculadora-widget-standalone.html via iframe (tenant=pd-norte).
Uso: python scripts/gerar_landing_dono_norte.py
"""
import os
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
OUT = os.path.join(REPO, "dono-norte")
CIDADES = {
    "Ubatuba": "ubatuba", "Ilhabela": "ilhabela",
    "Caraguatatuba": "caraguatatuba", "São Sebastião": "sao-sebastiao",
}
CALC = "https://praia.digital/assets/calculadora-widget-standalone.html?tenant=pd-norte"
TODAY = date.today().isoformat()

TPL = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Quanto seu imóvel rende em {cidade} — Praia Digital</title>
<meta name="description" content="Simule o yield de temporada do seu imóvel em {cidade} e descubra como a Praia Digital cuida de TUDO (limpeza, check-in, precificação) enquanto você ganha mais trabalhando zero horas.">
<style>body{{font-family:Arial,sans-serif;max-width:760px;margin:auto;padding:20px;color:#112}}
h1{{color:#0a3a6b;font-size:1.5rem}}p{{line-height:1.6;color:#334}}
.hero{{background:linear-gradient(135deg,#063a5a,#0a3a6b);color:#fff;border-radius:14px;padding:1.6rem;margin-bottom:1.2rem}}
.hero h1{{color:#fff}}.hero p{{color:#cbd5e1}}
iframe{{width:100%;height:680px;border:1px solid #cfe3f5;border-radius:12px}}
.cta{{background:#f0f7ff;border:1px solid #cfe3f5;border-radius:12px;padding:1.2rem;margin-top:1.2rem;text-align:center}}
.cta a{{display:inline-block;background:linear-gradient(90deg,#22d3ee,#0ea5e9);color:#04141f;font-weight:800;padding:.8rem 1.4rem;border-radius:10px;text-decoration:none}}
ul{{color:#334;line-height:1.7}}</style></head>
<body>
<div class="hero"><h1>📈 Quanto seu imóvel rende em {cidade}?</h1>
<p>Simule o yield de temporada da sua casa em {cidade} em 30 segundos. Depois, a Praia Digital cuida de TUDO — limpeza, check-in e precificação dinâmica — enquanto você ganha mais trabalhando zero horas.</p></div>

<iframe src="{calc}" title="Calculadora de Yield — {cidade}"></iframe>

<div class="cta"><h2 style="color:#0a3a6b;margin:.2rem 0 .6rem">Prefere conversar com a gente?</h2>
<p style="color:#334;margin:.3rem 0 .8rem">Abrimos seu WhatsApp direto com nossa equipe em {cidade}.</p>
<a href="https://wa.me/5511954346288?text={wa}" target="_blank">Falar sobre gestão em {cidade} →</a></div>

<h2>Por que Gestão Completa Praia Digital em {cidade}</h2>
<ul>
<li><b>Precificação Dinâmica</b> — diária e ocupação no talo, sem você mexer em nada.</li>
<li><b>Zero horas</b> — cuidamos de limpeza, check-in, check-out e suporte 24h.</li>
<li><b>Mais receita</b> — donos que migram pra gestão profissional aumentam ocupação vs. anúncio solo.</li>
<li><b>Você no controle</b> — relatório mensal de receita e calendário no app.</li>
</ul>
<p style="font-size:.8rem;color:#667">Praia Digital · Gestão de temporada no litoral de SP · {data}</p>
</body></html>"""

def main():
    os.makedirs(OUT, exist_ok=True)
    for cidade, slug in CIDADES.items():
        wa = f"Olá! Simulei o yield do meu imóvel em {cidade} pela Praia Digital e quero saber mais sobre gestão completa."
        html = TPL.format(cidade=cidade, calc=CALC, wa=wa.replace(" ", "%20"), data=TODAY)
        open(os.path.join(OUT, f"dono-{slug}.html"), "w", encoding="utf-8").write(html)
        print(f"Landing dono: {cidade} -> dono-{slug}.html")
    print(f"\n{len(CIDADES)} landings de dono do norte em {OUT}")

if __name__ == "__main__":
    main()
