"""
Litoral Prime — sugestão automática de follow-up baseada em score.
Saída: outreach/do-dia/<data>/follow-up-sugestoes.csv
"""
from pathlib import Path
import csv, datetime

BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "outreach" / "do-dia" / datetime.date.today().isoformat()
OUT_DIR.mkdir(parents=True, exist_ok=True)

PRIORITIZED = OUT_DIR / "pronto-disparo-priorizado.csv"
OUT_FILE = OUT_DIR / "follow-up-sugestoes.csv"


def classify(score: int) -> str:
    if score >= 60:
        return "alto"
    if score >= 40:
        return "medio"
    return "baixo"


def window(stage: str, score: int) -> str:
    if score >= 60:
        return "até 24h"
    if score >= 40:
        return "24h a 72h"
    return "7 dias"


def next_message(r) -> str:
    s = r.get("estagio", "").lower()
    nome = r.get("nome", "")
    cidade = r.get("cidade_interesse", "")
    tipo = r.get("tipo_interesse", "")
    if s == "primeiro_contato":
        return f"{nome}, lembrete: temos opções de {tipo} em {cidade} alinhadas com sua busca. Quer que eu envie a pré-seleção?"
    if s == "oferta":
        return f"{nome}, seguimos com a pré-seleção de {tipo} em {cidade}. Quer agendar uma visita?"
    return f"{nome}, sem resposta ainda sobre {tipo} em {cidade}. Posso reenviar opções atualizadas?"


def run():
    if not PRIORITIZED.exists():
        raise SystemExit("pronto-disparo-priorizado.csv não encontrado. Rode o runner primeiro.")
    with PRIORITIZED.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit("Arquivo de priorizados vazio.")
    fields = list(rows[0].keys())
    for r in rows:
        score = int(r.get("score", 0) or 0)
        r["classificacao"] = classify(score)
        r["janela_followup"] = window(r.get("estagio", ""), score)
        r["sugestao_proxima_mensagem"] = next_message(r)
    out_fields = fields + ["classificacao", "janela_followup", "sugestao_proxima_mensagem"]
    with OUT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Gerado: {OUT_FILE} ({len(rows)} sugestões de follow-up)")


if __name__ == "__main__":
    run()
