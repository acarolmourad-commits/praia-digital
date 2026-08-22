#!/usr/bin/env python3
"""
Motor A D2 — Runner operacional (standalone).
Fonte: docs/comercial/motor_a_novo_estoque_2026-08-16.csv
Saída: docs/comercial/motor_a_fila_d2_2026-08-17.csv + docs/comercial/motor_a_audit_log_2026-08-17.csv + relatório Markdown.
Não envia mensagens. Apenas prepara fila executável.
"""

import csv
import re
from datetime import datetime
from pathlib import Path

REPO = Path('C:/Users/Carolina/praia-digital')
ESTOQUE_PATH = REPO / 'docs/comercial/motor_a_novo_estoque_2026-08-16.csv'
FILA_PATH = REPO / 'docs/comercial/motor_a_fila_d2_2026-08-17.csv'
AUDIT_PATH = REPO / 'docs/comercial/motor_a_audit_log_2026-08-17.csv'
REPORT_PATH = REPO / 'docs/comercial/motor_a_d2_report_2026-08-17.md'
CHECKLIST_GSC_PATH = REPO / 'docs/seo/gsc-improvement-checklist-pos-d2-2026-08-17.md'
FRONT_A_PATH = REPO / 'assets/servico-video-ia-imoveis-litoral.html'
DATA_HOJE = '2026-08-17'
D2_ORIGINAL_ORDEM = ['9', '11', '14', '15', '27', '29']


def _normalize(text: str) -> str:
    text = text or ''
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '', text)
    return text


def _now_iso():
    return datetime.now().isoformat(timespec='seconds')


def read_csv(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows, fieldnames):
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def audit_estoque(rows):
    validados = []
    duplicados = []
    bloqueados = []
    seen_email = {}
    seen_phone = {}
    seen_company_contact = {}

    for r in rows:
        lead_id = r.get('lead_id', '').strip()
        empresa = _normalize(r.get('nome_empresa', ''))
        contato = _normalize(r.get('canal_contato', ''))
        url_key = _normalize(r.get('url', ''))
        phone_key = _normalize(r.get('canal_contato', ''))

        if not lead_id:
            bloqueados.append({'lead_id': lead_id, 'motivo': 'lead_id ausente'})
            continue

        dup_reason = None
        if url_key and url_key in seen_email:
            dup_reason = 'DUPLICADO'
        elif phone_key and phone_key in seen_phone:
            dup_reason = 'DUPLICADO'
        elif empresa and contato and f'{empresa}|{contato}' in seen_company_contact:
            dup_reason = 'REVISÃO_NECESSÁRIA'

        if dup_reason:
            duplicados.append({'lead_id': lead_id, 'motivo': dup_reason})
        else:
            validados.append(r)

        seen_email[url_key] = lead_id
        seen_phone[phone_key] = lead_id
        if empresa and contato:
            seen_company_contact[f'{empresa}|{contato}'] = lead_id

    return {'total': len(rows), 'validados': validados, 'duplicados': duplicados, 'bloqueados': bloqueados}


def qualificar(r):
    score = int(r.get('score', '0') or '0')
    servico = r.get('servico_potencial', '').lower()
    if 'administração' in servico or 'gestão' in servico or score >= 80:
        potencial = 'ALTO'
    elif score >= 70:
        potencial = 'MÉDIO'
    else:
        potencial = 'BAIXO'
    return {'receita_potencial': 'RECEITA_NÃO_INFORMADA', 'qualificacao': potencial, 'motivo': f"score={score}; servico={r.get('servico_potencial')}"}


def priorizar(validados):
    def rank(r):
        score = int(r.get('score', '0') or '0')
        servico = r.get('servico_potencial', '').lower()
        bonus = 0
        if 'administração' in servico or 'gestão' in servico:
            bonus += 5
        if r.get('canal_contato') in {'WhatsApp', 'Instagram', 'Facebook'}:
            bonus += 2
        return score + bonus

    return sorted(validados, key=rank, reverse=True)


def gerar_acao(r):
    canal = r.get('canal_contato', '')
    servico = r.get('servico_potencial', '')
    cidade = r.get('city', '')
    bairro = r.get('bairro', '')
    nome = r.get('nome_empresa', '') or 'proprietário'
    if canal.lower() == 'whatsapp':
        return f'Abrir conversa no WhatsApp com {nome} ({cidade}/{bairro}) para {servico}.'
    if canal.lower() == 'instagram':
        return f'Enviar DM no Instagram para {nome} com proposta de {servico}.'
    if canal.lower() == 'facebook':
        return f'Enviar mensagem no Facebook para {nome} sobre {servico}.'
    if canal.lower() == 'olx':
        return f'Responder pelo OLX e converter para WhatsApp; proposta {servico}.'
    if canal.lower() == 'zap imóveis':
        return f'Responder pelo Zap Imóveis e converter para WhatsApp; proposta {servico}.'
    if 'temporadalivre' in (r.get('url', '') or '').lower():
        return f'Responder pelo TemporadaLivre e converter para WhatsApp; proposta {servico}.'
    return f'Contatar {nome} por {canal} para {servico}.'


