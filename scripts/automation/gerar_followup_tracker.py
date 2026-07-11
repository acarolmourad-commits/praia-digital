"""Gera e-mails de follow-up automáticos a partir do tracker de follow-up.
Lê docs/sales/followup-registro.md e cria HTMLs em outreach/emails-followup-tracker/.
"""
from pathlib import Path
import html as ihtml
from datetime import datetime

ROOT = Path('C:/Users/Carolina/praia-digital')
tracker = ROOT / 'docs/sales/followup-registro.md'
out_dir = ROOT / 'outreach/emails-followup-tracker'
out_dir.mkdir(parents=True, exist_ok=True)

FOLLOWUP_TEMPLATES = {
    'enviar_proposta': 'Olá, {nome_contato},\nObrigado pela conversa. Segue proposta comercial da Praia Digital para {imobiliaria}, com início sem custo.\nPróximos passos:\n- Revisão da proposta em até 48h\n- Call de alinhamento\n- Case conjunto e métricas\nSite: https://acarolmourad-commits.github.io/praia-digital/\nFerramentas gratuitas: https://praia.digital\nCEO - Praia Digital',
    'follow_up_7d': 'Olá, {nome_contato},\nPerfeito, vamos manter uma conversa objetiva. Seguem dados adicionais sobre redução de custos e aumento de conversão para {imobiliaria}.\nSe fizer sentido, reagendamos uma call de 15 minutos.\nSite: https://acarolmourad-commits.github.io/praia-digital/\nFerramentas gratuitas: https://praia.digital\nCEO - Praia Digital',
    'follow_up_3d': 'Olá, {nome_contato},\nSó passando rapidinho para não sumir. A ideia continua: piloto sem investimento inicial focado em resultado para {imobiliaria}.\nSe fizer sentido, eu sigo com o Deep Dive e confirmamos 30min em vídeo.\nSite: https://acarolmourad-commits.github.io/praia-digital/\nFerramentas gratuitas: https://praia.digital\nCEO - Praia Digital',
    'onboarding': 'Olá, {nome_contato},\nÓtimo! Vamos iniciar o onboarding de {imobiliaria} em até 24h. Você receberá cronograma, acessos e métricas do case.\nSite: https://acarolmourad-commits.github.io/praia-digital/\nFerramentas gratuitas: https://praia.digital\nCEO - Praia Digital',
    'assinatura': 'Olá, {nome_contato},\nParabéns pelo fechamento com {imobiliaria}. O documento de assinatura está pronto e inclui participação no case oficial.\nSite: https://acarolmourad-commits.github.io/praia-digital/\nFerramentas gratuitas: https://praia.digital\nCEO - Praia Digital',
    'follow_up_90d': 'Olá, {nome_contato},\nSem problema. Vou deixar o contato aberto para quando fizer sentido. Voltarei daqui a 90 dias com novidades relevantes para {imobiliaria}.\nAproveite nossas ferramentas gratuitas enquanto isso: https://praia.digital\nCEO - Praia Digital',
}

def parse_markdown_table(text):
    rows = []
    for line in text.splitlines():
        line=line.strip()
        if not line.startswith('|') or line.strip().startswith('|---') or 'lead_id' in line:
            continue
        cells=[c.strip() for c in line.strip().strip('|').split('|')]
        rows.append(cells)
    return rows

def main():
    if not tracker.exists():
        print('Tracker não encontrado:', tracker)
        return
    rows = parse_markdown_table(tracker.read_text(encoding='utf-8'))
    count=0
    for cells in rows:
        if len(cells) < 8:
            continue
        lead_id, nome_contato, imobiliaria, cidade, data_call, resultado, proxima_acao, data_proxima = cells[:8]
        template = FOLLOWUP_TEMPLATES.get(proxima_acao)
        if not template:
            continue
        nome = nome_contato or 'Contato'
        imob = imobiliaria or 'Imobiliária'
        body = template.format(nome_contato=nome, imobiliaria=imob)
        fname = f'{lead_id}-{proxima_acao}-{imob.lower().replace(" ","-")[:30]}.html'
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
    print('Gerados:', count)
    print('Pasta:', out_dir)

if __name__ == '__main__':
    main()
