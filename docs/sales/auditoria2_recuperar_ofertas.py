"""
Auditoria 2 — Recuperação de ofertas reais com parsing seguro por arquivo.

Gera:
- docs/sales/qualidade-parsing-fontes-2026-08-17.json
- docs/sales/auditoria-ofertas-recuperadas-2026-08-17.json
- docs/sales/auditoria-ofertas-recuperadas-2026-08-17.html
"""
import csv, json, re, hashlib, os
from pathlib import Path
from datetime import datetime
from io import StringIO

BASE = Path("C:/Users/Carolina/praia-digital")
DOCS = BASE / "docs" / "sales"

# Arquivos-alvo para parsing seguro
TARGETS = [
    DOCS / "csv-lotes-email" / "tracker-whatsapp-proprietarios.csv",
    DOCS / "csv-lotes-email" / "tracker-email-proprietarios.csv",
    DOCS / "csv-lotes-b2b" / "tracker-b2b.csv",
    DOCS / "csv-lotes-b2b" / "tracker-email-b2b.csv",
]
TARGETS.extend(sorted((DOCS / "csv-lotes-b2b").glob("followup-pairs-*.csv")))

# Campos padrão para followup-pairs-*
FOLLOWUP_FIELDS = ["id;nome;cidade;telefone;telefone_raw;q1_em;msg1;q2_em;msg2;q3_em;msg3".split(";"),
                   "Lote;Nome;Telefone;Cidade;Data_Msg1;Status;Resposta;Valor_Estimado;Obs;Acao_Conversao;Msg1;Msg2;Msg3;Email;Imobiliaria".split(";"),
                   ["lote","nome","telefone","cidade","data_msg1","status","resposta","valor_estimado","obs","acao_conversao","msg1","msg2","msg3","email","imobiliaria"]]

QUALITY_REPORT = {
    "gerado_em": datetime.utcnow().isoformat() + "Z",
    "arquivos": []
}
OFFERS = []
INCONSISTENCIES = []

def detect_sniff(text, default_delimiter=';'):
    try:
        sample = text[:2048]
        dialect = csv.Sniffer().sniff(sample, delimiters=[';',',','\t','|'])
        return dialect.delimiter
    except Exception:
        return default_delimiter

def safe_read(path: Path):
    # Detect BOM/encoding
    raw = path.read_bytes()
    if raw[:3] == b'\xef\xbb\xbf':
        text = raw[3:].decode('utf-8', errors='replace')
        encoding = 'utf-8-sig'
    else:
        text = raw.decode('utf-8', errors='replace')
        encoding = 'utf-8'
    return text, encoding

def parse_tracker(path: Path):
    text, encoding = safe_read(path)
    delimiter = detect_sniff(text, ';')
    reader = csv.reader(StringIO(text), delimiter=delimiter)
    rows = []
    headers = []
    total = 0
    invalid = 0
    ambiguous = 0
    valid = 0
    parse_errors = []
    for i, row in enumerate(reader, start=1):
        total += 1
        if i == 1:
            headers = [h.strip() for h in row]
            continue
        if not any(v.strip() for v in row):
            invalid += 1
            continue
        # Simple heuristic: must have at least nome/status/valor columns
        if len(row) < 3:
            invalid += 1
            parse_errors.append({"linha": i, "motivo": "colunas insuficientes", "raw": row})
            continue
        obj = dict(zip(headers, row))
        # Mark ambiguous if status is missing but valor exists, etc.
        status = (obj.get('Status') or obj.get('status') or '').strip()
        valor = (obj.get('Valor_Estimado') or obj.get('valor_estimado') or '').strip()
        nome = (obj.get('Nome') or obj.get('nome') or '').strip()
        if not nome:
            invalid += 1
            parse_errors.append({"linha": i, "motivo": "nome ausente", "raw": row})
            continue
        if status == '' and valor != '':
            ambiguous += 1
            obj['PARSING_AMBIGUO'] = True
            obj['MOTIVO_AMBIGUO'] = 'status ausente com valor presente'
        rows.append(obj)
        valid += 1
    quality = {
        "arquivo": str(path.relative_to(BASE)),
        "encoding": encoding,
        "delimitador": delimiter,
        "cabeçalho": headers,
        "linhas_totais": total,
        "linhas_validas": valid,
        "linhas_ambiguas": ambiguous,
        "linhas_invalidas": invalid,
        "campos_detectados": headers,
        "erros_parsing": parse_errors[:20]
    }
    return quality, rows

