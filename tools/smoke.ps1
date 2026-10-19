# Starts the latest built server pack in a throwaway Docker world, waits until it is ready, checks the logs, stops it.
# Fails on a crash, a 10 minute startup timeout, or errors from FTB Quests or KubeJS.
#   .\tools\smoke.ps1
param([int]$TimeoutMinutes = 10)
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$serverDir = Join-Path $root 'server'
$data = Join-Path $serverDir 'smoke-data'
$compose = @('compose', '-p', 'servus-smoke', '-f', 'docker-compose.yml', '-f', 'docker-compose.smoke.yml')

if (-not (Test-Path (Join-Path $root 'dist/at-your-servus-latest-server.zip'))) { throw 'No server pack, run tools/build.ps1 first' }

function Invoke-Docker([string[]]$arguments) {
    $ErrorActionPreference = 'Continue'
    $out = & docker @arguments 2>&1 | ForEach-Object { "$_" }
    $ErrorActionPreference = 'Stop'
    $out
}

Push-Location $serverDir
$problems = @()
try {
    if (Test-Path $data) { Remove-Item -Recurse -Force $data }
    Invoke-Docker ($compose + @('up', '-d')) | Write-Host
    if ($LASTEXITCODE -ne 0) { throw 'docker compose up failed' }

    $deadline = (Get-Date).AddMinutes($TimeoutMinutes)
    $ready = $false
    while (-not $ready -and (Get-Date) -lt $deadline) {
        Start-Sleep -Seconds 10
        $logs = Invoke-Docker ($compose + @('logs', '--no-color', 'mc'))
        if ($logs -match 'Done \(\d') { $ready = $true; break }
        $state = (Invoke-Docker @('inspect', '-f', '{{.State.Running}}', 'servus-pack-smoke')) -join ''
        if ($state -ne 'true') { break }
    }
    if (-not $ready) {
        $problems += "server did not report ready within $TimeoutMinutes minutes or stopped"
        $problems += ($logs | Select-Object -Last 40)
    }

    $crashes = Get-ChildItem (Join-Path $data 'crash-reports') -Filter '*.txt' -ErrorAction SilentlyContinue
    foreach ($c in $crashes) { $problems += "crash report: $($c.Name)"; $problems += (Get-Content $c.FullName -TotalCount 30) }

    $latest = Join-Path $data 'logs/latest.log'
    if (Test-Path $latest) {
        $problems += Select-String -Path $latest -Pattern '\[[^\]]*/(ERROR|FATAL)\].*(ftbquests|FTB Quests|kubejs|KubeJS)' |
            ForEach-Object { "latest.log: $($_.Line)" }
    }
    $kubejsLogs = Get-ChildItem (Join-Path $data 'logs/kubejs') -Filter '*.log' -ErrorAction SilentlyContinue
    foreach ($k in $kubejsLogs) {
        # Errors anywhere; warnings only when they point at the pack's own scripts (other mods' recipe warnings are theirs).
        $problems += Select-String -Path $k.FullName -CaseSensitive -Pattern '\[ERROR\]|with [1-9]\d* errors|with [1-9][\d,]* failed recipes|\[WARN\].*_scripts[/\\]' |
            ForEach-Object { "$($k.Name): $($_.Line)" }
    }
} finally {
    Invoke-Docker ($compose + @('down')) | Out-Null
    Pop-Location
}

if ($problems.Count -gt 0) {
    $problems | ForEach-Object { Write-Host $_ }
    throw 'smoke check failed'
}
Write-Host 'smoke check passed: the server pack started cleanly'
