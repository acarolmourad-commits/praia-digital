# D2 → Decisão automática — Motor A
Data de referência: 2026-08-16
Execução D2: 2026-08-17 09:00
Leads: 9, 11, 14, 15, 27, 29

## Princípio
Este arquivo é um mapeamento estático de decisão. Não altera leads, não simula execução e não envia mensagens. Ele documenta qual decisão deve ser tomada para cada combinação `lead × resposta`, servindo como referência para a execução humana e automática pós-D2.

---

## Regras gerais de decisão

| Resposta do lead | Decisão automática | Responsável | Ação subsequente |
|------------------|--------------------|-------------|------------------|
| ✅ Positiva | `HANDOFF_HUMANO` | Humano | Entrar em contato via comercial@praia.digital / (11) 95434-6288 |
| 💰 Pediu preço | `RESPONDENDO_PRECO` | Humano | Responder com preço aprovado e aguardar decisão |
| 📅 Pediu agendamento | `AGENDAMENTO_HUMANO` | Humano | Confirmar disponibilidade |
| ❌ Negativa | `ENCERRADO` | — | Parar follow-up |
| 🛑 Bloqueio / Não quero contato | `BLOQUEADO` | — | Parar follow-up |
| ⏳ Sem resposta até D5 | `SEGUINDO_SEQUENCIA` | Automático | Executar D5 em 20/08 |
| Objeção classficada | `AGUARDANDO` | Automático | Manter na sequência ou escalar conforme matriz |

---

## Decisão por lead

### Lead 9 — Juquehy (OLX)
- **Status pré-D2:** `ENVIADO_D0` (2026-08-15)
- **Score:** 82
- **Serviço:** Fotografia + Edição de anúncio
- **Canal:** OLX/WhatsApp
- **Preço:** R$ 700+ (fotografia) / R$ 497 (edição)

| Cenário pós-D2 | Decisão | Próxima ação |
|----------------|---------|--------------|
| Resposta positiva | `HANDOFF_HUMANO` | Proposta personalizada de fotografia + edição |
| Pediu preço | `RESPONDENDO_PRECO` | Enviar valores: R$ 497 (edição) e/ou R$ 700+ (fotografia) |
| Pediu agendamento | `AGENDAMENTO_HUMANO` | Alinhar briefing e data para sessão de fotos |
| Pediu informações | `AGUARDANDO` | Responder com dados específicos do anúncio Juquehy |
| Objeção: já tenho fotos | `AGUARDANDO` | Educação/comparação; follow-up D5 |
| Objeção: eu mesmo faço | `AGUARDANDO` | Diagnóstico de resultado; follow-up D5 |
| Objeção: muito caro | `AGUARDANDO` | ROI por diária; follow-up D5 |
| Sem resposta | `SEGUINDO_SEQUENCIA` | D5 em 20/08 |
| Negativa | `ENCERRADO` | Nenhuma ação |
| Bloqueio | `BLOQUEADO` | Nenhuma ação |

---

### Lead 11 — Indaiá (OLX)
- **Status pré-D2:** `ENVIADO_D0` (2026-08-15)
- **Score:** 80
- **Serviço:** Fotografia + Edição de anúncio
- **Canal:** OLX/WhatsApp
- **Preço:** R$ 700+ (fotografia) / R$ 497 (edição)

| Cenário pós-D2 | Decisão | Próxima ação |
|----------------|---------|--------------|
| Resposta positiva | `HANDOFF_HUMANO` | Proposta personalizada de fotografia + edição |
| Pediu preço | `RESPONDENDO_PRECO` | Enviar valores: R$ 497 (edição) e/ou R$ 700+ (fotografia) |
| Pediu agendamento | `AGENDAMENTO_HUMANO` | Alinhar briefing e data |
| Pediu informações | `AGUARDANDO` | Responder com dados específicos do anúncio Indaiá |
| Objeção: já tenho fotos | `AGUARDANDO` | Educação/comparação; follow-up D5 |
| Objeção: eu mesmo faço | `AGUARDANDO` | Diagnóstico de resultado; follow-up D5 |
| Objeção: muito caro | `AGUARDANDO` | ROI por diária; follow-up D5 |
| Sem resposta | `SEGUINDO_SEQUENCIA` | D5 em 20/08 |
| Negativa | `ENCERRADO` | Nenhuma ação |
| Bloqueio | `BLOQUEADO` | Nenhuma ação |

