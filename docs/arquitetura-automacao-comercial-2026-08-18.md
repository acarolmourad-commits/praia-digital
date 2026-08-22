# Automação comercial — Arquitetura de fluxo

## Jornada 1 — Cliente imobiliário
VISITA
→ SERVIÇO
→ LEAD
→ PROPOSTA
→ CHECKOUT
→ PAGAMENTO
→ ENTREGA

Automação:
- Captura de lead por formulário/WhatsApp
- Classificação automática por interesse
- Proposta gerada automaticamente
- Checkout integrado
- Cobrança automática
- Validação automática
- Entrega automática após PAGAMENTO_CONFIRMADO

Intervenção humana:
- Somente em exceções: negociação personalizada, serviço de IA, complexidade documental

## Jornada 2 — Cliente Academy
VISITA
→ CURSO
→ CHECKOUT
→ PAGAMENTO_CONFIRMADO
→ LIBERAÇÃO_AUTOMÁTICA

Automação:
- Navegação para curso
- Checkout
- Cobrança
- Validação
- Liberação automática

Intervenção humana:
- Nenhuma, uma vez integrado

## Jornada 3 — IA para imobiliárias
VISITA
→ DIAGNÓSTICO
→ BRIEFING
→ PROPOSTA
→ WHATSAPP HUMANO
→ NEGOCIAÇÃO
→ CONTRATAÇÃO
→ ONBOARDING

Automação:
- Captura de lead
- Classificação automática de intenção
- Briefing inicial automatizado
- Proposta preparada automaticamente
- Registro no CRM

Intervenção humana:
- Diagnóstico personalizado
- Negociação
- Personalização do escopo
- Implantação
- Relacionamento contínuo

## Separação das jornadas
- Jornada 1 e 2: checkout automático
- Jornada 3: WhatsApp humano como etapa core
- Não misturar fluxos

## Pontos de integração
- Site → Checkout → Gateway → Agente Financeiro → Academy
- Lead → Classificação → Oferta → Proposta → Checkout/Pagamento → Entrega
- IA → Captura → Classificação → Briefing → Proposta → WhatsApp Humano → Negociação → Contratação → Onboarding
