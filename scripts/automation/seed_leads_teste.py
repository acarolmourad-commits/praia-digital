import csv
from pathlib import Path
from datetime import datetime, timedelta

root = Path("C:/Users/Carolina/praia-digital")
source = root / "docs/sales/parcerias-leads-capturados.csv"

cities = ["Santos", "Guarujá", "São Vicente", "Praia Grande", "Bertioga", "Outra"]
names = [
    ("Ana", "Porto da Lua"), ("Bruno", "Praia Grande Imóveis"), ("Carla", "Costa Verde"),
    ("Diego", "Alpha Imóveis"), ("Elena", "Blue House"), ("Fábio", "Site View"),
    ("Gabi", "Litoral Negócios"), ("Hugo", "Barra Norte"), ("Iris", "Mar Aberto"),
    ("João", "Porto da Lua")
]
messages = [
    "Quero uma parceria para captar mais leads com IA",
    "Temos interesse em automação de atendimento",
    "Quero aumentar vendas no verão",
    "Busco ferramentas gratuitas para começar",
    "Quero reduzir custos de aquisição",
    "Interesse em SEO local",
    "Quero um piloto sem custo",
    "Estamos procurando parceria de tecnologia",
    "Quero atendimento 24h para meus clientes",
    "Busco recomendação automática de imóveis"
]

rows = []
now = datetime.now()
for i, (first, company) in enumerate(names):
    city = cities[i % len(cities)]
    email = f"contato{i+1}@exemplo.com"
    whatsapp = f"(11) 9{1000+i}-{1000+i}"
    ts = (now - timedelta(hours=i*2)).strftime("%Y-%m-%d %H:%M:%S")
    msg = messages[i % len(messages)]
    origem = "site"
    rows.append({
        "Nome da imobiliária": company,
        "Seu nome": first,
        "E-mail comercial": email,
        "WhatsApp": whatsapp,
        "Cidade": city,
        "Mensagem": msg,
        "Timestamp": ts,
        "Origem": origem,
    })

fields = list(rows[0].keys())
with source.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"Seed criado com {len(rows)} leads fictícios em {source}")
