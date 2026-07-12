# instalar-rotina-comercial-diaria.ps1
# Instala tarefa agendada no Windows para a rotina comercial diaria da Praia Digital
$ErrorActionPreference = 'Stop'

$repo = 'C:\Users\Carolina\praia-digital'
$bat = Join-Path $repo 'scripts\rotina-comercial-diaria.bat'
$taskName = 'PraiaDigital-RotinaComercial-Diaria'
$description = 'Rotina automatica diaria da Praia Digital: backup incremental, processamento de leads e briefing matinal'

if (-not (Test-Path $bat)) {
    Write-Host "ERRO: Arquivo nao encontrado: $bat"
    exit 1
}

# Remove tarefa existente para recriar limpa
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue | Out-Null
}

$action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument "/c `"$bat`""
$trigger = New-ScheduledTaskTrigger -Daily -At '08:00'
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

# Usar usuario atual para evitar prompt de senha no contexto local
$principal = New-ScheduledTaskPrincipal -UserId $env:USERDOMAIN\$env:USERNAME -LogonType S4U -RunLevel Highest

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description $description | Out-Null

# Confirmacao
$task = Get-ScheduledTask -TaskName $taskName
Write-Host ""
Write-Host "Tarefa instalada com sucesso!"
Write-Host "Nome: $taskName"
Write-Host "Horario: 08:00 diariamente"
Write-Host "Status: $($task.State)"
Write-Host ""
Write-Host "Para executar manualmente agora:"
Write-Host "  Start-ScheduledTask -TaskName '$taskName'"
Write-Host ""
Write-Host "Para remover depois:"
Write-Host "  Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false"
