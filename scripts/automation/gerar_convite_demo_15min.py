#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de convites para demonstração de 15min personalizados por perfil de lead.
Saída: outreach/convites-demo-15min/<perfil>-<cidade>-<nome>.html
"""
import os, csv, random
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEADS_CSV = os.path.join(BASE, "docs", "sales", "leads-litoral-enriquecido.csv")
OUT_DIR = os.path.join(BASE, "outreach", "convites-demo-15min")
os.makedirs(OUT_DIR, exist_ok=True)

PERFIS = {
    "construtora": {
        "titulo": "Demo exclusiva para construtoras do litoral",
        "abertura": "Mostramos como aumentar a captação de lançamentos sem aumentar equipe.",
        "destaques": ["qualificação automática de leads", "avaliação de preço em tempo real", "integração com lançamentos"]
    },
    "imobiliaria": {
        "titulo": "Demo para imobiliárias do litoral paulista",
        "abertura": "Em 15min você vê como automatizar o atendimento e fechar mais vendas na temporada.",
        "destaques": ["follow-up automático", "assistente virtual para compradores", "gestão de temporada"]
    },
    "gestor": {
        "titulo": "Demonstração para gestores imobiliários",
        "abertura": "Apresentamos métricas e automação para decisão rápida.",
        "destaques": ["dashboard de performance", "priorização de leads com IA", "relatórios automáticos"]
    },
    "corretor": {
        "titulo": "Demo rápida para corretores",
        "abertura": "Ferramenta prática para usar no dia a dia do atendimento.",
        "destaques": ["descrição automática de imóveis", "resposta rápida no WhatsApp", "organização de visitas"]
    }
}

def slugify(s):
    return "".join(c if c.isalnum() else "-" for c in s).strip("-").lower()

def build_invite(lead):
    perfil = (lead.get("perfil") or "imobiliaria").strip().lower()
    p = PERFIS.get(perfil, PERFIS["imobiliaria"])
    nome = lead.get("pessoa_de_contato") or "Equipe"
    imob = lead.get("nome_da_imobiliaria") or "Imobiliária"
    cidade = lead.get("cidade") or "Litoral"
    dor = lead.get("dor_principal") or "aumentar vendas"
    slug = f"{slugify(imob)}-{slugify(cidade)}-{perfil}"
    agora = datetime.now().strftime("%d/%m/%Y")
    body = "\n".join([f'<li><strong>{d}</strong></li>' for d in p["destaques"]])
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{p['titulo']} — {imob}</title>
<style>
  body {{ font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 20px; }}
  .card {{ max-width: 720px; margin: 0 auto; background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 4px 24px rgba(0,0,0,.05); }}
  .header {{ background: #0d47a1; color: #fff; padding: 18px; border-radius: 12px; margin-bottom: 20px; }}
  .header h1 {{ margin: 0 0 6px; font-size: 20px; }}
  ul {{ line-height: 1.8; padding-left: 18px; }}
  .cta {{ display: inline-block; background: #f57c00; color: #fff; padding: 12px 16px; border-radius: 8px; margin-top: 14px; font-weight: bold; text-decoration: none; }}
  .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #617d8b; }}
  a {{ color: #0d47a1; text-decoration: none; }}
</style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1>{p['titulo']}</h1>
      <div style="font-size:13px;opacity:.9;">Convite para demonstração de 15 minutos</div>
    </div>
    <p>Olá, <strong>{nome}</strong>!</p>
    <p>{p['abertura']}</p>
    <p>Hoje você vai ver na prática como resolver <strong>{dor}</strong> com fluxo simples, sem fricção e sem investimento inicial.</p>
    <p>Nesta demo você verá:</p>
    <ul>
      {body}
    </ul>
    <p>Agende agora o horário que funciona melhor para você.</p>
    <a class="cta" href="mailto:comercial@praia.digital?subject=Desejo agendar uma demo de 15min — {imob}&body=Olá, sou {nome} da {imob} em {cidade}. Gostaria de agendar a demonstração de 15min.">Quero agendar minha demo</a>
    <p style="margin-top:14px; font-size:13px; color:#374a5e;">Duração: 15 minutos · Sem compromisso · Foco no seu resultado no litoral paulista.</p>
    <div class="footer">
      Praia Digital · Proptech Litoral · {agora}<br>
      Site: <a href="https://acarolmourad-commits.github.io/praia-digital/">Praia Digital</a> | Ferramentas: <a href="https://praia.digital">praia.digital</a>
    </div>
  </div>
</body>
</html>"""
    path = os.path.join(OUT_DIR, f"{slug}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def main():
    if not os.path.exists(LEADS_CSV):
        print(f"Leads CSV não encontrado: {LEADS_CSV}")
        return
    rows = []
    with open(LEADS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")
        for r in reader:
            rows.append(r)
    created = []
    for r in rows:
        p = build_invite(r)
        created.append(p)
    print(f"Gerados {len(created)} convites em {OUT_DIR}")
    for p in created[:5]:
        print(f"- {p}")


if __name__ == "__main__":
    main()
