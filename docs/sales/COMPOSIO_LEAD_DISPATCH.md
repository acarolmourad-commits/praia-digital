# Composio Lead Dispatch — Praia Digital

## Objetivo
Automatizar a notificação de novos leads em tempo real quando os formulários de Afiliados ou Corretores forem acionados.

## Fontes
- `/afiliados/index.html` — indicação de imóvel por afiliado.
- `/corretores/cadastrar-imovel.html` — cadastro de imóvel por corretor.

## Destino
- Canal interno de atendimento via integração Composio (Discord/Telegram/Workspace).
- Fallback: `mailto:comercial@praia.digital` com subject estruturado.

## Arquitetura
1. Frontend captura submissão dos formulários.
2. Backend/automation recebe payload estruturado.
3. Composio envia alerta formatado para o canal de atendimento.

## Payload esperado
```json
{
  "source": "afiliados|corretores",
  "lead": {
    "nome": "...",
    "email": "...",
    "telefone": "...",
    "whatsapp": "...",
    "pix": "...",
    "imobiliaria": "...",
    "creci": "...",
    "endereco": "...",
    "cidade": "...",
    "bairro": "...",
    "tipo_imovel": "...",
    "negocio": "...",
    "valor": "...",
    "condominio": "...",
    "iptu": "...",
    "caracteristicas": [],
    "video": "...",
    "descricao": "...",
    "observacoes": "...",
    "termos_aceitos": true
  },
  "metadata": {
    "received_at": "2026-09-01T21:00:00Z",
    "page": "/afiliados/index.html",
    "user_agent": "...",
    "ip": "..."
  }
}
```

## Scripts de exemplo
- `scripts/composio_lead_dispatch.py`: consumir endpoint do Composio e enviar payload.
- `.env.composio`: armazenar chaves/URLs da integração.

## Observações
- Esta documentação define o fluxo alvo. A ativação real depende de credenciais e apps habilitados no Composio.
- Não expor chaves secretas no frontend.
- Validar TLS/HTTPS em todos os endpoints.
