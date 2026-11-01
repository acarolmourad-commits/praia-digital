# Guia de Bairros — revisão de 1 de novembro de 2026

Base: `7ec198908be1eaf665bb6996e775e163b7013548` (main). Entrega para revisão em PR rascunho; sem merge ou publicação.

## Conteúdo e navegação

- `bairros/index.html` é o catálogo público: 123 guias em 12 cidades, com HTML navegável sem JavaScript. As duas matérias relacionadas não contam como bairros adicionais. O DOM é a fonte da busca e das contagens filtradas, sem catálogo paralelo.
- Busca combina cidade, bairro e temas das matérias, normaliza acentos e oferece estado vazio, limpeza e controles de expansão. Links de cidade e fragmentos continuam utilizáveis ao voltar de uma matéria.
- As URLs dos guias e dos dois artigos foram preservadas. Riviera recebe ligação recíproca com seu guia de bairro; Praia Grande é contexto municipal da simulação, não um bairro novo.
- O blog deixa de chamar a matéria de rental yield de estudo. As duas matérias têm sumário, breadcrumbs, fontes, leitura responsiva e publicidade secundária sem os blocos duplicados.
- Não foram importadas vitrines antigas, aliases, redirecionamentos ou rascunhos como guias completos. A fonte integral dos textos adicionais mencionados pelo usuário continua não identificada.

## Evidências editoriais

- [Projeto oficial da Riviera](https://www.rivieradesaolourenco.com/sobre-a-riviera/o-projeto/): descreve bairro aberto integrado a Bertioga. Não equivale a acesso controlado de um condomínio.
- [Associação dos Amigos](https://www.rivieradesaolourenco.com/associacao-dos-amigos/): declara serviços urbanos e auxílio à segurança pública. O texto atribui essas informações à entidade; não garante segurança ou valorização.
- [FipeZAP/Fipe](https://www.fipe.org.br/pt-br/indices/fipezap/): preços baseados em anúncios não demonstram ocupação de temporada nem a taxa líquida anunciada anteriormente.
- Simulação: R$ 350 × 200 noites = R$ 70.000; 200/365 = 54,8% arredondados; R$ 70.000/R$ 500.000 = 14% bruto. Custos supostos de 22% = R$ 15.400; saldo preliminar = R$ 54.600, ou 10,92% antes das demais despesas. A taxa de 5,8% exigiria outras deduções de R$ 25.600 não demonstradas. O denominador exclui aquisição, mobília e outros investimentos iniciais.

## Verificação reproduzível

```sh
python -X utf8 -m unittest discover -s tests -p 'test_neighborhood_guide.py' -v
python -X utf8 -m unittest discover -s tests -p 'test_navigation.py' -v
python -X utf8 -m unittest discover -s tests -p 'test_homepage_content.py' -v
node --check js/neighborhood-guide.js
python scripts/preview-neighborhood-guide.py /tmp/guide-preview
GUIDE_BUILT_ROOT=/tmp/guide-preview GUIDE_QA_OUTPUT=/tmp/guide-qa node tests/neighborhood-guide-browser.cjs
```

Instale Playwright 1.63.0 com Chromium para o teste de navegador. No Windows local foi usado Chrome instalado (`GUIDE_BROWSER_CHANNEL=chrome`), pois o Chromium empacotado não estava instalado. O teste intercepta requisições, serve arquivos locais e bloqueia tráfego externo e envios de formulário. As imagens e `results.json` são gerados em `GUIDE_QA_OUTPUT`; o workflow específico anexa essas evidências ao CI.

Testes locais: 5 testes do guia, 6 de navegação e 5 da home passaram. Navegador: 375, 390 e 1280 px, busca com/sem acentos, filtros combinados, estado vazio, limpeza/foco, teclado em `summary`, expandir/recolher, retorno de artigos, 123 guias sem JavaScript, ausência de overflow e de erros de execução. O build de navegação foi aplicado às três páginas em diretório isolado. `-X utf8` evita a limitação preexistente de encoding padrão Windows no teste de navegação.

## Limites de escopo

O catálogo preserva os guias publicados; esta revisão não valida todas as afirmações de mercado dos 123 textos antigos. Nenhuma mudança na home, preços, serviços, cursos, Stripe, Workers ou automação Academy do PR #86. A publicação depende de uma etapa posterior de coordenação.
