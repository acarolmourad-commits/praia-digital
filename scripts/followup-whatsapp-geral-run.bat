@echo off
rem Wrapper resiliente para o cronjob 'followup-whatsapp-geral' (Windows).
rem Corrige o erro: "! [rejected] main -> main (fetch first)"
rem Causa: clone local desatualizado quando outro processo publica na main.
rem Estrategia: commitar, sincronizar com rebase e so entao dar push.
rem Em conflito, publica em branch propria em vez de falhar o job.

setlocal
cd /d "%~dp0.."

echo == followup-whatsapp-geral: gerando lembretes ==
python scripts\followup_whatsapp_geral.py

git add -A
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "cron: followup whatsapp geral %DATE%"
) else (
  echo Sem mudancas locais para commitar.
)

git fetch origin main
git rebase origin/main
if errorlevel 1 (
  echo Conflito no rebase - publicando em branch propria.
  git rebase --abort
  set BR=cron/followup-whatsapp-geral-%RANDOM%%RANDOM%
  git checkout -b %BR%
  git push -u origin %BR%
  echo Publicado em %BR%. Abrir PR para revisao.
  exit /b 0
)

git push origin main
if errorlevel 1 (
  echo Push rejeitado por corrida - tentando novamente apos rebase.
  git fetch origin main
  git rebase origin/main && git push origin main
)

echo == followup-whatsapp-geral: OK ==
endlocal