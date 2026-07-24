"""
Litoral Prime — follow-up do lote sanitizado.
Gera arquivos CSV geracao por estagio: primeiro_contato, reengajamento, oferta.
"""
from pathlib import Path
import csv, datetime

BASE = Path(__file__).resolve().parent.parent
INPUT = BASE / "outreach" / "lote-001-sanitizado.csv"
OUT_DIR = BASE / "outreach" / "followups"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def build_first(name: str, interesse: str, cidade: str):
    return (
        f"Olá, {name}! Tudo bem?\n"
        f"Vi que você tem interesse em {interesse.lower()} na região de {cidade}.\n"
        f"Quer que eu envie 3 opções compatíveis com o seu perfil?"
    )


def build_reengagement(name: str):
    return (
        f"Olá, {name}! Lembrete rápido: a Litoral Prime Imóveis tem novas opções no litoral de SP.\n"
        f"Quer que eu envie as melhores oportunidades desta semana?"
    )


def build_offer(name: str, cidade: str, tipo: str):
    return (
        f"{name}, selecionei {tipo.lower()}s exclusivos em {cidade}.\n"
        f"Se quiser, envio a pré‑seleção agora por aqui."
    )


STAGE_MESSAGES = {
    "primeiro_contato": build_first,
    "reengajamento": build_reengagement,
    "oferta": build_offer,
}


def run():
    if not INPUT.exists():
        raise SystemExit(f"Execute sanitize antes: {INPUT}")
    with INPUT.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for stage in STAGE_MESSAGES.keys():
        path = OUT_DIR / f"lote-001-{stage}.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "nome", "telefone", "cidade_interesse", "tipo_interesse",
                    "estagio", "mensagem", "data_geracao"
                ],
            )
            writer.writeheader()
            for r in rows:
                writer.writerow(
                    {
                        "nome": r["nome"],
                        "telefone": r["telefone"],
                        "cidade_interesse": r["cidade_interesse"],
                        "tipo_interesse": r["tipo_interesse"],
                        "estagio": stage,
                        "mensagem": STAGE_MESSAGES[stage](r["nome"], r["cidade_interesse"], r["tipo_interesse"]) if stage == "primeiro_contato"
                        else STAGE_MESSAGES[stage](r["nome"], r["cidade_interesse"], r["tipo_interesse"]) if stage == "oferta"
                        else STAGE_MESSAGES[stage](r["nome"]),
                        "data_geracao": datetime.date.today().isoformat(),
                    }
                )
        print(f"Gerado: {path}")

if __name__ == "__main__":
    run()
