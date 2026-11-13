# Solicitações de serviços de IA

Formulários em /solicitar-servico.html e /ia/marketplaces/#cadastro. Avisos automáticos à equipe ativos; consultar NOTIFICACOES.md. Confirmação por e-mail ao visitante não ativada.

Cadastro com protocolo → aviso à equipe → análise e contato → escopo e cotação → aprovação. Sem contratação ou orçamento automático. Dados privados em D1; nenhum endpoint público de listagem.

Publicar worker.mjs e notifications.mjs com deploy-metadata.json, preservando D1 e rate limiter. Cron separado */5 * * * *. Não alterar MX principal Google nem ampliar destinatário do binding. Testes: node --test workers/livebridge-leads/worker.test.mjs.
