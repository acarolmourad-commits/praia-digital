#!/usr/bin/env python3
"""
Automacao de follow-up D2/D5/D10 para leads de São Sebastião/Bertioga.
- Marca no CSV leads prontos para próxima etapa.
- Para Instagram com PSID conhecido: envia DM via Composio.
- Para demais canais: gera lote manual.
"""
import csv
import json
import subprocess
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parent.parent / 'docs' / 'comercial'
LEADS_PATH = BASE / 'leads_sao_sebastiao_bertioga.csv'
LOTE_PATH_TMPL = BASE / 'lote_envio_dia_{today}.md'
TEMPLATES_PATH = BASE / 'templates_followup_ab_sao_sebastiao_bertioga_2026-08-30.md'

TODAY = date.today()
TODAY_STR = TODAY.isoformat()

# Mapeamento manual de PSIDs conhecidos por lead_id (preencher conforme houver dados reais)
KNOWN_PSIDS = {
    # Exemplo: 6: 'aWdfZAG06MzQwMjgyMzY2ODQxNzEwMzAxMjQ0MjU5MTI1MDk3NzQ0OTkwOTIz',
}

# Templates por variante e dia
TEMPLATES = {
    'A/D2': "Olá, {nome}! Muitos proprietários em {bairro}/{cidade} estão perdendo receita por precificação errada e resposta lenta. Com gestão profissional da temporada + precificação dinâmica, é comum chegar a mais de 70% de ocupação e reduzir trabalho operacional. Se quiser, preparo uma estimativa rápida para o seu imóvel.",
    'A/D5': "Olá, uma dica rápida para {cidade}/{bairro}: temporada alta sem preço atualizado pode custar até 30% da receita. Com gestão profissional e atualização diária, o impacto aparece nas próximas semanas. Se fizer sentido, te mostro como aplicar no seu imóvel.",
    'A/D10': "Olá, última mensagem por aqui: se profissionalizar a gestão da temporada fizer sentido no momento, me avise. Caso contrário, posso manter contato para quando for oportuno.",
    'B/D2': "Olá, {nome}! Muitos imóveis em {bairro}/{cidade} deixam de ganhar visibilidade por uma apresentação pouco profissional. Com fotografia + anúncio estruturado, a qualidade do anúncio melhora muito a experiência do hóspede. Se quiser, envio um exemplo rápido.",
    'B/D5': "Olá, uma dica rápida para {cidade}/{bairro}: anúncios bem estruturados aumentam a confiança do interessado e reduzem dúvidas antes da reserva. Se fizer sentido, posso preparar uma sugestão objetiva para o seu imóvel.",
    'B/D10': "Olá, última mensagem por aqui: se profissionalizar a apresentação do imóvel fizer sentido no momento, me avise. Caso contrário, posso manter contato para quando for oportuno.",
}

def choose_variant(row):
    score = int(row.get('score', 0) or 0)
    evidencia = (row.get('evidencia', '') or '').lower()
    servico = (row.get('servico_potencial', '') or '').lower()
    if score >= 75 and any(k in evidencia for k in ['gestão manual', 'gestao manual', 'whatsapp público', 'whatsapp direto', 'administração']):
        return 'A'
    if any(k in servico for k in ['fotografia', 'edição de anúncio', 'anuncio']):
        return 'B'
    return 'A'

def parse_date(s):
    if not s:
        return None
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None

def days_since(d):
    if not d:
        return None
    return (TODAY - d).days

def send_instagram_dm(recipient_id, text):
    cmd = [
        'wsl', '-e', 'bash', '-lc',
        f'composio execute INSTAGRAM_SEND_TEXT_MESSAGE -d \'{{"recipient_id":"{recipient_id}","text":"{text.replace(chr(34), chr(39))}","ig_user_id":"me"}}\''
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), 1

