# Expansão H — Re-segmentação de Follow-up (Msg5 por sinal)

**Rationale:** follow-ups por tempo fixo (D+1/D+2) tratam todos iguais. Leads que chegam em Msg3
sem fechar têm motivos diferentes (dúvida de preço, falta de tempo, desconfiança). Uma Msg5
única não converte. A H gera Msg5 variando por micro-segmento deduzido de Obs/Resposta.

## Micro-segmentos
- `preco` (mencionou preço/ROI) → Msg5 foca em simulação de ROI grátis
- `tempo` (falta de tempo) → Msg5 foca em "zero horas"
- `desconfia` (resposta negativa leve) → Msg5 foca em transparência/sem fidelidade
- `default` → última chance curta

## Entregue
- `scripts/gerar_msg5_resegmentada.py` — gera `lote-msg5-resegmentada-*.csv` (B2C WPP).
  Alvo: leads em `msg3_enviada`/`encerrado`/`sem_interesse` sem `Acao_Conversao`.
  Modo `--demo` gera 3 casos (Ana/Beto/Caio) para treino/validação.

## Status: ✅ script validado (teste sintético + demo), 0 leads reais ainda
O funil B2C está no início (trackers em estágio inicial), logo não há leads em Msg3 sem fechar.
A H opera automaticamente quando houver. Não forjei dados.

## Próximo passo
- [ ] Quando o tracker B2C tiver leads em Msg3, rodar o script e enviar Msg5 por segmento.
