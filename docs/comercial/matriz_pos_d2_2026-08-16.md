# Matriz de leitura pós-D2 — Motor A
Data de referência: 2026-08-16
D2 alvo: 2026-08-17 09:00
Leads: 9, 11, 14, 15, 27, 29

## Objetivo
Ler o estado pós-D2 sem alterar leads nem simular execução. Cada lead mantém o status `ENVIADO_D0` até a execução real do script `scripts/executar_d2_2026-08-17.py`.

---

## 1. Snapshot pré-D2 dos leads

| lead_id | bairro | canal | score | serviço_potencial | preço | d0_enviado_em | status_atual |
|---------|--------|-------|-------|-------------------|-------|---------------|--------------|
| 9 | Juquehy | OLX | 82 | Fotografia + Edição de anúncio | R$ 700+ / R$ 497 | 2026-08-15 | ENVIADO_D0 |
| 11 | Indaiá | OLX | 80 | Fotografia + Edição de anúncio | R$ 700+ / R$ 497 | 2026-08-15 | ENVIADO_D0 |
| 14 | Indaiá | Instagram | 83 | Fotografia + Edição de anúncio | R$ 700+ / R$ 497 | 2026-08-15 | ENVIADO_D0 |
| 15 | Bertioga Centro | Facebook | 79 | Edição de anúncio + Administração Airbnb | R$ 497 / 10–15% | 2026-08-15 | ENVIADO_D0 |
| 27 | Bertioga | Instagram | 84 | Administração Airbnb/temporada | 10–15% | 2026-08-15 | ENVIADO_D0 |
| 29 | Bertioga Centro | Facebook | 76 | Administração Airbnb + Edição de anúncio | 10–15% / R$ 497 | 2026-08-15 | ENVIADO_D0 |

---

## 2. Sinais Motor B locais relevantes por lead

O rastreamento local (`assets/tracking-motor-b.js`) escuta `page_view`, `whatsapp_click`, `form_submit` e `custom_click` em páginas-alvo. Para os leads D2, os sinais aplicáveis são:

### 2.1 WhatsApp click
- **Quando acontece:** lead clica em CTA de WhatsApp em página instrumentada.
- **Leads com maior probabilidade:** 9 (OLX/WhatsApp), 11 (OLX/WhatsApp), 14 (Instagram/WhatsApp), 15 (Facebook/WhatsApp), 27 (Instagram/WhatsApp), 29 (Facebook/WhatsApp).
- **Significado comercial:** intenção de contato direto; acelerar para handoff humano.

### 2.2 Form submit
- **Quando acontece:** lead envia formulário de cadastro/diagnóstico em página instrumentada.
- **Significado comercial:** pedido formal; mapear para `RESPONDENDO_PRECO` ou `AGENDAMENTO_HUMANO` dependendo do serviço e campos.

### 2.3 Page view
- **Quando acontece:** lead visita página-alvo (`/diagnosticos-anfitrioes.html`, `/assets/cadastro-imovel-publico.html`, etc.).
- **Significado comercial:** aquecimento; manter na sequência D5/D10.

### 2.4 Custom click
- **Quando acontece:** clique em elemento com `data-motor-b-event`.
- **Significado comercial:** micro-conversão; usar como reforço de intenção na classificação.

---

## 3. Matriz de leitura: D2 → resposta → decisão

Regras aplicáveis (origem: `docs/comercial/fluxo_resposta_2026-08-15.md` e `docs/comercial/matriz_resposta_comercial_2026-08-15.md`):

| resposta_do_lead | decisão_automatica | acao_humana | proximo_passo_motor_a |
|------------------|--------------------|-------------|------------------------|
| ✅ Positiva | `HANDOFF_HUMANO` | comercial@praia.digital / (11) 95434-6288 | parar follow-up |
| 💰 Pediu preço | `RESPONDENDO_PRECO` | responder com preço aprovado | continuar follow-up após resposta |
| 📅 Pediu agendamento | `AGENDAMENTO_HUMANO` | confirmar disponibilidade | parar follow-up |
| ❌ Negativa | `ENCERRADO` | nenhuma | parar follow-up |
| 🛑 Bloqueio | `BLOQUEADO` | nenhuma | parar follow-up |
| ⏳ Sem resposta (até D5) | `SEGUINDO_SEQUENCIA` | nenhuma | D5 em 20/08 |

---

## 4. Perfil de decisão por lead (D2 → cenário)

