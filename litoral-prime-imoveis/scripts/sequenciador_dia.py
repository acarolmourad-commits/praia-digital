"""
Litoral Prime — sequenciador do dia: gera ordem sugerida de contato por score e janela de follow-up.
Entrada: outreach/do-dia/<data>/pronto-disparo-priorizado.csv
Saída: outreach/do-dia/<data>/sequencia.csv
"""
from pathlib import Path
import csv, datetime

BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "outreach" / "do-dia" / datetime.date.today().isoformat()
PRIORIZED = OUT_DIR / "pronto-disparo-priorizado.csv"
OUT = OUT_DIR / "sequencia.csv"


def time_window(score: int, classification: str) -> str:
    if classification == "alto" or score >= 60:
        return "09:00 - 12:00"
    if score >= 40:
        return "12:00 - 15:00"
    return "15:00 - 18:00"


def suggested_next(r: dict) -> str:
    s = (r.get("estagio", "") or "").lower()
    nome = r.get("nome", "")
    tipo = r.get("tipo_interesse", "")
    cidade = r.get("cidade_interesse", "")
    if s == "primeiro_contato":
        return f"Mensagem inicial personalizada para {nome} sobre {tipo} em {cidade}"
    if s == "oferta":
        return f"Enviar pré-seleção de {tipo} em {cidade} e propor visita"
    if s == "cross-sell":
        return f"Oferecer serviço complementar: {r.get('cross_sell', '')}"
    return f"Follow-up leve para {nome} sobre {tipo}"


def run():
    if not PRIORIZED.exists():
        raise SystemExit("pronto-disparo-priorizado.csv não encontrado. Rode o runner primeiro.")
    with PRIORIZED.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: int(r.get("score", 0) or 0), reverse=True)
    fieldnames = list(rows[0].keys())
    for idx, r in enumerate(rows, 1):
        r["ordem"] = idx
        r["janela_contato"] = time_window(int(r.get("score", 0) or 0), (r.get("classificacao", "") or "").lower())
        r["acao_sugerida"] = suggested_next(r)
        r["canal_sugerido"] = "whatsapp"
    out_fields = fieldnames + ["ordem", "janela_contato", "acao_sugerida", "canal_sugerido"]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Gerado: {OUT} ({len(rows)} contatos sequenciados)")


if __name__ == "__main__":
    run()