def parse_followup(path: Path):
    text, encoding = safe_read(path)
    delimiter = detect_sniff(text, ';')
    reader = csv.reader(StringIO(text), delimiter=delimiter)
    rows = []
    headers = []
    total = 0
    invalid = 0
    ambiguous = 0
    valid = 0
    errors = []
    for i, row in enumerate(reader, start=1):
        total += 1
        if i == 1:
            headers = [h.strip() for h in row]
            continue
        if not any(v.strip() for v in row):
            invalid += 1
            continue
        if len(row) < 4:
            invalid += 1
            errors.append({"linha": i, "motivo": "colunas insuficientes", "raw": row})
            continue
        obj = dict(zip(headers, row))
        nome = (obj.get('nome') or obj.get('Nome') or '').strip()
        telefone = (obj.get('telefone') or obj.get('Telefone') or '').strip()
        if not nome or not telefone:
            invalid += 1
            errors.append({"linha": i, "motivo": "nome/telefone ausentes", "raw": row})
            continue
        # Identify service/value from perfil/valor columns
        perfil = (obj.get('perfil') or obj.get('Obs') or '').strip()
        valor = (obj.get('valor_estimado') or obj.get('Valor_Estimado') or '').strip()
        servico = ''
        m = re.search(r'Servico alvo:\s*(.+?)(?:;|$)', perfil, re.IGNORECASE)
        if m:
            servico = m.group(1).strip()
        if not servico and perfil:
            ambiguous += 1
            obj['PARSING_AMBIGUO'] = True
            obj['MOTIVO_AMBIGUO'] = 'servico alvo não identificado no perfil'
        rows.append(obj)
        valid += 1
    quality = {
        "arquivo": str(path.relative_to(BASE)),
        "encoding": encoding,
        "delimitador": delimiter,
        "cabeçalho": headers,
        "linhas_totais": total,
        "linhas_validas": valid,
        "linhas_ambiguas": ambiguous,
        "linhas_invalidas": invalid,
        "campos_detectados": headers,
        "erros_parsing": errors[:20]
    }
    return quality, rows

# Parse all targets
all_qualities = []
all_rows = []
for path in TARGETS:
    if not path.exists():
        continue
    if 'followup-pairs' in path.name:
        q, rows = parse_followup(path)
    else:
        q, rows = parse_tracker(path)
    all_qualities.append(q)
    all_rows.extend(rows)

# Save quality report
QUALITY_REPORT['arquivos'] = all_qualities
qual_path = DOCS / "qualidade-parsing-fontes-2026-08-17.json"
qual_path.write_text(json.dumps(QUALITY_REPORT, ensure_ascii=False, indent=2), encoding='utf-8')
print("QUALIDADE_PARSING", qual_path, qual_path.stat().st_size)

# Build offer evidence from reliable rows
# For trackers, offer is mostly not explicit; for followup-pairs, service target is evidence.
offer_evidence = []
inconsistencies = []
seen_offer = set()

for row in all_rows:
    nome = (row.get('nome') or row.get('Nome') or '').strip()
    telefone = (row.get('telefone') or row.get('Telefone') or '').strip()
    cidade = (row.get('cidade') or row.get('Cidade') or '').strip()
    canal = row.get('campanha') or row.get('canal') or Path(row.get('fonte','')).name if isinstance(row.get('fonte'), str) else ''
    valor = (row.get('valor_estimado') or row.get('Valor_Estimado') or '').strip()
    perfil = row.get('perfil') or row.get('Obs') or ''
    servico = ''
    m = re.search(r'Servico alvo:\s*(.+?)(?:;|$)', perfil, re.IGNORECASE)
    if m:
        servico = m.group(1).strip()
    status = (row.get('status') or row.get('Status') or '').strip()
    fonte = row.get('fonte', '') if isinstance(row.get('fonte'), str) else ''
    if not fonte:
        # infer from row keys if needed
        fonte = ''
    oferta_status = 'OFERTA_CONFIRMADA' if servico else ('OFERTA_PROVÁVEL' if perfil else 'OFERTA_NÃO_IDENTIFICADA')
    key = (nome, telefone, servico, valor, oferta_status)
    if key in seen_offer:
        continue
    seen_offer.add(key)
    # Academy mapping attempt by service keywords -> slug guess
    slug_guess = ''
    course_id_guess = None
    product_id_guess = None
    academy_relacao = 'PRODUTO_NÃO_IDENTIFICADO'
    if servico:
        s = servico.lower()
        if 'avaliacao' in s:
            slug_guess = 'avaliacao-de-imoveis'
        elif 'captacao' in s:
            slug_guess = 'captacao-imoveis-corretores'
        elif 'consultoria' in s:
            slug_guess = 'consultoria'
        elif 'descricao' in s:
            slug_guess = 'descricao-de-imoveis'
        elif 'proptech' in s:
            slug_guess = 'ia-para-imobiliarias'
        elif 'seo local' in s:
            slug_guess = 'seo-local'
        elif 'automacao' in s:
            slug_guess = 'automacao-comercial'
        if slug_guess:
            academy_relacao = 'PRODUTO_PROVÁVEL'
    # inconsistencies
    if status == 'fechou':
        inconsistencies.append({'lead': nome, 'inc': 'fechou + pagamento ausente', 'fonte': fonte})
    if 'onboarding_feito' in row.get('Acao_Conversao', '') or 'onboarding_feito' in row.get('acao_conversao', ''):
        inconsistencies.append({'lead': nome, 'inc': 'onboarding_feito + pagamento ausente', 'fonte': fonte})
    if valor and status != 'PAGAMENTO_CONFIRMADO':
        inconsistencies.append({'lead': nome, 'inc': 'valor estimado não é receita confirmada', 'fonte': fonte})
    offer_evidence.append({
        'lead': nome,
        'contato': telefone,
        'cidade': cidade,
        'canal': canal,
        'oferta_status': oferta_status,
        'produto_academy': academy_relacao,
        'slug_guess': slug_guess,
        'course_id': course_id_guess,
        'product_id': product_id_guess,
        'valor': valor,
        'servico': servico,
        'perfil': perfil[:200],
        'fonte': fonte,
        'evidencia': perfil[:200] if perfil else valor or status,
        'payment_status': 'PAGAMENTO_NAO_ENCONTRADO',
        'delivery_status': 'BLOQUEADA',
        'revenue_confirmed': 0
    })

