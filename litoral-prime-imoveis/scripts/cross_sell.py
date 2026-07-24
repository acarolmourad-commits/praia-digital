"""
Litoral Prime — cross-sell automático por tipo de interesse.
Uso standalone:
    python scripts/cross_sell.py
Uso como módulo:
    from scripts.cross_sell import generate_cross_sell
    generate_cross_sell(Path("outreach/lotes-prontos/lote-001-leads-sanitizado.csv"), Path("outreach/do-dia/2026-07-23"))
"""
from pathlib import Path
import csv, datetime

CROSS_SELL_MAP = {
    "compra": ["Avaliação", "Descrição com IA", "Consultoria Proptech"],
    "aluguel": ["Captação Digital", "Automação", "SEO Local"],
    "venda": ["Avaliação", "Captação Digital", "Descrição com IA"],
    "avaliação": ["Consultoria Proptech", "Descrição com IA"],
    "captação": ["Automação", "SEO Local", "Descrição com IA"],
    "consultoria proptech": ["Automação", "Captação Digital"],
    "automação": ["Captação Digital", "Consultoria Proptech"],
    "seo local": ["Captação Digital", "Consultoria Proptech"],
}


def build_message(nome: str, tipo: str, cidade: str, extras: list[str]) -> str:
    if not extras:
        return ""
    extra_str = ", ".join(extras[:2])
    return (
        f"{nome}, além de {tipo.lower()} em {cidade}, temos {extra_str} "
        f"que ajudam a vender/alugar mais rápido. Quer que eu envie detalhes?"
    )


def generate_cross_sell(sanitized_path: Path, out_dir: Path):
    with sanitized_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    out_path = out_dir / "cross-sell.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["nome", "telefone", "cidade_interesse", "tipo_interesse", "cross_sell", "mensagem", "data_acao"],
        )
        writer.writeheader()
        for r in rows:
            tipo = r["tipo_interesse"].lower().strip()
            extras = CROSS_SELL_MAP.get(tipo, ["Avaliação", "Descrição com IA"])
            writer.writerow(
                {
                    "nome": r["nome"],
                    "telefone": r["telefone"],
                    "cidade_interesse": r["cidade_interesse"],
                    "tipo_interesse": r["tipo_interesse"],
                    "cross_sell": ", ".join(extras),
                    "mensagem": build_message(r["nome"], r["tipo_interesse"], r["cidade_interesse"], extras),
                    "data_acao": datetime.date.today().isoformat(),
                }
            )
    print(f"Gerado: {out_path}")


def run():
    from pathlib import Path
    base = Path(__file__).resolve().parent.parent
    lotes_dir = base / "outreach" / "lotes-prontos"
    out_dir = base / "outreach" / "do-dia" / datetime.date.today().isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    candidates = sorted(lotes_dir.glob("*-sanitizado.csv"), key=lambda p: p.stat().st_size, reverse=True)
    if not candidates:
        raise SystemExit("Nenhum lote sanitizado encontrado.")
    generate_cross_sell(candidates[0], out_dir)


if __name__ == "__main__":
    run()
