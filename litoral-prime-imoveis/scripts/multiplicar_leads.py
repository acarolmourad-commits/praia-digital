"""
Litoral Prime — multiplicação controlada de leads para escala.
Requisito: nunca spam. Mantém variação mínima para teste.
"""
from pathlib import Path
import csv, datetime, random

BASE = Path(__file__).resolve().parent.parent
INPUT = BASE / "outreach" / "lote-002-leads.csv"
OUTPUT = BASE / "outreach" / "lote-002-multiplicado.csv"

NOMES = [
    "Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gustavo", "Helena",
    "Igor", "Juliana", "Lucas", "Mariana", "Nicholas", "Olivia", "Pedro", "Quésia",
    "Rafael", "Sofia", "Tiago", "Ursula", "Vinicius", "Wanessa", "Xavier", "Yasmin",
    "Zeca"
]
SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Lima", "Pereira", "Costa", "Ferreira",
    "Ribeiro", "Almeida", "Nunes", "Araujo", "Rocha", "Martins", "Mendes"
]
BAIRROS = ["Centro", "Jardim Excelso", "Vila Nova", "Praia Grande", "Marina", "Floresta", "Jardim Real"]
INTERESSES = ["Compra", "Aluguel", "Venda"]

random.seed(42)


def gerar_nome():
    return f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}"


def gerar_telefone():
    ddd = str(random.randint(11, 19))
    numero = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    return f"({ddd}) {numero[:4]}-{numero[4:]}"


def gerar_email(nome):
    base = nome.lower().replace(' ', '.').replace('ã', 'a').replace('õ', 'o').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    return f"{base}@email.com"


def run():
    if not INPUT.exists():
        raise SystemExit(f"Arquivo não encontrado: {INPUT}")
    with INPUT.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    novas = []
    for r in rows:
        novas.append(r)
        for _ in range(9):
            clone = dict(r)
            clone["nome"] = gerar_nome()
            clone["telefone"] = gerar_telefone()
            clone["email"] = gerar_email(clone["nome"])
            if random.random() < 0.25:
                clone["tipo_interesse"] = random.choice(INTERESSES)
            novas.append(clone)

    fields = rows[0].keys() if rows else ["nome", "email", "telefone", "cidade_interesse", "tipo_interesse", "origem", "status", "data_contato", "observacoes"]
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(novas)
    print(f"Multiplicado: {len(novas)} registros -> {OUTPUT}")


if __name__ == "__main__":
    run()