### Lead 9 — Juquehy (OLX)
- **Score:** 82 | **Serviço:** Fotografia + Edição de anúncio | **Preço:** R$ 700+ / R$ 497
- **Canal D2:** OLX/WhatsApp
- **Contexto D0:** Anúncio direto, casa 4 quartos com piscina, WhatsApp público, fotos básicas esperadas.
- **Sinais Motor B esperados:** `whatsapp_click` (alta probabilidade), `page_view` se visitar landing de fotografia.
- **Decisão pós-D2:**
  - Se responder positivamente → `HANDOFF_HUMANO` (proposta fotografia + edição).
  - Se pedir preço → `RESPONDENDO_PRECO` (preço fechado: R$ 497 edição, R$ 700+ fotografia).
  - Se pedir agendamento → `AGENDAMENTO_HUMANO` (alinhar briefing e data).
  - Se não responder → `SEGUINDO_SEQUENCIA` → D5.
  - Se negar → `ENCERRADO`.

### Lead 11 — Indaiá (OLX)
- **Score:** 80 | **Serviço:** Fotografia + Edição de anúncio | **Preço:** R$ 700+ / R$ 497
- **Canal D2:** OLX/WhatsApp
- **Contexto D0:** Casa 3 quartos a 600m da praia, anúncio simples, proprietário direto.
- **Sinais Motor B esperados:** `whatsapp_click`, `form_submit` se preencher cadastro.
- **Decisão pós-D2:**
  - Positiva → `HANDOFF_HUMANO` (fotografia + edição).
  - Pedido de preço → `RESPONDENDO_PRECO` (mesma tabela do Lead 9).
  - Pedido de agendamento → `AGENDAMENTO_HUMANO`.
  - Sem resposta → `SEGUINDO_SEQUENCIA` → D5.
  - Negativa → `ENCERRADO`.

### Lead 14 — Indaiá (Instagram)
- **Score:** 83 | **Serviço:** Fotografia + Edição de anúncio | **Preço:** R$ 700+ / R$ 497
- **Canal D2:** Instagram/WhatsApp
- **Contexto D0:** Casa 150m da praia, R$650/dia público, perfil Instagram ativo, estrutura visual esperada amadora.
- **Sinais Motor B esperados:** `whatsapp_click`, `custom_click` se houver CTA no reel/página, `page_view`.
- **Decisão pós-D2:**
  - Positiva → `HANDOFF_HUMANO` (fotografia + edição + possível agendamento presencial).
  - Pedido de preço → `RESPONDENDO_PRECO`.
  - Pedido de agendamento → `AGENDAMENTO_HUMANO` (sugerir visita para briefing).
  - Sem resposta → `SEGUINDO_SEQUENCIA` → D5.
  - Negativa → `ENCERRADO`.

### Lead 15 — Bertioga Centro (Facebook)
- **Score:** 79 | **Serviço:** Edição de anúncio + Administração Airbnb | **Preço:** R$ 497 / 10–15%
- **Canal D2:** Facebook/WhatsApp
- **Contexto D0:** WhatsApp público, anúncio manual, alta oportunidade de gestão profissional.
- **Sinais Motor B esperados:** `whatsapp_click`, `form_submit` se houver formulário de diagnóstico.
- **Decisão pós-D2:**
  - Positiva → `HANDOFF_HUMANO` (edição + administração; propor diagnóstico rápido).
  - Pedido de preço → `RESPONDENDO_PRECO` (R$ 497 edição + 10–15% administração).
  - Pedido de agendamento → `AGENDAMENTO_HUMANO` (alinhar início da gestão).
  - Sem resposta → `SEGUINDO_SEQUENCIA` → D5.
  - Negativa → `ENCERRADO`.

### Lead 27 — Temporada Bertioga (Instagram)
- **Score:** 84 | **Serviço:** Administração Airbnb/temporada | **Preço:** 10–15%
- **Canal D2:** Instagram/WhatsApp
- **Contexto D0:** 10+ anos de experiência, WhatsApp direto, alta evidência de gestão manual, perfil institucional.
- **Sinais Motor B esperados:** `whatsapp_click` (forte), `page_view` se acessar landing de administração.
- **Decisão pós-D2:**
  - Positiva → `HANDOFF_HUMANO` (proposta de administração completa; lead de alto valor).
  - Pedido de preço → `RESPONDENDO_PRECO` (10–15% sobre faturamento; propor modelo de governança).
  - Pedido de agendamento → `AGENDAMENTO_HUMANO` (reunião de diagnóstico operacional).
  - Sem resposta → `SEGUINDO_SEQUENCIA` → D5.
  - Negativa → `ENCERRADO`.

