# Revisão editorial — 08/10/2026

Alterações confirmadas pelo usuário: adicionar nomes propostos/status à planilha; bloquear reescrita por família; incorporar seis correções na base sem republicar páginas nem mudar checkouts.

## Base corrigida e histórico
Os arquivos kb_part1..5.py permanecem como registros da base original. editorial_corrections_20261008.json preserva antes/depois das seis correções e suas fontes. editorial_corrections.apply_corrections(FAMS) aplica os novos textos na base em memória e recusa aplicação se o original tiver mudado. Não é uma correção dos módulos já publicados: sua atualização fica pendente da revisão dos currículos específicos.

## Bloqueio preventivo
rewrite_courses.py exige tools/kb/course_content_by_slug.json. O manifesto ainda não existe. Sem ele, ou com cursos faltantes/estruturas incompletas/conjuntos exatamente duplicados, o script aborta antes de gravar módulos, páginas ou catálogo. Não foi executada reescrita na produção.

## Validação local
Todos os arquivos Python compilaram. Execução em diretório isolado confirmou o bloqueio por manifesto ausente antes de qualquer escrita em education. Teste local, não certificação de CI nem revisão jurídica integral.

## Publicação
Commit usa [skip ci] para evitar gatilhos push de reescrita/deploy. Nenhum HTML, checkout, preço ou URL foi alterado. Não acionar workflow_dispatch. Fluxos agendados ou commits futuros são independentes deste marcador e devem ser monitorados.

## Próxima etapa
Produzir e revisar conteúdo próprio para cada curso, bibliografia atualizada, exercícios e avaliações; reconciliar fichas comerciais, quantidades de aulas e entregas; só então autorizar geração/publicação e liberação comercial.
