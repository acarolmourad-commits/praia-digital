"""
Litoral Prime — calibra o scoring com base em metricas.csv.
Compara score vs taxa de resposta real e ajusta pesos automaticamente.
Saída: scripts/scoring_weights.json
"""
from pathlib import Path
import csv, json, datetime

BASE = Path(__file__).resolve().parent.parent
METRICAS = BASE / "outreach" / "metricas.csv"
WEIGHTS_FILE = BASE / "scripts" / "scoring_weights.json"

DEFAULT_WEIGHTS = {
    "tipo_interesse": {"venda": 30, "avaliação": 30, "consultoria proptech": 40, "captação": 20, "aluguel": 15, "compra": 10, "default": 5},
    "cidade_interesse": {"santos": 20, "guarujá": 20, "praia grande": 20, "bertioga": 25, "itanhaém": 10, "mongaguá": 10, "são vicente": 10, "peruíbe": 10},
    "origem": {"site": 15, "indicacao": 20, "default": 0},
    "telefone": 10,
    "email": 5,
}


def load_weights():
    if WEIGHTS_FILE.exists():
        return json.loads(WEIGHTS_FILE.read_text(encoding="utf-8"))
    return DEFAULT_WEIGHTS.copy()


def save_weights(weights):
    WEIGHTS_FILE.write_text(json.dumps(weights, ensure_ascii=False, indent=2), encoding="utf-8")


def score_with_weights(r, weights):
    score = 0
    tipo = (r.get("tipo_interesse") or r.get("tipo") or "").strip().lower()
    cidade = (r.get("cidade_interesse") or r.get("cidade") or "").strip().lower()
    origem = (r.get("origem") or "site").strip().lower()

    tipo_map = weights.get("tipo_interesse", {})
    score += tipo_map.get(tipo, tipo_map.get("default", 0))

    cidade_map = weights.get("cidade_interesse", {})
    score += cidade_map.get(cidade, 0)

    origem_map = weights.get("origem", {})
    score += origem_map.get(origem, origem_map.get("default", 0))

    if r.get("telefone"):
        score += weights.get("telefone", 0)
    if r.get("email"):
        score += weights.get("email", 0)
    return score


def calibrate():
    if not METRICAS.exists():
        print("metricas.csv não encontrado. Sem dados para calibrar.")
        return
    with METRICAS.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("metricas.csv vazio.")
        return

    # Separa respondidos vs não respondidos por cidade/tipo
    stats = {}
    for r in rows:
        tipo = (r.get("tipo") or r.get("tipo_interesse") or "").strip().lower()
        cidade = (r.get("cidade") or r.get("cidade_interesse") or "").strip().lower()
        status = (r.get("status") or "").strip().lower()
        key = (tipo, cidade)
        stats.setdefault(key, {"respondido": 0, "total": 0})
        stats[key]["total"] += 1
        if "respondido" in status or "interessado" in status:
            stats[key]["respondido"] += 1

    # Pesos atuais
    weights = load_weights()
    tipo_map = weights.setdefault("tipo_interesse", {})
    cidade_map = weights.setdefault("cidade_interesse", {})
    origem_map = weights.setdefault("origem", {})

    # Ajuste: aumento/diminui peso por taxa de resposta
    for (tipo, cidade), s in stats.items():
        rate = s["respondido"] / s["total"] if s["total"] else 0
        # Se taxa baixa (<30%) reduz peso; se alta (>60%) aumenta peso
        tipo_bonus = 1
        cidade_bonus = 1
        if rate < 0.3:
            tipo_bonus = 0.7
            cidade_bonus = 0.85
        elif rate > 0.6:
            tipo_bonus = 1.4
            cidade_bonus = 1.2

        cur = tipo_map.get(tipo, 0) or 0
        tipo_map[tipo] = max(1, int(cur * tipo_bonus))

        cur = cidade_map.get(cidade, 0) or 0
        cidade_map[cidade] = max(1, int(cur * cidade_bonus))

    save_weights(weights)
    print(f"Pesos calibrados e salvos em {WEIGHTS_FILE}")
    print(json.dumps(weights, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    calibrate()
