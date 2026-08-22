# SECURITY HARDENING — FASE 1

Data: 2026-08-19
Status: PREPARAÇÃO — NÃO EXECUTAR AINDA
Referência: docs/auditoria/SECURITY_BASELINE.md

---

## Executive Summary

Transformar os achados P1/P2 da auditoria em plano executável, com causa, impacto, risco, teste, rollback e ordem de implementação.

Prioridade técnica:
1. Segredos potencialmente expostos e scanning
2. Webhook fail-closed
3. Admin auth hardening
4. CORS restrito
5. Payment logging redaction
6. Orchestrator/cron least privilege
7. Supply chain hardening
8. Backup restore controlado
9. Testes de segurança permanentes

Nenhuma alteração será aplicada até autorização explícita.

---

## P1-1 — SECRETS

### O QUE?
Remover `.env` do versionamento, migrar segredos para vault/CI secrets, rotacionar credenciais suspeitas e implementar secret scanning contínuo.

### POR QUÊ?
Arquivo `.env` na raiz contém credenciais ativas de SMTP, Hotmart, Mercado Pago, WhatsApp e banco. Se commitado acidentalmente, causa exposição grave.

### EVIDÊNCIA
- `.env` presente na raiz.
- `.env.example` lista todas as chaves reais.
- `.gitignore` não confirmado como bloqueando `.env`.
- Git history não auditado nesta fase por timeout; assumir POTENCIALMENTE EXPOSTO até prova contrária.

### IMPACTO
Comprometimento de integrações externas, possível fraude em checkout/pagamentos, abuso de WhatsApp/SMTP.

### SERVIÇOS AFETADOS
- SMTP: envio de e-mails transacionais.
- Hotmart: checkout/notificação de pagamento.
- Mercado Pago: preferências de pagamento.
- WhatsApp: notificações de matrícula/certificado.
- Database: conexão da Academy.

### CAUSA
Segredos armazenados em arquivo local versionado ou passível de commit.

### ESTRATÉGIA
1. Inventariar todos os consumers de cada secret no código.
2. Migrar cada secret para GitHub Secrets / vault.
3. Rotacionar todos os segredos listados em `.env.example`.
4. Remover `.env` do histórico com `git filter-repo` ou equivalente; se inviável, rotacionar todos os segredos de qualquer forma.
5. Adicionar `.env` ao `.gitignore` e validar.
6. Habilitar secret scanning no GitHub.
7. Auditar artifacts/CI logs em busca de vazamento.

### ORDEM
Começar por SMTP e DB; depois Hotmart/Mercado Pago; depois WhatsApp.

### TESTE
- confirmar que `.env` não aparece em `git ls-files`.
- confirmar que nenhum consumer referencia path local de `.env`.
- CI health check sem secrets locais.

### ROLLBACK
Manter cópia dos valores antigos em local seguro offline até validação completa. Se deploy falhar, restaurar consumer anterior e reverter segredo antigo temporariamente.

### CRITÉRIO DE SUCESSO
Nenhum arquivo `.env` versionado; nenhum consumer usa secret local; scanning sem alertas.

---

## P1-2 — WEBHOOKS

### O QUE?
Tornar `verify_webhook()` fail-closed quando secret não configurado, adicionar replay protection e idempotência explícita.

### POR QUÊ?
Webhook pode aceitar eventos forjados se secret não estiver configurado no ambiente.

### EVIDÊNCIA
`academy/core/payments/webhooks.py`:
- Sandbox: sempre aceita.
- Hotmart: aceita se `HOTMART_TOKEN` vazio.
- Mercado Pago: aceita se `MERCADOPAGO_TOKEN` vazio.
- Stripe: aceita se `STRIPE_SECRET` vazio.

### IMPACTO
Um atacante que descubra a URL do webhook pode forjar eventos de pagamento e liberar matrículas sem pagamento real.

### ATAQUE POSSÍVEL
Forjar payload `approved` para `/academy/payments/webhook` → cria/atualiza `Payment` para `paid` e ativa matrícula via `finalize_payment`.

### ESTRATÉGIA
1. Em produção, exigir secret configurado; se ausente, retornar 500 e logar alerta.
2. Implementar replay protection com timestamp/nonce e janela de 5 minutos.
3. Garantir idempotência por `enrollment_id` + `gateway_payment_id`.
4. Nunca retornar sucesso (`handled: True`) quando a verificação falhar.

### TESTE
- secret ausente + payload válido → 403/500.
- assinatura inválida → 403.
- replay com timestamp antigo → 403.
- mesmo evento repetido → idempotente.

### ROLLBACK
Reverter para versão anterior de `webhooks.py` e restaurar env var temporariamente. Dado que o comportamento atual já é permissivo, rollback não degrada segurança adicional.

### CRITÉRIO DE SUCESSO
Nenhum webhook processado sem verificação válida em produção.

---

## P1-3 — CORS

### O QUE?
Restringir `ALLOWED_ORIGINS` para domínios autorizados e impedir uso de `*` quando `allow_credentials=True`.

### POR QUÊ?
`academy/main.py` usa `allow_origins=["*"]` e `allow_credentials=True` quando `ALLOWED_ORIGINS="*"`.

