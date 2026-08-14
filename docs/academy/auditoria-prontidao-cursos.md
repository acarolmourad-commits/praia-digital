# Auditoria de Prontidão dos Cursos — Praia Digital Academy

## Política de prontidão

Nenhum curso pode ser vendido sem evidência concreta de que todo o material prometido existe, está completo e pode ser entregue após confirmação do pagamento.

"Publicado" ≠ "pronto para entrega".

## Critérios de classificação

🟢 PRONTO_PARA_VENDA
- conteúdo completo;
- material existente e não vazio;
- estrutura coerente;
- entrega possível imediatamente;
- nenhuma pendência crítica.

🟡 REVISAR_ANTES_DE_VENDER
- conteúdo parcialmente disponível;
- pequena pendência;
- entrega possível, mas não deve ser liberada sem correção.

🔴 BLOQUEAR_VENDA
- conteúdo ausente ou módulos faltantes;
- material prometido inexistente;
- entrega impossível;
- inconsistência grave entre produto e conteúdo.

## Resultado da auditoria — 2026-08-14

Total de cursos auditados: 64

| Classificação | Quantidade |
|---|---|
| PRONTO_PARA_VENDA | 0 |
| REVISAR_ANTES_DE_VENDER | 64 |
| BLOQUEAR_VENDA | 0 |

### Pendências encontradas

1. **estudos_caso faltante** — 64/64 cursos
   - Nenhum curso possui diretório `estudos-caso/` com conteúdo.
   - Item obrigatório na ficha de planejamento de cada curso.
   - Ação: criar material de estudos de caso para cada curso.

2. **google_ads parcial** — 64/64 cursos
   - Arquivo `marketing/google-ads.md` existe em todos os cursos.
   - Conteúdo mínimo: apenas metadados, sem plano de campanha completo.
   - Ação: expandir com palavras-chave, orçamento, criativos e métricas.

### Cursos amarelos

Todos os 64 cursos estão em REVISAR_ANTES_DE_VENDER.

### Cursos vermelhos

Nenhum curso bloqueado atualmente.

## Fluxo de entrega pós-pagamento

PAGAMENTO APROVADO
        ↓
identificar produto/curso
        ↓
validar compra
        ↓
identificar curso adquirido
        ↓
liberar acesso/material
        ↓
enviar e-mail ao comprador
        ↓
registrar entrega

### Regras

- Entregar apenas quando status = paid.
- Não liberar conteúdo em: pending, refused, cancelled, abandoned, error.
- Webhook deve ser idempotente.
- Comprador recebe somente o que comprou.

## E-mail de entrega

Assunto: "Seu acesso à Praia Digital Academy está liberado"

Corpo:
- confirmação da compra;
- nome do curso;
- identificação do comprador;
- instruções de acesso;
- link seguro para acessar o material;
- suporte.

Implementação atual: `academy/core/email_service.py:send_enrollment_confirmation`

## Segurança da entrega

- Autenticação: JWT Bearer
- Autorização: matrícula ativa vinculada ao usuário
- Impossibilidade de acessar outro curso
- Webhook com verificação HMAC
- Idempotência garantida por `payment_id` + `enrollment_id`

## Testes

Testes existentes:
- `academy/tests/test_pilot_fotografia_edicao.py` — 3/3 passando
- `academy/tests/test_phase1.py` — 1/2 passando
- `academy/tests/test_payment_sandbox_flow.py` — OK
- `academy/tests/test_checkout_public.py` — OK

Testes adicionais necessários:
- Pagamento aprovado → curso liberado → e-mail enviado
- Pagamento pendente → nenhum acesso
- Pagamento recusado → nenhum acesso
- Webhook duplicado → apenas uma entrega
- Curso inexistente/inativo → erro registrado

## Ação recomendada

1. Criar conteúdo de estudos de caso para cada um dos 64 cursos em `education/cursos/<slug>/estudos-caso/`
2. Revisar `marketing/google-ads.md` para incluir plano de campanha completo
3. Re-executar auditoria após correções
4. Apenas então, liberar vendas

## Arquivos de referência

- `education/auditoria-completa.json` — auditoria detalhada por curso
- `education/auditoria-final.json` — resumo executivo
- `education/cursos/` — diretório de cursos
- `academy/core/conversion.py` — operador de conversão genérico
- `academy/core/payments/service.py` — serviço de pagamentos
- `academy/core/payments/webhooks.py` — webhook com verificação HMAC
- `academy/core/email_service.py` — e-mail transacional
