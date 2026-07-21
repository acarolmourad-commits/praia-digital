# Deploy do backend de IA — Praia Digital

Como é serverless, este backend funciona melhor em **Vercel** ou **Netlify**.

## Vercel
1. Instale Vercel CLI: `npm i -g vercel`
2. Na pasta `backend/`, rode: `vercel --prod`
3. Nas configurações do projeto, adicione variáveis de ambiente:
   - `AI_PROVIDER_URL`
   - `AI_API_KEY`
   - `AI_MODEL`
   - `AI_PROVIDER_LABEL`
4. O deploy vai gerar uma URL base. Coloque-a em `ia/chat-central.html` na constante `BACKEND_URL`.

## Netlify
1. No Netlify, ligue este repositório ou pasta.
2. Em `Site settings > Functions`, aponte para `backend/functions/`.
3. Adicione as mesmas variáveis de ambiente.
4. Use a URL base do site como `BACKEND_URL` no chat.

## Sem provedor pago
Sem `AI_PROVIDER_URL`/`AI_API_KEY`, o chat retorna respostas mock.
Os endpoints de leads funcionam sem segredos.

## Teste local
`cd backend && npm install && npm run dev`
`GET /api/` deve retornar `{status:'ok'}`.
