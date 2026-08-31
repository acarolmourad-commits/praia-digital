# Checklist Follow-Up — Lote Manual 18 Leads

> Use este checklist para a rodada manual de hoje. Marque o status real após cada envio. NÃO apague esta estrutura.

## Autorização Gmail (Composio)
- Link de autorização: https://connect.composio.dev/link/lk_3Nhfpx6OssVq
- Account ID: `ca_9JeFN2KV3Nu2`
- Status atual: `INITIALIZATING`
- Ação necessária: abrir o link acima, autorizar Gmail e confirmar retorno para `ACTIVE`.
- Observação: o Composio CLI roda no WSL; após conexão ativa, o próximo ciclo de `GMAIL_SEND_EMAIL` pode ser disparado automaticamente via script WSL + agendamento.

---

## Mapeamento Instagram / PSIDs
- Conta ativa disponível: `instagram_plated-tickey` (`ACTIVE`).
- Tools úteis:
  - `INSTAGRAM_LIST_ALL_CONVERSATIONS` → listar conversas.
  - `INSTAGRAM_LIST_ALL_MESSAGES` → mensagens de uma conversa e descobrir `recipient_id`.
- Estratégia: para leads 6, 14, 22, 23, 26 e 27, a primeira interação manual por DM no Instagram costuma criar o PSID; depois disso, automação é possível.

---

## Disparos manuais da rodada de hoje

Base link com UTM: `https://praia.digital/hub/ia-corretores-litoral/?utm_source=followup&utm_medium=whatsapp&utm_campaign=sao_sebastiao_bertioga`

| # | Lead | Cidade | Canal | Link rastreável | Status | Observações |
|---|------|--------|-------|-----------------|--------|-------------|
| 1 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 2 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 3 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 4 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 5 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 6 | [NOME] | [CIDADE] | instagram | [LINK UTM] | pendente | coletar PSID se DM |
| 7 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 8 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 9 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 10 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 11 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 12 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 13 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 14 | [NOME] | [CIDADE] | instagram | [LINK UTM] | pendente | coletar PSID se DM |
| 15 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 16 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 17 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |
| 18 | [NOME] | [CIDADE] | whatsapp | [LINK UTM] | pendente | |

### Regras de status
- `enviado`: mensagem enviada no canal.
- `entregue`: confirmação de entrega.
- `abriu_link`: clique/abertura mensurável.
- `respondeu`: resposta do lead.
- `convertido`: fechamento/agendamento.
- `erro`: falha no envio/entrega.

---

## Próximos passos automáticos
1. Você autoriza o Gmail no link acima.
2. Eu ajusto este checklist com os nomes reais da base.
3. Disparamos a rodada manual de hoje.
4. Depois, eu orquestro os fluxos automáticos:
   - Gmail: `GMAIL_SEND_EMAIL`
   - Instagram: `INSTAGRAM_SEND_TEXT_MESSAGE` com PSID mapeado
