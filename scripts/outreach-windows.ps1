# Praia Digital - Outreach Windows Helper
# Chamado amigável para rotinas de outreach/SEO no Windows
# Uso: powershell -ExecutionPolicy Bypass -File scripts/outreach-windows.ps1

$ErrorActionPreference = 'Stop'
$Repo = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Repo

Write-Host ''
Write-Host '=================================' -ForegroundColor Cyan
Write-Host '  Praia Digital - Outreach Windows' -ForegroundColor Cyan
Write-Host '=================================' -ForegroundColor Cyan
Write-Host ''
Write-Host 'Oi, tudo bem? Vamos dar uma forcinha nas rotinas do site :)'
Write-Host ''
Write-Host 'O que você quer fazer agora?'
Write-Host '1) Executar gerador de e-mails de prospecção'
Write-Host '2) Abrir outreach/index.html'
Write-Host '3) Mostrar status git curto'
Write-Host ''
$op = Read-Host 'Escolha 1, 2 ou 3'

switch ($op) {
  '1' {
    Write-Host '✅ Rodando gerador de e-mails...' -ForegroundColor Green
    if (Test-Path 'generate_emails.py') { python generate_emails.py } else { Write-Host '❌ generate_emails.py não encontrado.' -ForegroundColor Yellow }
  }
  '2' {
    Write-Host '✅ Abrindo outreach...' -ForegroundColor Green
    if (Test-Path 'outreach/index.html') { Start-Process 'outreach/index.html' } else { Write-Host '❌ outreach/index.html não encontrado.' -ForegroundColor Yellow }
  }
  '3' {
    Write-Host '✅ Verificando git...' -ForegroundColor Green
    if (Get-Command git -ErrorAction SilentlyContinue) { git status -sb } else { Write-Host '❌ git não encontrado.' -ForegroundColor Yellow }
  }
  default {
    Write-Host 'Quase! Escolha 1, 2 ou 3, ok?' -ForegroundColor Yellow
  }
}

Write-Host ''
Write-Host 'Feito! Se precisar, é só rodar de novo. 🚀'
pause
