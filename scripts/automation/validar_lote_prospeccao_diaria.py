#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador de lote de prospecção diária.
Checa CSV do dia, procura repetições, e-mails/whatsapp inválidos e gera relatório.
"""
import os, re, csv
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEADS_CSV = os.path.join(BASE, "docs", "sales", "leads-litoral-enriquecido.csv")
OUT_DIR = os.path.join(BASE, "docs", "sales")
TODAY = datetime.now().strftime("%Y-%m-%d")
OUT = os.path.join(OUT_DIR, f"validacao-lote-{TODAY}.md")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
WA_RE = re.compile(r"^\+?\d[\d\s\-\(\)]{8,}$")


def ok(msg):
    return f"✔ {msg}"


def fail(msg):
    return f"✘ {msg}"


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_phone(value):
    digits = re.sub(r"\D", "", value or "")
    return digits


def warn(msg):
    return f"⚠ {msg}"


def validate_row(r, idx):
    issues = []
    nome = (r.get("nome_da_imobiliaria") or r.get("nome") or "").strip()
    contato = (r.get("pessoa_de_contato") or r.get("nome") or "").strip()
    email = (r.get("email") or "").strip()
    whats = normalize_phone(r.get("whatsapp") or "")
    cidade = (r.get("cidade") or "").strip()
    if not nome:
        issues.append(fail(f"Linha {idx}: nome vazio"))
    if not email or not EMAIL_RE.match(email):
        issues.append(fail(f"Linha {idx}: e-mail inválido: '{email}'"))
    if not whats or len(whats) < 10 or len(whats) > 13:
        issues.append(fail(f"Linha {idx}: WhatsApp inválido após limpeza: '{whats}'"))
    if not cidade:
        issues.append(warn(f"Linha {idx}: cidade vazia"))
    return issues


def main():
    if not os.path.exists(LEADS_CSV):
        print(f"Arquivo não encontrado: {LEADS_CSV}")
        return
    rows = []
    with open(LEADS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, r in enumerate(reader, 1):
            rows.append(r)
    issues = []
    seen_emails = set()
    seen_whats = set()
    for i, r in enumerate(rows, 1):
        issues.extend(validate_row(r, i))
        email = (r.get("email") or "").strip().lower()
        whats = (r.get("whatsapp") or "").strip()
        if email:
            if email in seen_emails:
                issues.append(warn(f"Linha {i}: e-mail repetido: {email}"))
            seen_emails.add(email)
        if whats:
            if whats in seen_whats:
                issues.append(warn(f"Linha {i}: WhatsApp repetido: {whats}"))
            seen_whats.add(whats)

    total = len(rows)
    erros = sum(1 for x in issues if x.startswith("✘"))
    warnings = sum(1 for x in issues if x.startswith("⚠"))
    ok_lines = sum(1 for x in issues if x.startswith("✔"))
    status = "APROVADO" if erros == 0 else "BLOQUEADO"

    md = f"""# Validação de Lote de Prospecção — {TODAY}

Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}

## Status: {status}

| Métrica | Valor |
|---------|-------|
| Total de leads | {total} |
| Erros | {erros} |
| Avisos | {warnings} |
| Linhas OK | {ok_lines} |

## Detalhamento

"""
    if issues:
        md += "\n".join(issues) + "\n"
    else:
        md += ok("Nenhum problema encontrado.\n")

    md += """
## Ações sugeridas

"""
    if erros:
        md += "- Corrija os campos inválidos antes de enviar.\n"
    if warnings:
        md += "- Revise duplicidades para evitar rejeição por spam.\n"
    if erros == 0 and warnings == 0:
        md += "- Lote liberado para envio.\n"

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Relatório: {OUT}")
    print(f"Status: {status} | Erros: {erros} | Avisos: {warnings}")


if __name__ == "__main__":
    main()
