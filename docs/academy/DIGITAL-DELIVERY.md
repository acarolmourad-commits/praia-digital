> **Proposta de separação privada — outubro de 2026:** as fontes completas e apostilas devem ficar fora deste repositório público. O catálogo e as amostras permanecem públicos. A remoção do HEAD não elimina histórico, forks ou cópias; isso ainda não comprova acesso exclusivo após pagamento. A execução do gerador exige entrada e saída privadas externas. A documentação histórica abaixo não autoriza republicar arquivos completos.

# Academy: catálogo digital e entrega assistida

Edição: 30 de outubro de 2026. O catálogo público substitui promessas incompatíveis com o acervo anterior (quatro módulos curtos, amplamente repetidos entre temas).

## Fonte única e escopo

- `course-learning-plans.json` no armazenamento privado externo: planos revistos, lições específicas, exemplos resolvidos, procedimentos demonstrados, modelos preenchidos, casos de falha, atividades e critérios de autoavaliação. Cada curso é **curto, escrito e autoinstrucional**, não um curso extensivo em vídeo.
- `course-prices.json`: preços em reais, pagamento único; justificativa na análise de mercado.
- `education/assets/catalog.json`: catálogo público gerado. Checkout resolve exclusivamente esses dados, nunca o preço/título informado na URL.
- URLs antigas de versões duplicadas permanecem como páginas de encaminhamento e não são vendidas como materiais adicionais.
- Trilhas identificam os materiais incluídos; não acrescentam tutoria, certificação ou habilitação profissional.

## Regenerar e verificar

```sh
python scripts/build_academy_digital.py --private-plans /CAMINHO_PRIVADO/course-learning-plans.json --private-output /CAMINHO_PRIVADO/delivery
python scripts/validate_academy_inventory.py
python -m unittest discover -s tests -p 'test_academy_digital.py'
node tests/test_academy_enrollment.cjs
```

O gerador cria páginas comerciais e amostras com a primeira lição neste repositório, mas grava apostilas HTML somente no diretório privado externo indicado por `--private-output`. Entrada e saída privadas dentro deste repositório são recusadas; o build público falha caso fontes completas reapareçam. Não publicar links públicos para apostilas completas como se fossem protegidos por login. O histórico e os materiais antigos preservados continuam públicos; este controle não é DRM nem um mecanismo de autorização ao comprador.

## Procedimento comercial de entrega — manual, não automatizado

1. Receber o contato com o curso/trilha, preço anunciado e página correspondente.
2. Antes de cobrar, conferir se o interessado já possui materiais da trilha; explicar formato textual, exclusões, valor final, meio de pagamento, prazo e canal da entrega digital. Não vender acesso a vídeo, certificado ou suporte que não integram este escopo.
3. Preparar o HTML correspondente no diretório privado externo de entrega (ou os vários HTMLs da trilha), nunca em `docs/academy/delivery/` deste repositório. Ele funciona sem envio de respostas: o estudante registra sua atividade em arquivo próprio. Pode ser salvo/imprimido em PDF pelo navegador; revisar o PDF antes de enviar se optar por esse formato.
4. Somente após a confirmação comercial e de pagamento pelo processo real da equipe, enviar os arquivos pelo canal combinado. Não usar parâmetro `status=success` ou clique do usuário como prova de pagamento.
5. Confirmar recebimento e orientar sobre abertura do arquivo. Não prometer liberação instantânea no LMS: a integração pública não foi validada ponta a ponta.

Nenhum pagamento, cadastro, envio de mensagem, matrícula, credencial, configuração de segurança ou preço Stripe foi criado/modificado nesta implementação. O formulário de login mantém o endpoint existente e informa falhas visivelmente; não foi redirecionado a uma API presumida.

## QA

A CI executa validações do catálogo/material, testes do handler de login com respostas simuladas e navegação offline em 390px/1280px. Todas as requisições dos testes de browser são interceptadas: não há compra ou login real. A entrega comercial e o LMS requerem verificação operacional própria; não são comprovados pela existência do catálogo.

## Conteúdo antigo e publicação

`prepare_academy_publication.py --check` audita links HTML antes de excluir do artefato público apenas os diretórios antigos `education/cursos/*/marketing`, `email-sequence`, `instagram` e `seo-articles`, além dos novos planos-fonte (`course-learning-plans*.json`), suplementos (`course-application-*.json`) e apostilas de entrega assistida. O código recusa exclusão se existir uma referência HTML ativa. Esses arquivos continuam no repositório para recuperação.

**Preservados:** todo `academy/cursos/**`, os módulos `education/cursos/*/curso-completo/modulo-*.md` usados pelo fallback da área do aluno, materiais e planilhas. Metadados antigos `ficha-completa`, `MANIFESTO` e `sumario` receberam aviso de edição anterior; não representam a oferta nova. Direitos e conteúdo de contratações anteriores não foram substituídos. As novas ofertas usam somente as apostilas e exercícios revisados desta edição.
