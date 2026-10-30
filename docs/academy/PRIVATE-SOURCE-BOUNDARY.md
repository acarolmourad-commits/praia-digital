# Separação dos materiais completos — proposta restrita à Academy

## O que este patch faz

Remove da versão atual (HEAD), por commit recuperável, exatamente 62 apostilas HTML em `docs/academy/delivery/` e 11 arquivos `course-learning-plans*.json` / `course-application-*.json`. As fontes completas permanecem em backup privado externo com hashes verificados; os 62 PDFs privados de entrega são mantidos no Workspace. Nenhuma alteração de visibilidade, domínio, histórico ou fork está incluída.

O site e repositório continuam públicos. Catálogo, preços, primeiras lições e páginas comerciais permanecem byte a byte iguais. Os 268 módulos antigos de alunos e demais materiais anteriores não são removidos. Nenhuma área fora da Academy é desativada e nenhum link de serviço humano é alterado.

O gerador exige `--private-plans` e `--private-output` fora deste checkout e recusa caminhos internos, inclusive resolvidos por links simbólicos. O build público e a CI rejeitam a presença de fontes completas nos caminhos conhecidos. `.gitignore` reduz reintroduções acidentais. Esses controles não são DRM, não escondem histórico e não impedem que alguém renomeie/copiei conteúdo para outro caminho; revisão de publicação continua necessária. CI ocorre depois do push e não revoga bytes já enviados ao GitHub.

## Testes separados

- CI pública: catálogo/prévias, preços, aliases, trilhas, navegação e ausência de materiais completos no checkout.
- Auditoria privada explícita: `ACADEMY_PRIVATE_PLANS=/caminho/externo/course-learning-plans.json ACADEMY_PRIVATE_OUTPUT=/caminho/externo/delivery python -m unittest discover -s tests -p 'test_academy_digital.py'`.
- Sem essas entradas, a auditoria curricular completa é marcada como não executada na CI pública; não é simulada por flags de prontidão.

## O que NÃO resolve

O histórico público conserva os arquivos removidos e o fork público pode expor os objetos por SHA. Materiais legados preservados continuam públicos. Portanto este patch não permite afirmar que todo conteúdo da Academy só está disponível a compradores e não autoriza ativar novas cobranças de cursos como se o acesso exclusivo estivesse validado.

## Próxima decisão necessária

Mantendo este repositório público, há duas escolhas honestas:
1. Autorizar separadamente a avaliação/limpeza do histórico específico da Academy e tratar o fork com seu proprietário. Isso pode exigir reescrita de histórico e não recolhe cópias já baixadas. Não executar sem aprovação específica.
2. Aceitar a edição já exposta como histórica e criar uma edição realmente nova, somente privada, cujo material não tenha sido publicado. A entrega oficial pode usar Stripe confirmado + Drive nominal + Gmail assistido, com prazo informado antes da compra; não prometer liberação automática.

O estado financeiro do Stripe não altera permissões de conteúdo. Uma URL de sucesso, mensagem encaminhada ou compra pendente não é comprovação de pagamento. Os cursos só devem ser anunciados como exclusivos quando armazenamento, concessão ao comprador e todas as exposições conhecidas da edição vendida forem verificados.
