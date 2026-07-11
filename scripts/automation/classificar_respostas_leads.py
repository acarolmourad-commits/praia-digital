"""Classifica respostas de leads por palavras-chave, atualiza o tracking e gera follow-ups.

Uso:
  python scripts/automation/classificar_respostas_leads.py docs/sales/tracking-envios-lote-50-2026-07-12.csv
"""
import csv, sys
from pathlib import Path
from datetime import datetime
import html as ihtml

REGRAS = {
    'interessado': ['interesse','quero','sim','vamos','agendar','call','proposta','demo','avançar','pode','mande','envie','solicita','material','case','contrato'],
    'rejeitado': ['não','obrigado','agora não','sem orçamento','não preciso','recusar'],
    'fechado': ['aceito','fechado','combinado','assinar','contrato','bora','fechou','ok','parceria','voucher'],
    'neutro': ['talvez','depois','mais tarde','informaç','dúvida','preço','valor','como funciona','ajudar','esclarecer']
}

TEMPLATES = {
    'enviar_proposta': 'Olá, {nome_contato},\nObrigado pela conversa. Segue proposta comercial da Praia Digital para {imobiliaria}, com início sem custo.\nPróximos passos:\n- Revisão da proposta em até 48h\n- Call de alinhamento\n- Case conjunto e métricas\nSite: https://acarolmourad-commits.github.io/praia-digital/\nFerramentas gratuitas: https://praia.digital\nCEO - Praia Digital',
    'follow_up_7d': 'Olá, {nome_contato},\nPerfeito, vamos manter uma conversa objetiva. Seguem dados adicionais sobre redução de custos e aumento de conversão para {imobiliaria}.\nSe fizer sentido, reagendamos uma call de 15 minutos.\nSite: https://acarolmourad-commits.github.io/praia-digital/\nFerramentas gratuitas: https://praia.digital\nCEO - Praia Digital',
    'follow_up_90d': 'Olá, {nome_contato},\nSem problema. Vou deixar o contato aberto para quando fizer sentido. Voltarei daqui a 90 dias com novidades relevantes para {imobiliaria}.\nAproveite nossas ferramentas gratuitas enquanto isso: https://praia.digital\nCEO - Praia Digital',
    'onboarding': 'Olá, {nome_contato},\nÓtimo! Vamos iniciar o onboarding de {imobiliaria} em até 24h. Você receberá cronograma, acessos e métricas do case.\nSite: https://acarolmourad-commits.github.io/praia-digital/\nFerramentas gratuitas: https://praia.digital\nCEO - Praia Digital',
}

def classificar(texto):
    texto = (texto or '').lower()
    for classe, palavras in REGRAS.items():
        if any(p in texto for p in palavras):
            return classe
    return 'neutro'

def next_action(classe):
    return {
        'interessado': 'enviar_proposta',
        'rejeitado': 'follow_up_90d',
        'fechado': 'onboarding',
        'neutro': 'follow_up_7d'
    }.get(classe, 'follow_up_7d')

def main():
    if len(sys.argv) < 2:
        print('Uso: python scripts/automation/classificar_respostas_leads.py <csv_tracking>')
        sys.exit(1)
    resp_path = Path(sys.argv[1])
    root = Path('C:/Users/Carolina/praia-digital')
    out_csv = root / 'docs/sales/leads-litoral-enriquecido-classificado.csv'
    tracker_path = root / 'docs/sales/tracking-envios-lote-50-2026-07-12.csv'
    out_dir = root / 'outreach/emails-followup-classificados'
    out_dir.mkdir(parents=True, exist_ok=True)

    with resp_path.open('r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter=';'))

    headers = list(rows[0].keys()) if rows else []
    extra = ['classificacao','proxima_acao','data_classificacao']
    for h in extra:
        if h not in headers:
            headers.append(h)

    hoje = datetime.now().strftime('%d/%m/%Y')
    processed = []
    for r in rows:
        texto = ' '.join([str(r.get('resposta','')), str(r.get('nome_imobiliaria','')), str(r.get('cidade',''))])
        cls = classificar(texto)
        r['classificacao'] = cls
        r['proxima_acao'] = next_action(cls)
        r['data_classificacao'] = hoje
        processed.append(r)

    with tracker_path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=headers, delimiter=';')
        w.writeheader()
        for r in processed:
            w.writerow({k: r.get(k,'') for k in headers})

    count = 0
    for r in processed:
        acao = r.get('proxima_acao','')
        template = TEMPLATES.get(acao)
        if not template:
            continue
        nome = (r.get('contato') or r.get('nome_contato') or 'Contato').strip()
        imob = (r.get('nome_imobiliaria') or 'Imobiliária').strip()
        body = template.format(nome_contato=nome, imobiliaria=imob)
        fname = f"{r.get('lead_id','0').zfill(3)}-{acao}-{imob.lower().replace(' ','-')[:30]}.html"
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>Follow-up - {imob}</title></head>
<body style="font-family:Arial,sans-serif;max-width:700px;margin:auto;padding:20px;color:#222;">
<pre style="white-space:pre-wrap;font-family:Arial,sans-serif;font-size:15px;">{ihtml.escape(body)}</pre>
<p>Site: <a href="https://acarolmourad-commits.github.io/praia-digital/">Praia Digital</a></p>
<p>Ferramentas gratuitas: <a href="https://praia.digital">https://praia.digital</a></p>
<p>CEO — Praia Digital</p>
</body></html>"""
        (out_dir / fname).write_text(html, encoding='utf-8')
        count += 1

    from collections import Counter
    print('Processados:', len(processed))
    print('Classificados:', dict(Counter(r.get('classificacao') for r in processed)))
    print('Follow-ups gerados:', count)
    print('Tracking atualizado:', tracker_path)
    print('Pasta:', out_dir)

if __name__ == '__main__':
    main()
