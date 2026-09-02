# Automação WhatsApp + Composio — Fluxo de Atendimento

## Objetivo
Padronizar o fluxo de captação, classificação e resposta automática para leads do Praia Digital via WhatsApp/Composio.

## Origem dos leads
- Wizard de cadastro de imóveis: `/corretores/cadastrar-imovel.html`
- Modal de captura: `partials/lead-modal.html` + `js/lead-modal.js`
- Landing pages: `/afiliados/enxoval-automacao-riviera.html`, `/blog/top-10-acessorios-indispensaveis-praia-riviera-2026.html`, etc.

## Payload esperado
- Nome
- Telefone/WhatsApp
- Origem do lead (`origem` no Wizard; `Modal de Captura` no lead modal)
- Interesse: cadastro de imóvel, análise de mercado, automação/enxoval, acessórios praia, churrasco/gourmet, investimento imobiliário

## Regras de roteamento
- Origem `Cadastrando Imóvel` → atendimento de corretores/parcerias
- Origem `Simulador de Rentabilidade` → atendimento de investidores
- Origem `Guia de Enxoval e Automação` → atendimento de afiliados/vendas
- Origem `Guia Top 10 Acessórios Praia` → atendimento de afiliados/vendas
- Origem `Guia de Churrasco e Área Gourmet` → atendimento de afiliados/vendas
- Origem `Modal de Captura` → atendimento de análise de mercado/imóveis

## Modelos de resposta rápida
1. **Investidor/Rentabilidade**
   - "Olá, [NOME]! Recebemos seu interesse pelo Simulador de Rentabilidade. Queremos enviar a Análise de Mercado PDF e agendar uma consultoria rápida. Qual o melhor horário?"
2. **Cadastro de imóvel**
   - "Olá, [NOME]! Recebemos seu cadastro de imóvel ([ORIGEM]). Um corretor parceiro vai validar CRECI e publicar no marketplace. Pode enviar fotos/vídeo pelo WhatsApp?"
3. **Automação/Enxoval/Acessórios/Gourmet**
   - "Olá, [NOME]! Você pediu informações sobre [CATEGORIA]. Posso enviar o link do guia completo e as ofertas Amazon selecionadas para a Riviera. Qual item você quer primeiro?"
4. **Geral**
   - "Olá, [NOME]! Recebemos seu contato pelo Praia Digital. Como posso ajudar: aluguel temporada, compra/permuta ou indicação de serviços na Riviera?"

## Configuração do Composio
- Variável: `COMPOSIO_WEBHOOK_URL`
- Variável: `COMPOSIO_API_KEY`
- Ação sugerida: enviar payload JSON para o webhook do Composio e deixar a reply automatizada seguir o modelo conforme `origem`.
