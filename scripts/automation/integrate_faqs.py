#!/usr/bin/env python3
"""
integrate_faqs.py
Insere bloco de FAQ nas landing pages B2B que ainda não possuem, antes do fechamento do container.
"""
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

faq_map = {
    'captacao-imoveis-litoral.html': [
        'Quanto investir em anúncios para ver resultado?', 'A partir de R$ 500/mês, com ajustes contínuos por cidade e perfil de imóvel.',
        'Os leads são qualificados?', 'Sim. Usamos landing + formulário + WhatsApp para filtrar intenção real antes de chegar ao time.',
        'Funciona para temporada?', 'Perfeito. Campanhas por cidade e datas aumentam ocupação e antecipam reservas.',
        'Preciso de site próprio?', 'Não. Usamos landing pages integradas; seu site atual pode continuar recebendo tráfego orgânico.',
        'Como medir o retorno?', 'Relatório semanal: leads, custo por lead, taxa de resposta e agendamentos.',
    ],
    'solucao-proptech-unificada.html': [
        'Preciso trocar todas as ferramentas?', 'Não. Integramos com o que você já usa e unificamos o fluxo; a mudança é gradual.',
        'Qual o investimento mínimo?', 'A partir de R$ 890/mês no plano Starter, com 1 cidade e relatório mensal.',
        'Em quanto tempo fica pronto?', 'Setup inicial em 7–15 dias; os primeiros resultados aparecem no primeiro mês.',
        'Serve para franquias ou multiunidades?', 'Sim. O plano Enterprise suporta multiunidades, API e white-label.',
        'Tem suporte?', 'Sim. Suporte por WhatsApp no Starter, prioritário no Professional e dedicado no Enterprise.',
    ],
    'descricao-imoveis-ia.html': [
        'A descrição fica genérica?', 'Não. Cada texto é adaptado por cidade, perfil e canal, com tom e palavras-chave ajustáveis.',
        'Em quanto tempo fica pronto?', 'Segundos. O lote é gerado em massa para portais e redes sem bloqueio criativo.',
        'Preciso revisar?', 'Sim. O corretor pode editar antes de publicar; a IA entrega o rascunho persuasivo.',
        'Funciona para temporada?', 'Sim. Templates específicos para alta temporada aumentam ocupaçãocpm e cliques.',
        'Qual a diferença para o ChatGPT?', 'Prompt engineering imobiliário + dados de mercado por cidade + formato pronto para publicação.',
    ],
    'seo-local-imobiliarias.html': [
        'Em quanto tempo apareço no Google?', 'De 30 a 60 dias, dependendo da concorrência por cidade e bairro.',
        'Preciso de site próprio?', 'Não obrigatoriamente. Usamos páginas otimizadas e Google Business Profile para gerar visibilidade.',
        'Funciona para temporada?', 'Sim. Campanhas sazonais aumentam buscas por cidade no período de alta demanda.',
        'Como medir o resultado?', 'Por impressões, cliques, posição média e leads vindos de busca local.',
        'Preciso de conhecimento técnico?', 'Não. A equipe cuida de conteúdo, palavras-chave e otimização.',
    ],
    'avaliacao-preco-imoveis.html': [
        'A avaliação é automática ou humana?', 'Automática por dados de mercado, com possibilidade de revisão antes de enviar ao proprietário.',
        'Quanto tempo leva?', 'Segundos para gerar o relatório com comparáveis locais.',
        'Funciona para venda e temporada?', 'Sim. Ajustamos filtros por perfil: venda, locação ou temporada.',
        'Como usar com proprietários?', 'Gere o relatório, personalize se quiser e envie como material oficial de avaliação.',
        'Dá para exportar?', 'Sim. PDF ou link compartilhável para o proprietário.',
    ],
    'consultoria-transformacao-digital-imobiliarias.html': [
        'Preciso de um projeto grande?', 'Não. Começamos por diagnóstico e evoluímos em módulos, sem interromper a operação.',
        'Quanto tempo leva o diagnóstico?', 'Cerca de 15 minutos de call + 5 dias para o roadmap.',
        'Funciona para equipe pequena?', 'Sim. O plano Starter cobre 1 módulo e setup básico para pequenos times.',
        'Vocês fazem a implantação?', 'Sim. Inclui configuração, integração e treino de corretores.',
        'Como medir o retorno?', 'Por indicadores: redução de retrabalho, aumento de leads qualificados e conversão.',
    ],
    'planos-proptech-2026.html': [
        'Posso mudar de plano depois?', 'Sim. Ajuste conforme a imobiliária crescer, sem migração complexa.',
        'Tem fidelidade?', 'Não. Mensal, com cancelamento sem multa a partir do 2º mês.',
        'O plano inclui implementação?', 'Starter inclui setup básico; Professional e Enterprise incluem onboarding.',
        'Atende imobiliária pequena?', 'Sim. O Starter foi pensado para operações enxutas do litoral.',
        'Como contratar?', 'Por WhatsApp, e-mail ou formulário na página de planos.',
    ],
}

faq_tpl = '''
      <div class="card">
        <h2>Perguntas frequentes</h2>
        <div class="faq">
          {items}
        </div>
      </div>
'''

detail_tpl = '''          <details>
            <summary>{q}</summary>
            <p style="color:#334155;">{a}</p>
          </details>
'''

for page, qas in faq_map.items():
    if len(qas) % 2 != 0:
        raise SystemExit(f'FAQ inválida em {page}: número ímpar de itens')
    path = BASE / page
    if not path.exists():
        print('missing', page)
        continue
    text = path.read_text(encoding='utf-8')
    if 'Perguntas frequentes' in text:
        print('skip faq', page)
        continue
    items = ''.join(detail_tpl.format(q=qas[i], a=qas[i+1]) for i in range(0, len(qas), 2))
    block = faq_tpl.format(items=items)
    if '</div>\n  </div>' not in text:
        print('skip structure', page)
        continue
    text = text.replace('</div>\n  </div>', block + '    </div>\n  </div>', 1)
    path.write_text(text, encoding='utf-8')
    print('updated', page)
