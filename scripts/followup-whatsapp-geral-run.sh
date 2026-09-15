#!/usr/bin/env bash
# Wrapper resiliente para o cronjob 'followup-whatsapp-geral'.
# Corrige o erro: "! [rejected] main -> main (fetch first)"
# Causa: o clone local fica desatualizado quando outro processo/agente
# publica na main remota; o push direto é rejeitado (non-fast-forward).
# Estratégia: commitar localmente, sincronizar com rebase, e só então push.
# Em caso de conflito, publica em branch própria em vez de falhar o job.

set -uo pipefail
cd "$(dirname "$0")/.."

echo "== followup-whatsapp-geral: gerando lembretes =="
python scripts/followup_whatsapp_geral.py || true  # lembrete operacional nunca derruba o job

# 1) Commita mudanças locais (se houver)
git add -A
if ! git diff --cached --quiet; then
  git commit -m "cron: followup whatsapp geral $(date +%F)"
else
  echo "Sem mudanças locais para commitar."
fi

# 2) Sincroniza com a main remota ANTES de publicar
git fetch origin main
if ! git rebase origin/main; then
  echo "Conflito no rebase — publicando em branch própria."
  git rebase --abort
  BR="cron/followup-whatsapp-geral-$(date +%Y%m%d-%H%M%S)"
  git checkout -b "$BR"
  git push -u origin "$BR"
  echo "Publicado em $BR. Abrir PR para revisão."
  exit 0
fi

# 3) Push (com 1 retry após novo rebase, cobre corrida entre fetch e push)
if ! git push origin main; then
  echo "Push rejeitado por corrida — tentando novamente após rebase."
  git fetch origin main
  git rebase origin/main && git push origin main
fi

echo "== followup-whatsapp-geral: OK =="