### EVIDÊNCIA
`.env.example` lista:
- `https://praia.digital`
- `https://www.praia.digital`
- `https://academy.praia.digital`

### IMPACTO
Potencial CSRF/credential abuse cross-origin; navegador pode enviar cookies/credenciais de qualquer origem.

### ESTRATÉGIA
1. Definir allowlist mínima por ambiente em `.env`.
2. Em produção, rejeitar configuração `*`.
3. Remover `allow_credentials=True` se `*` for usado; alternativamente, restringir origins.
4. Adicionar teste em CI que valida config de CORS.

### TESTE
- origem permitida → `Access-Control-Allow-Origin` correto.
- origem não listada → sem header ou bloqueio.

### ROLLBACK
Restaurar configuração anterior de CORS; risco baixo, apenas possível quebra de origin confiável não listada.

### CRITÉRIO DE SUCESSO
Nenhuma resposta com `*` + `allow_credentials=True` em produção.

---

## P1-4 — ADMIN / RATE LIMIT / MFA

### O QUE?
Implementar rate-limit global, brute-force lock e MFA para admin.

### POR QUÊ?
`RateLimitMiddleware` só aplica em produção; admin não tem MFA nem lockout.

### EVIDÊNCIA
`academy/core/middleware.py`: rate limit desligado se `APP_ENV != production`.
`academy/core/security.py`: sem MFA, sem lockout.

### IMPACTO
Credential stuffing/admin takeover.

### ESTRATÉGIA
1. Aplicar rate-limit independente de env, com limites distintos para login e admin.
2. Adicionar brute-force lock por usuário/IP: ex: 5 falhas → bloqueio temporário.
3. Planejar MFA TOTP/WebAuthn para admin; não ativar ainda.
4. Logar eventos de auth com request_id.

### TESTE
- 10 logins inválidos seguidos → 429/lockout.
- admin com MFA ativado → login exige segundo fator.
- token ausente → 401 consistente.

### ROLLBACK
Desativar rate-limit/MFA por env var; dados de lockout podem ser limpos.

### CRITÉRIO DE SUCESSO
Nenhum endpoint de auth/admin sem proteção contra força bruta.

---

## P2-1 — ORCHESTRATOR / CRON LEAST PRIVILEGE

### O QUE?
Reduzir permissões de orquestrador e crons: remover push automático para main, evitar `shell=True`, limitar módulos carregáveis.

### POR QUÊ?
`orchestrator_central.py` e `orchestrator_24h.py` executam git push, subprocess shell e leem/escrevem arquivos amplamente.

### EVIDÊNCIA
- `git_commit_and_push()` faz push para `origin main`.
- `update_sitemap()` usa `shell=True`.
- `run_*` carregam módulos por path sem restrição além de `ALLOWED_*`.

### IMPACTO
Publicação/acidente automático; injeção via path; module hijack.

### ESTRATÉGIA
1. Remover push automático; exigir branch de deploy + PR.
2. Substituir `shell=True` por lista de args; validar paths contra allowlist.
3. Carregar módulos apenas por hash/assinatura ou path fixo declarado.
4. Isolar execução de módulos legados em subprocess com privilégio mínimo.

### TESTE
- módulo inexistente → erro sem execução.
- path malicioso → bloqueado.
- push automático desativado.

### ROLLBACK
Restaurar funções anteriores de git/subprocess; risco baixo.

### CRITÉRIO DE SUCESSO
Nenhuma execução automática com privilégio máximo ou path não validado.

---

## P2-2 — SUPPLY CHAIN

### O QUE?
Fixar GitHub Actions por SHA; gerar lockfiles; auditar dependências.

### POR QUÊ?
Actions sem pin e dependências sem lockfile aumentam risco de compromise upstream.

### EVIDÊNCIA
`.github/workflows/deploy.yml` e `academy-ci.yml` usam `@v4` sem SHA.
Sem `requirements.lock` ou equivalente na raiz.

### ESTRATÉGIA
1. Fixar SHA das actions usadas.
2. Gerar `requirements.txt` lockfile com `pip freeze` ou `uv lock`.
3. Adicionar step de `pip-audit` ou `safety` em CI.
4. Revisar dependências do backend Node em `backend/api/package.json`.

### TESTE
- CI roda com actions fixadas.
- `pip-audit` sem HIGH/CRITICAL.

### ROLLBACK
Reverter SHAs para tags; remover lockfile se causar conflito.

### CRITÉRIO DE SUCESSO
Actions fixadas; lockfile presente; scanning sem alertas críticos.

---

## P2-3 — PAYMENT LOGGING

### O QUE?
Redigir payloads de webhook e checkout em logs.

### POR QUÊ?
`academy/routers/payments.py` loga payload cru do webhook; pode incluir dados sensíveis.

### EVIDÊNCIA
Linha 234: `logger.info("webhook_received gateway=%s result=%s", gateway, result)` — se `result` contiver detalhes sensíveis do gateway, vaza metadados.

### IMPACTO
Exposição de tokens, IDs de pagamento, PII em logs.