---

### Lead 14 — Indaiá (Instagram)
- **Status pré-D2:** `ENVIADO_D0` (2026-08-15)
- **Score:** 83
- **Serviço:** Fotografia + Edição de anúncio
- **Canal:** Instagram/WhatsApp
- **Preço:** R$ 700+ (fotografia) / R$ 497 (edição)

| Cenário pós-D2 | Decisão | Próxima ação |
|----------------|---------|--------------|
| Resposta positiva | `HANDOFF_HUMANO` | Proposta de fotografia + edição; sugerir agendamento presencial |
| Pediu preço | `RESPONDENDO_PRECO` | Enviar valores: R$ 497 (edição) e/ou R$ 700+ (fotografia) |
| Pediu agendamento | `AGENDAMENTO_HUMANO` | Confirmar visita para briefing |
| Pediu informações | `AGUARDANDO` | Responder com dados específicos do perfil Instagram |
| Objeção: já tenho fotos | `AGUARDANDO` | Educação/comparação; follow-up D5 |
| Objeção: eu mesmo faço | `AGUARDANDO` | Diagnóstico de resultado; follow-up D5 |
| Objeção: muito caro | `AGUARDANDO` | ROI por diária; follow-up D5 |
| Sem resposta | `SEGUINDO_SEQUENCIA` | D5 em 20/08 |
| Negativa | `ENCERRADO` | Nenhuma ação |
| Bloqueio | `BLOQUEADO` | Nenhuma ação |

---

### Lead 15 — Bertioga Centro (Facebook)
- **Status pré-D2:** `ENVIADO_D0` (2026-08-15)
- **Score:** 79
- **Serviço:** Edição de anúncio + Administração Airbnb
- **Canal:** Facebook/WhatsApp
- **Preço:** R$ 497 (edição) / 10–15% (administração)

| Cenário pós-D2 | Decisão | Próxima ação |
|----------------|---------|--------------|
| Resposta positiva | `HANDOFF_HUMANO` | Proposta de edição + administração; enviar diagnóstico rápido |
| Pediu preço | `RESPONDENDO_PRECO` | Enviar valores: R$ 497 (edição) + 10–15% (administração) |
| Pediu agendamento | `AGENDAMENTO_HUMANO` | Alinhar início da gestão |
| Pediu informações | `AGUARDANDO` | Responder com dados específicos de administração Airbnb |
| Objeção: já tenho gestor | `AGUARDANDO` | Nutrir / reativar após 30 dias |
| Objeção: eu mesmo faço | `AGUARDANDO` | Educar / diagnóstico; follow-up D5 |
| Objeção: não quero gastar | `AGUARDANDO` | Educar / ROI; follow-up D5 |
| Objeção: vou pensar | `AGUARDANDO` | Follow-up D5/D10 |
| Sem resposta | `SEGUINDO_SEQUENCIA` | D5 em 20/08 |
| Negativa | `ENCERRADO` | Nenhuma ação |
| Bloqueio | `BLOQUEADO` | Nenhuma ação |

---

### Lead 27 — Temporada Bertioga (Instagram)
- **Status pré-D2:** `ENVIADO_D0` (2026-08-15)
- **Score:** 84
- **Serviço:** Administração Airbnb/temporada
- **Canal:** Instagram/WhatsApp
- **Preço:** 10–15%

