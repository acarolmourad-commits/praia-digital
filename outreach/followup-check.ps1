$ErrorActionPreference='SilentlyContinue'
$OutreachDir = Join-Path $PSScriptRoot '..\docs\sales\emails'
$FollowUp1 = Join-Path $PSScriptRoot '..\docs\sales\follow-up-1-3dias.md'
$FollowUp2 = Join-Path $PSScriptRoot '..\docs\sales\follow-up-2-7dias.md'
$FollowUp3 = Join-Path $PSScriptRoot '..\docs\sales\follow-up-3-fechamento.md'
$LogFile = Join-Path $PSScriptRoot '..\docs\sales\followup-log.txt'
$Date = Get-Date -Format 'yyyy-MM-dd HH:mm'
Add-Content -Path $LogFile -Value "$Date - Follow-up check: prepared at $OutreachDir"
Write-Host "Follow-up check: $Date"
