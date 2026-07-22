# Guia de Implantação B2B — Praia Digital
> Pacote completo de serviços para imobiliárias do litoral de SP

## ✅ Serviços Operacionais no Runner Diário
- `automacao-imobiliarias.html` — Automação de e-mails, atendimento e prospecção
- `captacao-imoveis-litoral.html` — Captação Digital
- `solucao-proptech-unificada.html` — Solução Proptech Unificada
- `descricao-imoveis-ia.html` — Geração de Descrições com IA
- `seo-local-imobiliarias.html` — SEO Local
- `consultoria-transformacao-digital-imobiliarias.html` — Consultoria de Transformação Digital
- `avaliacao-preco-imoveis.html` — Avaliação de Preço com IA

## 📦 Artefatos B2B Criados
- `outreach/template-<servico>-2026.html` — cold outreach por serviço (7 templates)
- `outreach/roteiro-reels-shorts-<servico>-2026.html` — roteiros curtos (7 arquivos)
- `outreach/notificacao-b2b-pronta-2026-07-22.html` — modelo de notificação consolidada
- `faq-<servico>-2026.html` — FAQs por serviço (7 arquivos)
- `docs/sales/verificacao-integridade-b2b-2026-07-22.html`
- `docs/sales/checklist-seo-tecnico-b2b-2026-07-22.html`
- `docs/sales/checklist-lancamento-piloto-automacao-2026-07-22.html`
- `proposta-comercial-padrao-2026.html`
- `scripts/automation/add_canonical_and_description.py`
- `scripts/automation/integrate_faqs.py`
- `scripts/automation/notificar_vendas_b2b.py`

## 📊 Estrutura de Arquivos por Serviço
Cada serviço B2B inclui:
- `lote-b2b-<servico>-2026-07-22.csv` — Leads validados
- `lote-b2b-<servico>-sanitizado-2026-07-22.csv` — Leads sem duplicatas
- `followup-pairs-<servico>-2026-07-22.csv` — Follow-ups automáticos
- `tracker-<servico>-2026-07-22.csv` — Acompanhamento
- `para-brevo-<servico>-2026-07-22.csv` — CSV para e-mail (Brevo)
- `para-whatsapp-<servico>-2026-07-22.csv` — CSV para WhatsApp
- `checklist-envio-<servico>-2026-07-22.txt` — Checklist de envio

## 🚀 Passos de Implantação

### 1. Atualizar o `batch-sent-log.csv`
Editar o arquivo `docs/sales/batch-sent-log.csv` para registrar data, serviço, canal, quantidade de leads e status.

### 2. Importar CSVs nas Ferramentas Externas
- **Brevo (e-mail)**: importar `para-brevo-<servico>-2026-07-22.csv`
- **WhatsApp**: importar `para-whatsapp-<servico>-2026-07-22.csv`

### 3. Atualizar Status nos Trackers
Após envio, atualizar o campo `Status` nos arquivos:
- `docs/sales/csv-lotes-b2b/tracker-<servico>-2026-07-22.csv`

### 4. Acompanhar Follow-ups Automáticos
- **D0** (2026-07-22): envio inicial
- **D2** (2026-07-24): follow-up 1
- **D5** (2026-07-27): follow-up 2

Os scripts estão na pasta `scripts/automation/` e rodam via runner diário `automacao-diaria-runner` às 08:00.

## 📈 Métricas Esperadas (conforme relatório)
| Serviço | Leads | Valor Estimado |
|---------|-------|----------------|
| Automação | 8 | R$ 11.447,00 |
| Captação | 8 | R$ 11.920,00 |
| Solução Proptech | 8 | R$ 19.920,00 |
| Descrição Imóveis | 8 | R$ 3.920,00 |
| SEO Local | 8 | R$ 7.120,00 |
| Consultoria | 8 | R$ 11.920,00 |
| Avaliação Preço | 8 | R$ 11.920,00 |

## 🔗 Navegação B2B Integrada
- `index.html`: footer com links para todos os serviços
- `servicos-ia-imobiliarias.html`: central com cards de serviços
- `ia/index.html`: cards de cada serviço B2B
- Cross-sells aplicados em todas as landings B2B
- Sitemap atualizado com todas as URLs

## 📋 Checklist Diário
- [ ] Executar `python scripts/automation/run_vendas_do_dia.py`
- [ ] Verificar relatório em `docs/sales/relatorio-performance-b2b-YYYY-MM-DD.html`
- [ ] Acompanhar status dos trackers
- [ ] Atualizar `batch-sent-log.csv` com envios realizados
- [ ] Revisar respostas e agendar follow-ups adicionais se necessário

## 📁 Estrutura de Pastas
```
praia-digital/
├── automacao-imobiliarias.html
├── captacao-imoveis-litoral.html
├── solucao-proptech-unificada.html
├── descricao-imoveis-ia.html
├── seo-local-imobiliarias.html
├── avaliacao-preco-imoveis.html
├── consultoria-transformacao-digital-imobiliarias.html
├── planos-proptech-2026.html
├── sitemap.xml
├── docs/sales/csv-lotes-b2b/
├── scripts/automation/
│   ├── run_vendas_do_dia.py
│   └── [scripts por serviço]
└ outreach/
   └── template-<servico>-2026.html
```

## 🔧 Suporte
Para dúvidas ou ajustes, consulte os scripts em `scripts/automation/` ou edite diretamente as landings HTML.
