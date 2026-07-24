"""
Litoral Prime — gera CSV de disparo pronto, com link direto do WhatsApp por lead, sem duplicatas.
Saída: outreach/do-dia/<data>/pronto-disparo.csv
"""
from pathlib import Path
import csv, datetime

BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "outreach" / "do-dia" / datetime.date.today().isoformat()
OUT_DIR.mkdir(parents=True, exist_ok=True)

WHATSAPP_NUMBER = "5511954346288"

MESSAGE_TEMPLATES = {
    "primeiro_contato": "Olá, {nome}! Tudo bem? Vi que você tem interesse em {tipo_interesse} na região de {cidade_interesse}. Quer que eu envie 3 opções compatíveis com o seu perfil?",
    "reengajamento": "Olá, {nome}! Lembrete rápido: a Litoral Prime Imóveis tem novas opções no litoral de SP. Quer que eu envie as melhores oportunidades desta semana?",
    "oferta": "{nome}, selecionei {tipo_interesse.lower()}s exclusivos em {cidade_interesse}. Se quiser, envio a pré-seleção agora por aqui.",
    "cross-sell": "{nome}, além de {tipo_interesse} em {cidade_interesse}, temos {cross_sell} que ajudam a vender/alugar mais rápido. Quer que eu envie detalhes?",
}


def encode_message(message: str) -> str:
    return (
        message.replace(" ", "%20")
        .replace(",", "%2C")
        .replace("!", "%21")
        .replace("?", "%3F")
        .replace("á", "%C3%A1").replace("é", "%C3%A9").replace("í", "%C3%AD").replace("ó", "%C3%B3").replace("ú", "%C3%BA")
        .replace("ã", "%C3%A3").replace("õ", "%C3%B5").replace("â", "%C3%A2").replace("ê", "%C3%AA").replace("ô", "%C3%B4")
    )


def build_link(phone: str, message: str) -> str:
    digits = "".join(ch for ch in phone if ch.isdigit())
    if not digits.startswith("55"):
        digits = "55" + digits
    return f"https://wa.me/{digits}?text={encode_message(message)}"


def run():
    generated = []
    seen_keys = set()
    for stage in ["primeiro_contato", "reengajamento", "oferta", "cross-sell"]:
        src = OUT_DIR / f"{stage}.csv"
        if not src.exists():
            continue
        with src.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        for r in rows:
            template = MESSAGE_TEMPLATES.get(stage, "")
            try:
                message = template.format(**r)
            except Exception:
                message = template
            nome = (r.get("nome") or "").strip()
            telefone = (r.get("telefone") or "").strip()
            key = (stage, telefone)
            if telefone and key not in seen_keys:
                seen_keys.add(key)
                generated.append({
                    "nome": nome,
                    "telefone": telefone,
                    "cidade_interesse": r.get("cidade_interesse", ""),
                    "tipo_interesse": r.get("tipo_interesse", ""),
                    "estagio": stage,
                    "mensagem": message,
                    "whatsapp_link": build_link(telefone, message),
                    "data_acao": r.get("data_acao", datetime.date.today().isoformat()),
                })

    out = OUT_DIR / "pronto-disparo.csv"
    if not generated:
        raise SystemExit("Nenhum CSV gerado para o dia encontrado. Rode o runner primeiro.")
    fieldnames = ["nome", "telefone", "cidade_interesse", "tipo_interesse", "estagio", "mensagem", "whatsapp_link", "data_acao"]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(generated)
    print(f"Gerado: {out} ({len(generated)} contatos prontos para disparo)")

    # Pivot: gera versão priorizada se o runner de scoring estiver disponível
    try:
        from lead_scoring import score_row
        scored = []
        for r in generated:
            r["score"] = score_row(r)
            scored.append(r)
        scored.sort(key=lambda r: r.get("score", 0), reverse=True)
        priorizado = OUT_DIR / "pronto-disparo-priorizado.csv"
        with priorizado.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames + ["score"])
            writer.writeheader()
            writer.writerows(scored)
        print(f"Gerado: {priorizado} ({len(scored)} contatos priorizados)")
    except Exception as e:
        print(f"Lead scoring indisponível no momento: {e}")


if __name__ == "__main__":
    run()
