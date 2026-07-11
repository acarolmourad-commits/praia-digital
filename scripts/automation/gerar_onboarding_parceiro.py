#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de onboarding personalizado para novos parceiros.
Entrada: docs/sales/leads-litoral-enriquecido.csv
Saída: docs/materiais/onboarding-parceiro-<id>.html
"""
import os, csv
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEADS_CSV = os.path.join(BASE, "docs", "sales", "leads-litoral-enriquecido.csv")
OUT_DIR = os.path.join(BASE, "docs", "materiais")
os.makedirs(OUT_DIR, exist_ok=True)

FIRST_WEEK = [
    "Dia 1: Apresentação da equipe e alinhamento de metas.",
    "Dia 2: Tour pelo painel e ferramentas gratuitas em https://praia.digital.",
    "Dia 3: Configuração do primeiro anúncio com copy única.",
    "Dia 4: Revisão do funil de atendimento e follow-up.",
    "Dia 5: Primeira medição de resultados: respostas e agendamentos.",
    "Dia 6: Ajustes no script de atendimento e automações.",
    "Dia 7: Revisão semanal e definição de próximos passos."
]


def build_onboarding(lead):
    lead_id = (lead.get("id") or "000").strip()
    nome = lead.get("pessoa_de_contato") or "Novo parceiro"
    imob = lead.get("nome_da_imobiliaria") or "Imobiliária parceira"
    cidade = lead.get("cidade") or "Litoral"
    perfil = lead.get("perfil") or "imobiliaria"
    dor = lead.get("dor_principal") or "aumentar resultados"
    objetivo = lead.get("objetivo_90_dias") or "crescer no litoral"

    week_items = "\n".join([f"<li><strong>{d}</strong></li>" for d in FIRST_WEEK])
    filename = f"onboarding-parceiro-{lead_id}.html"
    path = os.path.join(OUT_DIR, filename)
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Onboarding — {imob} | Praia Digital</title>
<style>
  body {{ font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 20px; }}
  .card {{ max-width: 760px; margin: 0 auto; background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 4px 24px rgba(0,0,0,.05); }}
  .header {{ background: #0d47a1; color: #fff; padding: 18px; border-radius: 12px; margin-bottom: 20px; }}
  .header h1 {{ margin: 0 0 6px; font-size: 20px; }}
  ul {{ line-height: 1.8; padding-left: 18px; }}
  .cta {{ display: inline-block; background: #f57c00; color: #fff; padding: 10px 14px; border-radius: 8px; margin-top: 14px; font-weight: bold; text-decoration: none; }}
  .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #617d8b; }}
  a {{ color: #0d47a1; text-decoration: none; }}
</style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1>Bem-vindo à Praia Digital, {nome}!</h1>
      <div style="font-size:13px;opacity:.9;">Onboarding oficial — {imob} ({cidade})</div>
    </div>
    <p>A partir de agora vamos trabalhar juntos para resolver <strong>{dor}</strong> e alcançar <strong>{objetivo}</strong>.</p>
    <p>Este onboarding cobre a primeira semana do parceiro.</p>
    <p><strong>Perfil:</strong> {perfil}</p>
    <h2>Primeira semana</h2>
    <ul>
      {week_items}
    </ul>
    <p>Acesse já:</p>
    <a class="cta" href="https://acarolmourad-commits.github.io/praia-digital/">Visitar site</a>
    <a class="cta" href="https://praia.digital">Ferramentas gratuitas</a>
    <div class="footer">
      Praia Digital • Proptech Litoral • {datetime.now().strftime('%d/%m/%Y')}
    </div>
  </div>
</body>
</html>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def main():
    if not os.path.exists(LEADS_CSV):
        print(f"Arquivo não encontrado: {LEADS_CSV}")
        print("Gerando onboarding de exemplo...")
        exemplo = {
            "id": "exemplo-001",
            "pessoa_de_contato": "Carlos Mendes",
            "nome_da_imobiliaria": "Imobiliária Litoral Digital",
            "cidade": "Santos",
            "perfil": "imobiliaria",
            "dor_principal": "aumentar captação",
            "objetivo_90_dias": "crescimento de 30% em vendas"
        }
        p = build_onboarding(exemplo)
        print(f"Onboarding de exemplo gerado: {p}")
        return
    rows = []
    with open(LEADS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")
        for r in reader:
            rows.append(r)
    created = []
    for r in rows:
        p = build_onboarding(r)
        created.append(p)
    print(f"Gerados {len(created)} onboardings em {OUT_DIR}")
    for p in created[:5]:
        print(f"- {p}")


if __name__ == "__main__":
    main()
