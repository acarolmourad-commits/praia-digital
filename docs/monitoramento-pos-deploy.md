# Monitoramento Pós-Deploy — Praia Digital Academy
**Objetivo:** acompanhar saúde, desempenho e conversão após o deploy no Render.

---

## 1. Saúde da aplicação
- [ ] `/health` retornando `{"status":"ok"}` a cada 5 min
- [ ] Logs do Render sem erros 500 em `/auth/*`, `/academy/*`, `/payments/*`
- [ ] Banco PostgreSQL conectado e sem tabelas faltando
- [ ] Espaço em disco do Render acima de 20%

## 2. Frontend
- [ ] `/education/index.html` carregando em < 2s
- [ ] `/education/vendas.html` carregando em < 2s
- [ ] `/education/cursos/index.html` carregando em < 2s
- [ ] `/education/aluno/login.html` carregando em < 2s
- [ ] Páginas de curso com SEO OK (title, description, OG)

## 3. API
- [ ] `POST /auth/register` retornando 200
- [ ] `POST /auth/login` retornando 200 com JWT
- [ ] `GET /courses` retornando lista de cursos
- [ ] `POST /academy/cart/add` retornando 200
- [ ] `POST /academy/cart/checkout` retornando 200
- [ ] `POST /academy/payments` retornando 200
- [ ] `POST /academy/payments/{id}/webhook` retornando 200
- [ ] `GET /admin/users` retornando 200 com admin logado

## 4. Conversão
- [ ] Checkout completo funcionando
- [ ] Webhook de pagamento confirmando acesso
- [ ] Matrícula criada automaticamente após pagamento
- [ ] Progresso de aulas funcionando
- [ ] Certificado PDF gerando corretamente

## 5. Segurança
- [ ] CORS bloqueando origens não permitidas
- [ ] SECRET_KEY forte e não exposta
- [ ] Senhas hasheadas com bcrypt
- [ ] JWT com expiração de 7 dias
- [ ] Admin endpoints protegidos por role

## 6. Performance
- [ ] Tempo de resposta < 500ms para endpoints principais
- [ ] Banco sem queries lentas (> 1s)
- [ ] Frontend sem erros no console
- [ ] Imagens e assets carregando corretamente

## 7. Monitoramento contínuo
- [ ] UptimeRobot / Better Uptime monitorando `/health`
- [ ] Logs do Render exportados para análise
- [ ] Alertas configurados para erros 500
- [ ] Backup automático do banco PostgreSQL

## 8. SEO
- [ ] Google Search Console indexando páginas
- [ ] Sitemap.xml atualizado
- [ ] Core Web Vitals dentro do verde
- [ ] OG tags funcionando no WhatsApp/Telegram

## Comandos úteis
```bash
# Health check
curl https://academy.praia.digital/health

# Teste de API
curl -X POST https://academy.praia.digital/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","password":"123456"}'

# Ver logs no Render
# Dashboard → praia-digital-academy → Logs
```

## Contatos de suporte
- Render: https://render.com/support
- Domínio: registro.br ou provedor DNS
- GitHub: https://github.com/acarolmourad-commits/praia-digital