### ESTRATÉGIA
1. Logar apenas: gateway, status mapeado, enrollment_id, payment_id, handled/idempotent flag.
2. Nunca logar payload completo.
3. Aplicar redaction também em logs de checkout/error handlers.

### TESTE
- webhook com payload sensível → logs não contêm campos sensíveis.
- auditoria de log não mostra tokens/keys.

### ROLLBACK
Restaurar logging anterior; risco apenas de perder detalhe de debug.

### CRITÉRIO DE SUCESSO
Logs não armazenam segredos nem PII desnecessário.

---

## P2-4 — BACKUP RESTORE

### O QUE?"
"Elaborar procedimento de restore testado para Academy DB e conteúdo editorial.

### POR QUÊ?
Backups existem, mas não há evidência de restore testado.

### EVIDÊNCIA
Pastas `backup/`, `backups/`, `docs/sales/backups/` existem. Sem documento de restore testado.

### ESTRATÉGIA
1. Definir RPO/RTO.
2. Selecionar backup representativo.
3. Restaurar em ambiente isolado.
4. Validar integridade schema/dados.
5. Documentar procedimento passo a passo.

### TESTE
- restore completo valida schema, curso mínimo e enrollment.

### ROLLBACK
Dispensar ambiente de teste; backups originais não alterados.

### CRITÉRIO DE SUCESSO
Restore testado e documentado; RPO/RTO definidos.

---

## P2-5 — SECRET SCANNING

### O QUE?
Implementar detecção de segredos em pre-commit, CI e PR.

### POR QUÊ?
Prevenir commit acidental de segredos no futuro.

### ESTRATÉGIA
1. Usar `gitleaks` ou `detect-secrets` em pre-commit hook.
2. Adicionar step em CI que falha se segredo for detectado.
3. Configurar GitHub secret scanning nativo.
4. Treinar time para não commitar `.env`.

### TESTE
- commit com fake secret → CI BLOCK.
- PR com segredo → status check vermelho.

### ROLLBACK
Remover hook/step; risco apenas de perder barreira.

### CRITÉRIO DE SUCESSO
Nenhum PR com segredo chega a main; alertas emitidos.

---

## SECURITY TESTS

Proposta de testes permanentes:

| Teste | Esperado |
|-------|----------|
| invalid webhook without secret | BLOCK |
| invalid webhook signature | BLOCK |
| replay webhook old timestamp | BLOCK |
| CORS wildcard + credentials in production | BLOCK |
| admin brute force after 5 failures | BLOCK/LOCKOUT |
| secret in PR diff | CI BLOCK |
| payment payload in logs contains token | REDACTED/NOT FOUND |
| checkout/status without auth | 401/403 |
| monitoring/status without auth | 401/403 |
| article published without gate validation | BLOCK |
| missing publication gate module | BLOCK |
| orchestrator push without human gate | BLOCK |
| cron path outside allowlist | BLOCK |
| dependency with known CRITICAL CVE | CI BLOCK |

---

## ROLLBACK PLAN

Critério geral: cada mudança deve ter reversão rápida e documentada.

- Secrets: manter segredos antigos até validação; reverter env var.
- Webhook: reverter `webhooks.py` para versão anterior.
- CORS: reverter origins configuradas.
- Admin: desativar rate-limit/MFA por flag.
- Orchestrator/cron: reverter scripts; manter backup funcional.
- Supply chain: reverter actions para tags; remover lockfile.
- Logging: reverter formatação anterior.
- Backup: não alterar produção; restore em ambiente isolado.
- Secret scanning: remover hook/step.

Nenhuma alteração deve ser aplicada sem:
1. branch separada;
2. PR com descrição de risco;
3. teste automatizado antes/depois;
4. rollback documentado.

---

## IMPLEMENTATION ORDER

1. P1-1 Secrets — maior risco de exposição.
2. P1-2 Webhooks — evita fraude direta.
3. P1-3 CORS — reduz superfície cross-origin.
4. P1-4 Admin — protege painel administrativo.
5. P2-3 Payment Logging — reduz exposição em logs.
6. P2-1 Orchestrator/Cron — limita privilégios.
7. P2-2 Supply Chain — hardening de pipeline.
8. P2-4 Backup Restore — resiliência.
9. P2-5 Secret Scanning — prevenção contínua.

Justificativa: ordem segue impacto direto à confidencialidade/integridade/disponibilidade. Logging e least privilege vêm após controles de acesso porque reduzem janela de exposição enquanto o hardening principal é preparado.

---

## ACCEPTANCE CRITERIA

Fase 1 concluída quando:

- [ ] `.env` removido do versionamento/histórico ou segredos rotacionados.
- [ ] webhook bloqueia sem secret válido.
- [ ] CORS não retorna `*` com credenciais em produção.
- [ ] admin tem rate-limit e lockout.
- [ ] payloads sensíveis não aparecem em logs.
- [ ] orchestrator/cron sem shell/paths não validados.
- [ ] actions fixadas e lockfile presente.
- [ ] restore testado documentado.
- [ ] secret scanning ativo em CI.

Cada item deve possuir teste automatizado antes/depois e rollback verificado.

---

FIM — HARDENING FASE 1
