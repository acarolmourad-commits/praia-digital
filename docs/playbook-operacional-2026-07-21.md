# Playbook operacional — Praia Digital
Objetivo: executar todos os dias os temas pedidos com foco, métricas e sem duplicar conteúdo publicado.

## 1. Cadastro de imóveis
- Base: `docs/data/cadastro-imoveis.csv` e `propriedades/cadastro-imoveis.csv`.
- Target: 500+ (hoje verificar quantidade real; revisar semanalmente).
- Fluxo:
  1. Receber dados: tipo, área, quartos, estado, CEP, cidade, bairro, preço.
  2. Validar duplicatas por endereço/CEP.
  3. Gerar descrição automática + avaliação de preço.
  4. Publicar em `blog/imoveis/` e tool de busca.

## 2. Parceiros B2B
- Base: `docs/sales/csv-lotes-b2b/`.
- Meta 90 dias: 20 white-label.
- Sequência: apresentação → proposta → onboarding → publicação no site do parceiro.

## 3. Conteúdo diário
- Vídeo: 1 por dia, com roteiro em `blog/roteiro-video-diario-...`.
- Artigo SEO: 3 por semana, inédito, cluster por cidade.
- Newsletter semanal: publicar até 6ª feira, link interna para artigos da semana.
- Redes sociais: 1 post curto por dia com CTA.

## 4. Métricas diárias
- Imóveis cadastrados
- Parceiros em contato
- Visualizações de vídeo e cliques
- Assinaturas iniciadas

## 5. Checklist rápido
1. Publicar vídeo
2. Publicar 1 artigo ou atualizar ferramenta
3. Atualizar cadastro com mais imóveis
4. Enviar follow-up B2B
5. Medir métricas e ajustar
