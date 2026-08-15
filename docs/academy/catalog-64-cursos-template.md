# Catálogo 64 cursos — Template para preenchimento humano

Use este arquivo como base. Cada item deve ser validado/complementado pelo responsável comercial antes do deploy.

## Estrutura por curso
- slug
- título
- descrição curta
- proposta de valor
- para quem é
- o que o aluno aprende
- módulos
- benefícios
- entrega
- FAQ
- preço/oferta
- CTA de compra
- status

## Como usar
1. Preencher um bloco por curso abaixo.
2. Conferir que todo CTA aponta para destino existente.
3. Validar que preço/oferta estão corretos.
4. Após preenchimento, rodar validação final.

## Bloco modelo
```
### <slug>
- título:
- descrição curta:
- proposta de valor:
- para quem é:
- o que o aluno aprende:
- módulos:
- benefícios:
- entrega:
- FAQ:
- preço/oferta:
- CTA de compra:
- status: PRONTO_PARA_VENDA
```

## Observações
- Não alterar slugs; eles já estão seedados no banco.
- Manter consistência com `education/cursos/<slug>/index.html` e `vendas.html`.
- Não incluir segredos/credenciais aqui.
