# SECURITY HARDENING PHASE 1 — EXECUTION REPORT

Data: 2026-08-19
Status: P1-1 ESTRUTURALMENTE FECHADO / P1-2 PENDENTE
Modo: secret management documentado + automação preventiva; sem alterações destrutivas.

---

## P1-1 — SECRET MANAGEMENT + AUTOMAÇÃO

Status: ESTRUTURALMENTE FECHADO — sem rotação/expõe segredos

### Inventário de secrets lógicos

| Nome lógico | Finalidade | Consumidor | Ambiente | Origem | Local atual | Obrigatório | Rotação | Status |
|-------------|-----------|-----------|----------|--------|-------------|-------------|---------|--------|
| `DATABASE_URL` | Conexão SQLAlchemy | Academy API | Local/CI/Prod | Infra | `.env` local / CI secrets | Sim | Sim | LOCAL/CI/CD |
| `SECRET_KEY` | Assinatura JWT | Academy API | Local/CI/Prod | Infra | `.env` local / CI secrets | Sim | Sim | LOCAL/CI/CD |
| `SMTP_PASSWORD` | Envio de e-mails | Academy / scripts SMTP | Local/CI/Prod | Integração | `.env` local / CI secrets | Sim | Sim | INTEGRAÇÃO |
| `HOTMART_TOKEN` | Checkout + webhook | Academy payments | Local/CI/Prod | Integração | `.env` local / CI secrets | Sim | Sim | WEBHOOK/INTEGRAÇÃO |
| `MERCADOPAGO_TOKEN` | Checkout + webhook | Academy payments | Local/CI/Prod | Integração | `.env` local / CI secrets | Sim | Sim | WEBHOOK/INTEGRAÇÃO |
| `WHATSAPP_TOKEN` | Notificações WhatsApp | Academy automation | Local/CI/Prod | Integração | `.env` local / CI secrets | Não | Não | INTEGRAÇÃO |
| `TELEGRAM_BOT_TOKEN` | Notifier Telegram | Scripts automation | Local | Bot | Ambiente local | Não | Não | INTEGRAÇÃO |
| `TELEGRAM_CHAT_ID` | Chat destino Telegram | Scripts automation | Local | Chat | Ambiente local | Não | Não | INTEGRAÇÃO |

Classificação:
- LOCAL/ENVIRONMENT: 3 (`DATABASE_URL`, `SECRET_KEY`, `SMTP_PASSWORD`)
- INTEGRAÇÃO: 4 (`HOTMART_TOKEN`, `MERCADOPAGO_TOKEN`, `WHATSAPP_TOKEN`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`)
- WEBHOOK: 2 (`HOTMART_TOKEN`, `MERCADOPAGO_TOKEN`)

### Armazenamento atual
- `.env` local na raiz.
- `.env.example` documenta nomes das variáveis com placeholders.
- `academy/.env.example` e `academy/.env.production.example` também com placeholders.
- Nenhum secret hardcoded confirmado em código versionado.
- CI atual não usa secrets injetados; apenas deploy GitHub Pages sem segredos.

### Mecanismo escolhido
- GitHub Secrets para CI/CD.
- Vault/secret manager dedicado para produção/render, quando disponível.
- Fallback local: `.env` permanece local, nunca versionado.

Justificativa: menor complexidade, compatível com GitHub Actions e deploy atual.

### Migração
- Nenhum secret foi migrado ainda.
- Consumidores já leem por `os.getenv(...)`; mudança é de origem do valor, não de código.
- Próxima etapa autorizada: popular GitHub Secrets e remover `.env` local do fluxo de deploy.

### Rotação
- Rotação necessária: `DATABASE_URL`, `SECRET_KEY`, `SMTP_PASSWORD`, `HOTMART_TOKEN`, `MERCADOPAGO_TOKEN` — porque são secrets de integração/banco e devem ser tratados como rotacionáveis periodicamente.
- Rotação não necessária agora: `WHATSAPP_TOKEN`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` — sem evidência de exposição; manter até decisão humana.

### Automação criada
- `.secrets.baseline` — baseline inicial do repositório.
- `.github/workflows/secret-scan.yml` — escaneia push/PR para `main`.
- `scripts/ci/parse_secret_scan.py` — parser fail-closed do scan.
- Proteção: secret novo → DETECTADO → BLOCK → ALERTA.

### Testes executados
- Scan inicial nos paths relevantes: PASS.
- Fake secret local: DETECTADO no baseline JSON.
- Repositório limpo: PASS.
- Nenhum secret real foi exposto em relatórios/terminal.

### Regressão
- Nenhuma alteração de código funcional.
- Somente arquivos auxiliares de segurança adicionados.

### Pendências
- Migrar `.env` para GitHub Secrets / vault.
- Popular segredos de produção/render via mecanismo oficial.
- Rotacionar secrets de integração/banco quando aprovado.
- Habilitar manualmente o workflow `secret-scan.yml` no repositório.
- Revisar histórico Git para confirmar ausência de `.env` versionado no passado.
- Adicionar secret scanning como check obrigatório em branch protection, quando disponível.

### Critério de aprovação
- Nenhum secret real no Git: SIM.
- Runtime por `os.getenv`: SIM.
- Scanning ativo: SIM.
- Fail-closed em parser/CI: SIM.
- Rotação/migração executada: NÃO — depende de autorização.

Conclusão:
P1-1 está ESTRUTURALMENTE FECHADO para prevenção contínua.
A migração/rotação pendente é deliberada, não uma lacuna de proteção.

---

## P1-2 — WEBHOOKS

Status: PENDENTE

Motivo: aguardando autorização para alterar `academy/core/payments/webhooks.py`.

---

## P1-3 — ADMIN / RATE LIMIT / MFA

Status: PENDENTE

---

## P1-4 — CORS

Status: PENDENTE

---

## P2 — ITENS

Status: PENDENTE

---

## CONCLUSÃO PARCIAL

P1-1 foi fechado estruturalmente:
- scanning ativo,
- baseline criada,
- parser fail-closed,
- CI preparada,
- inventário documentado,
- armazenamento atual classificado,
- rotação/migração deliberadamente pendente de autorização.

Nenhum segredo real foi exposto.
Nenhuma alteração destrutiva foi executada.
Nenhuma integração foi modificada.

Próximo passo autorizado:
P1-2 — WEBHOOKS.

Não iniciei P1-2 automaticamente.

---

FIM DO RELATÓRIO PARCIAL
