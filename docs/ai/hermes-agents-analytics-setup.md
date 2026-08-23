# Hermes Agents — Analytics Setup (GA4)

Guia operacional para habilitar tracking de landing pages Hermes Agents no Google Analytics 4.

## 1. Pré-requisitos

- Conta Google Analytics 4 com propriedade criada para `praia.digital`
- Permissão de edição na propriedade GA4
- Acesso ao repositório do site

## 2. Obter o Measurement ID

1. Abra [GA4 Admin](https://admin.google.com/analytics/)
2. Selecione a propriedade do site
3. Vá em **Admin → Data Streams → Web**
4. Copie o **Measurement ID** no formato `G-XXXXXXXXXX`

## 3. Inserir o Measurement ID no site

### 3.1 Variável central (recomendado)

Se o site usar um build step ou variáveis de ambiente, adicione:

```
VITE_GA4_MEASUREMENT_ID=G-XXXXXXXXXX
```

### 3.2 Substituição direta em landing pages

Substitua `G-XXXXXXXXXX` pelo ID real em **todas** as landing pages Hermes Agents que contêm o snippet de tracking.

Arquivos afetados:

- `servicos/hermes-agents*.html`
- `solucoes/hermes-agents*.html`
- `outreach/cta-whatsapp-hermes-agents.html`
- `assets/score-hermes.html`

## 4. Eventos implementados

### 4.1 Page view (automático)

Disparado pelo `gtag('config', ...)` na abertura da página.

### 4.2 CTA click

Evento `cta_click` disparado em cliques em elementos com classes:
- `.btn`
- `.btn-primary`
- `.btn-purple`
- `.cta`

Parâmetros:
- `page_path` — caminho da página
- `href` — URL do CTA (até 200 chars)
- `text` — texto do botão (até 100 chars)

### 4.3 WhatsApp click

Evento `whatsapp_click` disparado em cliques em links do WhatsApp (`wa.me`) ou botões com texto contendo "whatsapp".

Mesmos parâmetros de `cta_click`.

### 4.4 Call click

Evento `call_click` disparado em cliques em links `tel:` ou botões com texto "ligar".

### 4.5 Scroll depth

Evento `scroll_depth` disparado nos marcos:
- 25 %
- 50 %
- 75 %
- 100 %

Parâmetros:
- `percent` — valor do marco (25, 50, 75, 100)
- `page_path` — caminho da página

## 5. Conversões no GA4

Marque como conversão os eventos abaixo (Admin → Events → Mark as conversion):

| Evento | Quando converter |
|--------|------------------|
| `whatsapp_click` | Lead quente — clique no CTA do WhatsApp |
| `cta_click` | Interação com CTA genérico |
| `scroll_depth` (100) | Leitura completa da página |
| `scroll_depth` (50) | Engajamento médio |

Dica: crie uma **audience** de usuários que completaram `scroll_depth` ≥ 50 para remarketing.

## 6. UTM parameters

Sempre usar UTMs em campanhas que apontam para landing pages:

| Parâmetro | Valor exemplo |
|-----------|---------------|
| `utm_source` | google, instagram, linkedin, email |
| `utm_medium` | cpc, social, email, referral |
| `utm_campaign` | hermes-agents-lancamento-2026 |
| `utm_content` | cta-hero, cta-final, banner |

Exemplo de URL com UTM:

```
https://praia.digital/servicos/hermes-agents.html?utm_source=google&utm_medium=cpc&utm_campaign=hermes-agents-lancamento-2026&utm_content=cta-hero
```

## 7. Debug e validação

1. Abra a landing page com `?debug=true`
2. Use o **GA4 DebugView** para confirmar eventos em tempo real
3. Valide com o **Google Tag Assistant** (extensão Chrome)
4. Teste cliques nos CTAs e scroll até o fim da página

## 8. Manutenção

- Sempre adicionar o snippet de eventos quando criar nova landing page Hermes Agents
- Revisar trimestralmente se os nomes de eventos estão consistentes
- Atualizar o Measurement ID se a propriedade GA4 mudar