| Cenário pós-D2 | Decisão | Próxima ação |
|----------------|---------|--------------|
| Resposta positiva | `HANDOFF_HUMANO` | Proposta de administração completa (governança, preço, disponibilidade) |
| Pediu preço | `RESPONDENDO_PRECO` | Enviar modelo 10–15% sobre faturamento; explicar governança |
| Pediu agendamento | `AGENDAMENTO_HUMANO` | Reunião de diagnóstico operacional |
| Pediu informações | `AGUARDANDO` | Responder com dados de gestão profissional e cases |
| Objeção: já tenho gestor | `AGUARDANDO` | Nutrir / reativar após 30 dias |
| Objeção: eu mesmo faço | `AGUARDANDO` | Diagnóstico de resultado; follow-up D5 |
| Objeção: muito caro | `AGUARDANDO` | ROI por aumento de avaliações e ocupação; follow-up D5 |
| Objeção: não preciso mexer agora | `AGUARDANDO` | Nutrir / reativar antes da alta temporada |
| Sem resposta | `SEGUINDO_SEQUENCIA` | D5 em 20/08 |
| Negativa | `ENCERRADO` | Nenhuma ação |
| Bloqueio | `BLOQUEADO` | Nenhuma ação |

---

### Lead 29 — Bertioga Aluga (Facebook)
- **Status pré-D2:** `ENVIADO_D0` (2026-08-15)
- **Score:** 76
- **Serviço:** Administração Airbnb + Edição de anúncio
- **Canal:** Facebook/WhatsApp
- **Preço:** 10–15% (administração) / R$ 497 (edição)

| Cenário pós-D2 | Decisão | Próxima ação |
|----------------|---------|--------------|
| Resposta positiva | `HANDOFF_HUMANO` | Proposta de pacote combinado administração + edição |
| Pediu preço | `RESPONDENDO_PRECO` | Enviar valores: R$ 497 (edição) + 10–15% (administração) |
| Pediu agendamento | `AGENDAMENTO_HUMANO` | Alinhar pacote e início |
| Pediu informações | `AGUARDANDO` | Responder com dados específicos do grupo Bertioga Aluga |
| Objeção: já tenho gestor | `AGUARDANDO` | Nutrir / reativar após 30 dias |
| Objeção: eu mesmo faço | `AGUARDANDO` | Educar / diagnóstico; follow-up D5 |
| Objeção: muito caro | `AGUARDANDO` | ROI por diária; follow-up D5 |
| Objeção: vou pensar | `AGUARDANDO` | Follow-up D5/D10 |
| Sem resposta | `SEGUINDO_SEQUENCIA` | D5 em 20/08 |
| Negativa | `ENCERRADO` | Nenhuma ação |
| Bloqueio | `BLOQUEADO` | Nenhuma ação |

---

## 8. Integração com Motor B local

Quando a execução D2 ocorrer em 2026-08-17, a leitura pós-D2 deve cruzar:

1. **localStorage** (`motor_b_events_v1`) nas páginas-alvo para capturar `whatsapp_click` e `form_submit`.
2. **CRM** (`leads_sao_sebastiao_bertioga.csv`) para verificar se `resposta`, `tipo_resposta` e `servico_interesse` foram preenchidos.
3. **resultado_d2_2026-08-17.md** para validar se o disparo ocorreu.

Prioridade de sinal para decisão:
1. Resposta explícita no CRM > 2. Evento Motor B > 3. Sem resposta → D5.

---

## 9. Referências

- Script D2: `scripts/executar_d2_2026-08-17.py`
- Rastreamento Motor B: `assets/tracking-motor-b.js`
- Leads: `docs/comercial/leads_sao_sebastiao_bertioga.csv`
- Regras de resposta: `docs/comercial/fluxo_resposta_2026-08-15.md`
- Matriz de resposta: `docs/comercial/matriz_resposta_comercial_2026-08-15.md`
- Resultado D2: `docs/comercial/resultado_d2_2026-08-17.md`
- Matriz de leitura: `docs/comercial/matriz_pos_d2_2026-08-16.md`
