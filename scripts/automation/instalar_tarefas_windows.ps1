$ErrorActionPreference = 'SilentlyContinue'

$repo = "C:\Users\Carolina\praia-digital"
$python = "python"
$tasks = @(
    @{
        Name = "PraiaDigital-Followup-Tracker-09h30"
        ScriptPath = "$repo\scripts\automation\agendar_followup_tracker_auto.py"
        Trigger = "Daily at 09:30"
    },
    @{
        Name = "PraiaDigital-HealthCheck-10h30"
        ScriptPath = "$repo\scripts\automation\health_check_site.py"
        Trigger = "Daily at 10:30"
    }
)

foreach ($task in $tasks) {
    $exists = schtasks /Query /TN $task.Name 2>&1
    if ($LASTEXITCODE -eq 0) {
        schtasks /Change /TN $task.Name /TR "cmd /c cd /d $repo && $python $($task.ScriptPath)" 2>&1 | Out-Null
    } else {
        schtasks /Create `
            /TN $task.Name `
            /TR "cmd /c cd /d $repo && $python $($task.ScriptPath)" `
            /SC DAILY `
            /ST (($task.Trigger -split ' at ')[1]) `
            /F 2>&1 | Out-Null
    }
    Write-Host "Tarefa configurada: $($task.Name)"
}