### Lead 29 — Bertioga Aluga (Facebook)
- **Score:** 76 | **Serviço:** Administração Airbnb + Edição de anúncio | **Preço:** 10–15% / R$ 497
- **Canal D2:** Facebook/WhatsApp
- **Contexto D0:** Grupo Facebook com WhatsApp público, anúncios manuais, gestão manual evidente.
- **Sinais Motor B esperados:** `whatsapp_click`, `form_submit` se converter por formulário.
- **Decisão pós-D2:**
  - Positiva → `HANDOFF_HUMANO` (administração + edição; pacote combinado).
  - Pedido de preço → `RESPONDENDO_PRECO` (R$ 497 edição + 10–15% administração).
  - Pedido de agendamento → `AGENDAMENTO_HUMANO` (alinhar pacote e início).
  - Sem resposta → `SEGUINDO_SEQUENCIA` → D5.
  - Negativa → `ENCERRADO`.

---

## 5. Mapa consolidado D2 → decisão

| lead_id | tipo_resposta_esperada | decisao_automatica | acao_humana | motor_b_sinal_chave | prioridade_pos_d2 |
|---------|------------------------|--------------------|-------------|---------------------|-------------------|
| 9 | Positiva | HANDOFF_HUMANO | comercial@praia.digital | whatsapp_click | Alta (score 82, OLX) |
| 9 | Pediu preço | RESPONDENDO_PRECO | responder preço aprovado | form_submit | Alta |
| 9 | Sem resposta | SEGUINDO_SEQUENCIA | nenhuma | page_view | Média |
| 11 | Positiva | HANDOFF_HUMANO | comercial@praia.digital | whatsapp_click | Alta (score 80, OLX) |
| 11 | Pediu preço | RESPONDENDO_PRECO | responder preço aprovado | form_submit | Alta |
| 11 | Sem resposta | SEGUINDO_SEQUENCIA | nenhuma | page_view | Média |
| 14 | Positiva | HANDOFF_HUMANO | comercial@praia.digital | whatsapp_click | Alta (score 83, Instagram) |
| 14 | Pediu preço | RESPONDENDO_PRECO | responder preço aprovado | form_submit | Alta |
| 14 | Sem resposta | SEGUINDO_SEQUENCIA | nenhuma | custom_click/page_view | Média |
| 15 | Positiva | HANDOFF_HUMANO | comercial@praia.digital | whatsapp_click | Alta (score 79, gestão) |
| 15 | Pediu preço | RESPONDENDO_PRECO | responder preço aprovado | form_submit | Alta |
| 15 | Sem resposta | SEGUINDO_SEQUENCIA | nenhuma | page_view | Média |
| 27 | Positiva | HANDOFF_HUMANO | comercial@praia.digital | whatsapp_click | Máxima (score 84, admin) |
| 27 | Pediu preço | RESPONDENDO_PRECO | responder preço aprovado | form_submit | Máxima |
| 27 | Sem resposta | SEGUINDO_SEQUENCIA | nenhuma | page_view | Alta |
| 29 | Positiva | HANDOFF_HUMANO | comercial@praia.digital | whatsapp_click | Alta (score 76, pacote) |
| 29 | Pediu preço | RESPONDENDO_PRECO | responder preço aprovado | form_submit | Alta |
| 29 | Sem resposta | SEGUINDO_SEQUENCIA | nenhuma | page_view | Média |

---

## 6. Critérios de leitura pós-D2 (checklist)

1. **Não alterar leads antes da execução.** O status só muda para `ENVIADO_D2` após `python scripts/executar_d2_2026-08-17.py`.
2. **Registrar resposta individualmente** em `docs/comercial/resultado_d2_2026-08-17.md` quando houver.
3. **Motor B local:** consultar `localStorage.getItem('motor_b_events_v1')` nas páginas-alvo para capturar `whatsapp_click`, `form_submit`, `page_view`, `custom_click`.
4. **Classificar por resposta** usando a matriz de resposta comercial (`docs/comercial/matriz_resposta_comercial_2026-08-15.md`).
5. **Atualizar CRM** com `tipo_resposta`, `servico_interesse`, `valor_potencial`, `estagio`, `proxima_acao` e `responsavel`.
6. **Handoff humano** apenas para positivas, pedidos de preço e agendamentos. Respostas negativas e bloqueios encerram automaticamente.
7. **Sem resposta** → manter `SEGUINDO_SEQUENCIA` e agendar D5 para 20/08.

---

## 7. Rastreabilidade

- Script de execução D2: `scripts/executar_d2_2026-08-17.py`
- Rastreamento Motor B local: `assets/tracking-motor-b.js`
- Leads fonte: `docs/comercial/leads_sao_sebastiao_bertioga.csv`
- Resultado D2: `docs/comercial/resultado_d2_2026-08-17.md`
- Regras de resposta: `docs/comercial/fluxo_resposta_2026-08-15.md`
- Matriz de resposta comercial: `docs/comercial/matriz_resposta_comercial_2026-08-15.md`