# Summary
summary = {
    "gerado_em": datetime.utcnow().isoformat() + "Z",
    "registros_confirmados": sum(1 for o in offer_evidence if o['oferta_status'] == 'OFERTA_CONFIRMADA'),
    "registros_provaveis": sum(1 for o in offer_evidence if o['oferta_status'] == 'OFERTA_PROVÁVEL'),
    "registros_nao_identificados": sum(1 for o in offer_evidence if o['oferta_status'] == 'OFERTA_NÃO_IDENTIFICADA'),
    "inconsistencias": inconsistencies,
    "inconsistencias_unicas": sorted({i['inc'] for i in inconsistencies}),
    "produtos_identificados": sorted({o['servico'] for o in offer_evidence if o['servico']}),
    "cursos_relacionados": sorted({o['slug_guess'] for o in offer_evidence if o['slug_guess']}),
    "fontes_externas_necessarias": [
        "CRM/WhatsApp Business API",
        "Gmail/Google Workspace",
        "Hotmart/gateway",
        "Registros de pagamento/comprovante"
    ]
}

audit_path = DOCS / "auditoria-ofertas-recuperadas-2026-08-17.json"
audit_path.write_text(json.dumps({"resumo": summary, "ofertas": offer_evidence}, ensure_ascii=False, indent=2), encoding='utf-8')
print("AUDITORIA", audit_path, audit_path.stat().st_size)
print("RESUMO", summary)

# HTML report (compacto e seguro)
html = f"""<!DOCTYPE html>
<html lang=\"pt-BR\">
<head><meta charset=\"utf-8\"><title>Auditoria de Ofertas Recuperadas — 2026-08-17</title></head>
<body>
<h1>Auditoria de Ofertas Recuperadas</h1>
<p>Gerado em: {summary['gerado_em']}</p>
<h2>Resumo</h2>
<ul>
<li>Confirmadas: {summary['registros_confirmados']}</li>
<li>Prováveis: {summary['registros_provaveis']}</li>
<li>Não identificadas: {summary['registros_nao_identificados']}</li>
<li>Produtos identificados: {len(summary['produtos_identificados'])}</li>
<li>Cursos relacionados: {len(summary['cursos_relacionados'])}</li>
</ul>
<h2>Inconsistências</h2>
<ul>
"""
for inc in summary['inconsistencias_unicas']:
    html += f"<li>{inc}</li>\n"
html += "</ul>\n<h2>Amostra Fernanda Lima</h2>\n<table border=1 cellpadding=6>\n<tr><th>Serviço</th><th>Valor</th><th>Status</th></tr>\n"
for o in offer_evidence:
    if o['lead'].lower() == 'fernanda lima':
        html += f"<tr><td>{o['servico']}</td><td>{o['valor']}</td><td>{o['oferta_status']}</td></tr>\n"
html += "</table>\n</body></html>"
html_path = DOCS / "auditoria-ofertas-recuperadas-2026-08-17.html"
html_path.write_text(html, encoding='utf-8')
print("HTML", html_path, html_path.stat().st_size)
