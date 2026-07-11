#!/usr/bin/env python3
"""
Simula motor de resposta automática por IA para WhatsApp/e-mail.
Classifica intenção do lead a partir de texto livre e sugere a próxima ação ideal.
Entrada: docs/sales/respostas-recebidas-simuladas.csv (pode ser substituído por entradas reais)
Saída: docs/sales/resposta-automatica-YYYY-MM-DD.md
"""
import collections
from pathlib import Path
from datetime import datetime

BASE = Path("C:/Users/Carolina/praia-digital")
TODAY = datetime.now().strftime("%Y-%m-%d")
OUTPUT = BASE / f"docs/sales/resposta-automatica-{TODAY}.md"
SAMPLE = BASE / "docs/sales/respostas-recebidas-simuladas.csv"
MASTER = BASE / "docs/sales/leads-litoral-enriquecido.csv"

PALAVRAS_POSITIVAS = {"sim", "quero", "ok", "vamos", "pode", "aceito", "agendar", "demo", "onboarding", "participar"}
PALAVRAS_NEGATIVAS = {"nao", "não", "agora nao", "depois", "sem interesse", "nao tenho verba", "nao quero"}
PALAVRAS_OBJECAO = {"já tenho", "ferramenta", "custo", "verba", "tempo", "consultar", "sócio", "gestor", "orçamento", "preco", "preço"}

def classificar(texto: str) -> str:
    t = (texto or "").lower()
    if any(p in t for p in PALAVRAS_OBJECAO):
        return "Objeção"
    if any(p in t for p in PALAVRAS_POSITIVAS):
        return "Interesse positivo"
    if any(p in t for p in PALAVRAS_NEGATIVAS):
        return "Interesse negativo"
    return "Indefinido"

def proxima_acao(classe: str) -> str:
    if classe == "Interesse positivo":
        return "Agendar demo de 15 minutos e enviar onboarding simplificado."
    if classe == "Objeção":
        return "Enviar resposta padrão para objeção + case curto."
    if classe == "Interesse negativo":
        return "Back-off 30 dias + reenvio com novidade."
    return "Follow-up D3: pedir 1 palavra sobre o interesse."

def gerar():
    linhas = [
        f"# Resposta automática — {TODAY}",
        "",
        "Classificação de intenção e próxima ação por lead.",
        "",
    ]
    count = collections.Counter()
    exemplos = []

    if SAMPLE.exists():
        import csv
        rows = list(csv.DictReader(SAMPLE.open(encoding="utf-8", errors="ignore")))
        for r in rows:
            texto = r.get("resposta", "")
            classe = classificar(texto)
            count[classe] += 1
            exemplos.append((r.get("lead_id", ""), classe, texto))
    else:
        exemplos = [
            ("001", "Interesse positivo", "Quero agendar a demo amanhã"),
            ("002", "Objeção", "Já tenho ferramenta, mas quero comparar"),
            ("003", "Interesse negativo", "Agora não, depois pode ser"),
        ]
        for _, classe, _ in exemplos:
            count[classe] += 1

    linhas.append("## Resumo")
    for classe, qtd in sorted(count.items(), key=lambda x: -x[1]):
        linhas.append(f"- {classe}: {qtd}")
    linhas.append("")
    linhas.append("## Detalhamento")
    linhas.append("| Lead | Intenção | Próxima ação |")
    linhas.append("|------|----------|--------------|")
    for lead_id, classe, texto in exemplos:
        linhas.append(f"| {lead_id} | {classe} | {proxima_acao(classe)} |")

    out = "\n".join(linhas) + "\n"
    OUTPUT.write_text(out, encoding="utf-8")
    print(f"Gerado: {OUTPUT}")
    for classe, qtd in sorted(count.items(), key=lambda x: -x[1]):
        print(f"- {classe}: {qtd}")

if __name__ == "__main__":
    gerar()
