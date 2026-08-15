# Homologação comercial — Academy pós-deploy

## Objetivo
Validar que a jornada de compra está funcional antes de liberar vendas reais.

## Pré-condições
- Deploy concluído e `/health` retornando 200
- Variáveis de produção preenchidas
- Banco de produção populado com os 64 cursos

## 1. Checkout
- Abrir página de checkout com slug real: `education/checkout.html?slug=<slug>&title=<nome>&price=<valor>`
- Confirmar exibição correta do nome, preço e slug do curso
- Confirmar botão de compra visível
- Confirmar ausência de erros no console do browser

## 2. Pagamento
- Usar gateway em sandbox quando disponível
- Simular pagamento aprovado → matrícula ativa
- Simular pagamento pendente → sem acesso
- Simular pagamento recusado → sem acesso
- Confirmar redirecionamento pós-pagamento

## 3. Webhook
- Disparar evento de teste do gateway para `/academy/payments/webhook`
- Confirmar recebimento 200
- Confirmar criação/atualização de matrícula
- Simular webhook duplicado → idempotente

## 4. E-mail transacional
- Confirmar e-mail de confirmação de matrícula enviado
- Confirmar e-mail de liberação de acesso enviado
- Confirmar ausência de spam/rejeição
- Validar conteúdo do e-mail: nome do curso, link de acesso, suporte

## 5. Acesso ao curso
- Confirmar acesso à página do curso após pagamento aprovado
- Confirmar estrutura de módulos/aulas carregada
- Testar logout/login novamente → acesso mantido
- Testar link direto sem login → sem acesso

## 6. Tracking
- Confirmar evento de checkout iniciado
- Confirmar evento de pagamento aprovado
- Confirmar evento de matrícula ativa
- Validar se há Analytics/GTM/Tracking Pixel disparando

## 7. Roteiros de erro
- Confirmar página de erro amigável para falha de pagamento
- Confirmar mensagem de sucesso após pagamento aprovado
- Testar link expirado/inválido
- Testar slug inexistente

## 8. Regressão
- Confirmar que `/courses` lista 64 cursos
- Confirmar que slugs reais abrem páginas corretas
- Confirmar que não houve quebra de navegação
- Confirmar que não houve vazamento de dados sensíveis

## 9. Performance
- Confirmar tempo de carregamento aceitável (<3s)
- Confirmar SSL válido
- Confirmar sem mixed content (HTTP em página HTTPS)

## Critérios de aprovação
- Todos os testes de checkout/pagamento/webhook/e-mail passam
- Nenhum erro 5xx em endpoints públicos
- Nenhum dado sensível exposto em responses
- Tracking funcionando