def build_fila(priorizados):
    fila = []
    for idx, r in enumerate(priorizados, start=1):
        q = qualificar(r)
        acao = gerar_acao(r)
        fila.append({
            'lead_id': r['lead_id'],
            'nome_empresa': r.get('nome_empresa', ''),
            'cidade': r.get('city', ''),
            'bairro': r.get('bairro', ''),
            'canal_contato': r.get('canal_contato', ''),
            'servico_potencial': r.get('servico_potencial', ''),
            'score': r.get('score', ''),
            'status': 'PRONTO_D2',
            'prioridade': idx,
            'receita_potencial': q['receita_potencial'],
            'acao_sugerida': acao,
            'origem': 'motor_a_novo_estoque_2026-08-16.csv',
            'd2_enviado_em': '',
            'responsavel': '',
            'proxima_acao': '',
            'evidencia': r.get('evidencia', ''),
        })
    return fila


def build_audit(fila):
    audit = []
    for r in fila:
        audit.append({
            'timestamp': _now_iso(),
            'lead_id': r['lead_id'],
            'evento': 'PRONTO_D2',
            'estado_anterior': 'NOVO_ESTOQUE',
            'estado_novo': 'PRONTO_D2',
            'origem': r['origem'],
            'motivo': r['acao_sugerida'],
        })
    return audit


def main():
    print('=== Motor A D2 — Runner operacional ===')
    print(f'Data/hora: {_now_iso()}')
    print('D2_ORIGINAL = BLOQUEADO — FONTE EXECUTÁVEL AUSENTE')

    if not ESTOQUE_PATH.exists():
        print('ESTOQUE_NAO_ENCONTRADO')
        return

    rows = read_csv(ESTOQUE_PATH)
    audit = audit_estoque(rows)
    priorizados = priorizar(audit['validados'])
    fila = build_fila(priorizados)
    audit_rows = build_audit(fila)

    fila_fieldnames = list(fila[0].keys()) if fila else []
    audit_fieldnames = list(audit_rows[0].keys()) if audit_rows else []

    write_csv(FILA_PATH, fila, fila_fieldnames)
    write_csv(AUDIT_PATH, audit_rows, audit_fieldnames)

    print('total', audit['total'])
    print('validados', audit['validados'])
    print('duplicados', audit['duplicados'])
    print('bloqueados', audit['bloqueados'])
    print('prontos_d2', len(fila))

    print('\n--- Ação D2 Motor A ---')
    for r in fila:
        print(f"{r['lead_id']} | {r['acao_sugerida']}")

    print('\n--- Verificação Front A ---')
    front = 'AUSENTE'
    if FRONT_A_PATH.exists():
        front = f"EXISTE tamanho={len(FRONT_A_PATH.read_text(encoding='utf-8'))}"
    print(front)

    report = f'''# Relatório Motor A D2
Data: {DATA_HOJE}
Gerado: {_now_iso()}

## D2 Original
- Status: BLOQUEADO — FONTE EXECUTÁVEL AUSENTE
- Leads originais: {len(D2_ORIGINAL_ORDEM)}
- Envios realizados: 0

## Estoque Motor A
- Arquivo: docs/comercial/motor_a_novo_estoque_2026-08-16.csv
- Total: {audit['total']}
- Válidos: {len(audit['validados'])}
- Duplicados: {len(audit['duplicados'])}
- Bloqueados: {len(audit['bloqueados'])}
- Prontos para D2: {len(fila)}

## Ação comercial
'''
    for r in fila:
        report += f"- Lead {r['lead_id']}: {r['acao_sugerida']}\n"

    report += '''
## Envio
- Real: NÃO EXECUTADO
- Motivo: sem canal de envio real autorizado/configurado
- Marcação: AÇÃO_HUMANA_NECESSÁRIA

## CRM
- Integração: CSV operacional + audit log
- Arquivos: motor_a_fila_d2_2026-08-17.csv, motor_a_audit_log_2026-08-17.csv

## Métricas
- Enviados: 0
- Respostas: NÃO DISPONÍVEL
- Receita confirmada: NÃO DISPONÍVEL
- Receita potencial: NÃO INFORMADA

## Integridade
- Front A: não alterada
- Checklist GSC: não alterado
- Estoque editorial: não alterado

## Status
- D2 original: BLOQUEADO
- Motor A D2: IMPLEMENTADO — PRONTO PARA AÇÃO HUMANA/ENVIO QUANDO AUTORIZADO
'''
    REPORT_PATH.write_text(report, encoding='utf-8')
    print('relatorio_salvo', REPORT_PATH)
    print('fila_salva', FILA_PATH)
    print('audit_salvo', AUDIT_PATH)
    print('\n=== Concluído ===')


if __name__ == '__main__':
    main()