def main():
    with LEADS_PATH.open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    # Ensure columns
    for col in ['resposta','data_resposta','tipo_resposta','servico_interesse','valor_potencial','estagio','proxima_acao','responsavel','objeção']:
        if col not in fieldnames:
            fieldnames.append(col)

    metrics = {'d2': 0, 'd5': 0, 'd10': 0, 'instagram_sent': 0, 'manual': 0}
    manual_batch = []
    instagram_sends = []

    for row in rows:
        status = row.get('status', '')
        lead_id = row.get('lead_id', '')
        nome = row.get('nome_empresa', 'Lead')
        cidade = row.get('city', '')
        bairro = row.get('bairro', '')
        canal = row.get('canal_contato', '')
        servico = row.get('servico_potencial', '')
        score = int(row.get('score', 0) or 0)

        d0 = parse_date(row.get('d0_enviado_em'))
        d2 = parse_date(row.get('d2_enviado_em'))
        d5 = parse_date(row.get('d5_enviado_em'))
        d10 = parse_date(row.get('d10_enviado_em'))

        # Skip completed
        if status in ['ENCERRADO','BLOQUEADO','HANDOFF','VENDIDO']:
            continue

        variant = choose_variant(row)
        next_msg = None
        next_stage = None

        if status == 'PROSPECTAR' and not d0:
            next_msg = f"Olá, {nome}! Vi que você aluga temporada em {bairro or cidade}. O imóvel tem potencial, mas a gestão manual pode estar custando receita. Na Praia Digital ajudamos com gestão profissional + precificação dinâmica para aumentar ocupação sem aumentar trabalho. Quer ver uma simulação rápida?"
            next_stage = 'ENVIADO_D0'
            metrics['d0'] = metrics.get('d0', 0) + 1
        elif status == 'ENVIADO_D0' and d0 and days_since(d0) >= 2 and not d2:
            next_msg = TEMPLATES[f'{variant}/D2'].format(nome=nome, bairro=bairro or cidade, cidade=cidade)
            next_stage = 'ENVIADO_D2'
            metrics['d2'] += 1
        elif status == 'ENVIADO_D2' and d2 and days_since(d2) >= 3 and not d5:
            next_msg = TEMPLATES[f'{variant}/D5'].format(nome=nome, bairro=bairro or cidade, cidade=cidade)
            next_stage = 'ENVIADO_D5'
            metrics['d5'] += 1
        elif status == 'ENVIADO_D5' and d5 and days_since(d5) >= 5 and not d10:
            next_msg = TEMPLATES[f'{variant}/D10'].format(nome=nome, bairro=bairro or cidade, cidade=cidade)
            next_stage = 'ENVIADO_D10'
            metrics['d10'] += 1

        if not next_msg:
            continue

        # Update CSV
        if next_stage == 'ENVIADO_D2':
            row['d2_enviado_em'] = TODAY_STR
        elif next_stage == 'ENVIADO_D5':
            row['d5_enviado_em'] = TODAY_STR
        elif next_stage == 'ENVIADO_D10':
            row['d10_enviado_em'] = TODAY_STR
        row['status'] = next_stage

        # Try Instagram send if PSID known
        psid = KNOWN_PSIDS.get(int(lead_id))
        if psid and canal == 'Instagram':
            text = next_msg
            stdout, rc = send_instagram_dm(psid, text)
            instagram_sends.append({
                'lead_id': lead_id,
                'nome': nome,
                'recipient_id': psid,
                'text': text,
                'stdout': stdout,
                'returncode': rc,
            })
            metrics['instagram_sent'] += 1
        else:
            manual_batch.append({
                'lead_id': lead_id,
                'nome': nome,
                'canal': canal,
                'cidade': cidade,
                'bairro': bairro,
                'variant': variant,
                'stage': next_stage,
                'text': next_msg,
                'servico': servico,
                'score': score,
            })
            metrics['manual'] += 1

    # Write CSV back
    with LEADS_PATH.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Write manual batch
    manual_path = LOTE_PATH_TMPL.with_name(LOTE_PATH_TMPL.name.format(today=TODAY_STR))
    with manual_path.open('w', encoding='utf-8') as f:
        f.write(f'# Lote de Envio do Dia — {TODAY_STR}\n\n')
        f.write(f'Total preparado: {len(manual_batch)} abordagens\n\n')
        for item in manual_batch:
            f.write(f"## Lead {item['lead_id']} — {item['nome']} ({item['canal']})\n")
            f.write(f"- Cidade/Bairro: {item['cidade']}/{item['bairro']}\n")
            f.write(f"- Serviço: {item['servico']}\n")
            f.write(f"- Score: {item['score']}\n")
            f.write(f"- Variante: {item['variant']} — {item['stage']}\n")
            f.write(f"- Mensagem:\n\n> {item['text']}\n\n")
        f.write('\n---\nGerado automaticamente por scripts/follow_up_automacao.py\n')

    # Write execution report
    report_path = BASE / f'relatorio_followup_{TODAY_STR}.json'
    report = {
        'date': TODAY_STR,
        'metrics': metrics,
        'instagram_sends': instagram_sends,
        'manual_batch_path': str(manual_path),
        'manual_count': len(manual_batch),
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

    print('Metrics:', metrics)
    print('Manual batch:', manual_path)
    print('Report:', report_path)

if __name__ == '__main__':
    main()
